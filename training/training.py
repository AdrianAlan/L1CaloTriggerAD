import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import argparse
import numpy as np
import numpy.typing as npt
import tensorflow as tf
import qkeras
import yaml

from pathlib import Path
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from qkeras import *
from typing import List, Optional, TypedDict

from generator import RegionETGenerator
from models import TeacherAutoencoder, CicadaV1, CicadaV2
from plotting import Draw
from utils import IsValidFile

tf.get_logger().setLevel("ERROR")


def loss(y_true: npt.NDArray, y_pred: npt.NDArray) -> npt.NDArray:
    return np.mean((y_true - y_pred) ** 2, axis=(1, 2, 3))


def quantize(arr: npt.NDArray, precision: tuple = (16, 8)) -> npt.NDArray:
    word, int_ = precision
    decimal = word - int_
    step = 1 / 2**decimal
    max_ = 2**int_ - step
    arrq = step * np.round(arr / step)
    arrc = np.clip(arrq, 0, max_)
    return arrc


def train_model(
    model: tf.keras.Model,
    X_train_gen: tf.data.Dataset,
    X_val_gen: tf.data.Dataset,
    name: str,
    lr: float = 0.001,
    epochs: int = 100,
    loss: str = "mse",
) -> None:
    draw = Draw(Path("plots"))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr), loss=loss)
    history = model.fit(
        X_train_gen,
        steps_per_epoch=len(X_train_gen),
        epochs=epochs,
        validation_data=X_val_gen,
        verbose=1,
        callbacks=[
            ReduceLROnPlateau(factor=0.5, patience=20),
            ModelCheckpoint(
                f"saved_models/{name}", save_weights_only=False, save_best_only=True
            ),
        ],
    )
    draw.plot_loss_history(
        history.history["loss"], history.history["val_loss"], f"{name}-training-history"
    )


def run_training(config: dict, eval_only: bool, verbose: bool) -> None:
    draw = Draw(Path("plots"))

    datasets = [i["path"] for i in config["background"] if i["use"]]
    datasets = [path for paths in datasets for path in paths]

    generator = RegionETGenerator()
    X_train, X_val, X_test = generator.get_background_split(datasets)
    X_train_gen = generator.get_generator(X_train, X_train, 512, True)
    X_val_gen = generator.get_generator(X_val, X_val, 512)
    X_signal = generator.get_signal(config["signal"], filter_acceptance=False)
    outlier_train = generator.get_background(config["exposure"]["training"])
    outlier_val = generator.get_background(config["exposure"]["validation"])

    if not eval_only:
        teacher = TeacherAutoencoder((18, 14, 1)).get_model()
        train_model(teacher, X_train_gen, X_val_gen, "teacher")
    teacher = keras.models.load_model("saved_models/teacher")

    # Comparison between original and reconstructed inputs
    X_example = X_test[:1]
    y_example = teacher.predict(X_example, verbose=0)
    draw.plot_reconstruction_results(
        X_example,
        y_example,
        loss=loss(X_example, y_example)[0],
        name="comparison-background",
    )
    X_example = X_signal["SUSYGGBBH"][:1]
    y_example = teacher.predict(X_example, verbose=0)
    draw.plot_reconstruction_results(
        X_example,
        y_example,
        loss=loss(X_example, y_example)[0],
        name="comparison-signal",
    )

    # Prepare student datasets
    X_train_student = np.concatenate([X_train, outlier_train])
    y_train_teacher = teacher.predict(X_train_student, batch_size=512, verbose=0)
    y_train = loss(X_train_student, y_train_teacher)
    y_train = np.log(y_train) * 32
    y_train = quantize(y_train)
    X_train_gen_student = generator.get_generator(
        X_train_student.reshape((-1, 252, 1)), y_train, 1024, True
    )

    X_val_student = np.concatenate([X_val, outlier_train])
    y_val_teacher = teacher.predict(X_val_student, batch_size=512, verbose=0)
    y_val = loss(X_val_student, y_val_teacher)
    y_val = np.log(y_val) * 32
    y_val = quantize(y_val)
    X_val_gen_student = generator.get_generator(
        X_val_student.reshape((-1, 252, 1)), y_val, 1024, False
    )

    # Knowledge Distillation and Quantization Aware Training
    if not eval_only:
        cicada_v1 = CicadaV1((252,)).get_model()
        cicada_v1 = train_model(
            cicada_v1,
            X_train_gen_student,
            X_val_gen_student,
            "cicada-v1",
            lr=0.01,
            epochs=1024,
            loss="mae",
        )
        cicada_v2 = CicadaV2((252,)).get_model()
        cicada_v2 = train_model(
            cicada_v2,
            X_train_gen_student,
            X_val_gen_student,
            "cicada-v2",
            lr=0.01,
            epochs=1024,
            loss="mae",
        )

    cicada_v1 = keras.models.load_model("saved_models/cicada-v1")
    cicada_v2 = keras.models.load_model("saved_models/cicada-v2")

    # Evaluation
    y_pred_background_teacher = teacher.predict(X_test, batch_size=512, verbose=0)
    y_loss_background_teacher = loss(X_test, y_pred_background_teacher)
    y_loss_background_cicada_v1 = cicada_v1.predict(
        X_test.reshape(-1, 252, 1), batch_size=512, verbose=0
    )
    y_loss_background_cicada_v2 = cicada_v2.predict(
        X_test.reshape(-1, 252, 1), batch_size=512, verbose=0
    )

    results_teacher, results_cicada_v1, results_cicada_v2 = dict(), dict(), dict()
    results_teacher["2023 Zero Bias (Test)"] = y_loss_background_teacher
    results_cicada_v1["2023 Zero Bias (Test)"] = y_loss_background_cicada_v1
    results_cicada_v2["2023 Zero Bias (Test)"] = y_loss_background_cicada_v2

    y_true, y_pred_teacher, y_pred_cicada_v1, y_pred_cicada_v2 = [], [], [], []
    inputs = []
    for name, data in X_signal.items():
        inputs.append(np.concatenate((data, X_test)))

        y_loss_teacher = loss(data, teacher.predict(data, batch_size=512, verbose=0))
        y_loss_cicada_v1 = cicada_v1.predict(
            data.reshape(-1, 252, 1), batch_size=512, verbose=0
        )
        y_loss_cicada_v2 = cicada_v2.predict(
            data.reshape(-1, 252, 1), batch_size=512, verbose=0
        )
        results_teacher[name] = y_loss_teacher
        results_cicada_v1[name] = y_loss_cicada_v1
        results_cicada_v2[name] = y_loss_cicada_v2

        y_true.append(
            np.concatenate((np.ones(data.shape[0]), np.zeros(X_test.shape[0])))
        )
        y_pred_teacher.append(
            np.concatenate((y_loss_teacher, y_loss_background_teacher))
        )
        y_pred_cicada_v1.append(
            np.concatenate((y_loss_cicada_v1, y_loss_background_cicada_v1))
        )
        y_pred_cicada_v2.append(
            np.concatenate((y_loss_cicada_v2, y_loss_background_cicada_v2))
        )

    draw.plot_anomaly_score_distribution(
        list(results_teacher.values()),
        [*results_teacher],
        "anomaly-score-teacher",
    )
    draw.plot_anomaly_score_distribution(
        list(results_cicada_v1.values()),
        [*results_cicada_v1],
        "anomaly-score-cicada-v1",
    )
    draw.plot_anomaly_score_distribution(
        list(results_cicada_v2.values()),
        [*results_cicada_v2],
        "anomaly-score-cicada-v2",
    )

    # ROC Curves with Cross-Validation
    draw.plot_roc_curve(y_true, y_pred_teacher, [*X_signal], inputs, "roc-teacher")
    draw.plot_roc_curve(y_true, y_pred_cicada_v1, [*X_signal], inputs, "roc-cicada-v1")
    draw.plot_roc_curve(y_true, y_pred_cicada_v2, [*X_signal], inputs, "roc-cicada-v2")


def main(args_in: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser("""Profile training and evaluation datasets""")
    parser.add_argument(
        "-c",
        "--config",
        action=IsValidFile,
        type=Path,
        help="Path to the config file",
        default="config.yml",
    )
    parser.add_argument(
        "--evaluate-only",
        action="store_true",
        help="Skip training",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Output verbosity",
        default=False,
    )
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))
    run_training(config, args.evaluate_only, args.verbose)


if __name__ == "__main__":
    main()
