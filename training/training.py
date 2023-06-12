import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import argparse
import numpy as np
import numpy.typing as npt
import tensorflow as tf
import qkeras
import yaml

from pathlib import Path
from tensorflow import keras
from qkeras import *
from typing import List, Optional, TypedDict

from generator import RegionETGenerator
from models import TeacherAutoencoder, CicadaV1, CicadaV2
from plotting import Draw
from utils import IsValidFile

tf.get_logger().setLevel("ERROR")


def loss(y_true: npt.NDArray, y_pred: npt.NDArray) -> npt.NDArray:
    return np.mean((y_true - y_pred) ** 2, axis=(1, 2, 3))


def train_model(
    model: tf.keras.Model,
    X_train_gen: tf.data.Dataset,
    X_val_gen: tf.data.Dataset,
    name: str,
) -> None:
    draw = Draw(Path("plots"))
    model.compile(optimizer="adam", loss="mse")
    history = model.fit(
        X_train_gen,
        steps_per_epoch=len(X_train_gen),
        epochs=40,
        validation_data=X_val_gen,
        verbose=1,
    )
    draw.plot_loss_history(
        history.history["loss"], history.history["val_loss"], f"{name}-training-history"
    )
    model.save(f"saved_models/{name}")


def run_training(config: dict, eval_only: bool, verbose: bool) -> None:
    draw = Draw(Path("plots"))

    datasets = [i["path"] for i in config["background"] if i["use"]]
    datasets = [path for paths in datasets for path in paths]

    generator = RegionETGenerator()
    X_train, X_val, X_test = generator.get_background_split(datasets)
    X_train_gen = generator.get_generator(X_train, X_train, 128, True)
    X_val_gen = generator.get_generator(X_val, X_val, 128)
    X_signal = generator.get_signal(config["signal"], filter_acceptance=False)

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
    y_train_teacher = teacher.predict(X_train, batch_size=128, verbose=0)
    y_train = loss(X_train, y_train_teacher)
    X_train_gen_student = generator.get_generator(
        X_train.reshape((-1, 252, 1)), y_train, 1024, True
    )

    y_val_teacher = teacher.predict(X_val, batch_size=128, verbose=0)
    y_val = loss(X_val, y_val_teacher)
    X_val_gen_student = generator.get_generator(
        X_val.reshape((-1, 252, 1)), y_val, 1024, False
    )

    # Knowledge Distillation and Quantization Aware Training
    if not eval_only:
        cicada_v1 = CicadaV1((252,)).get_model()
        cicada_v1 = train_model(
            cicada_v1, X_train_gen_student, X_val_gen_student, "cicada-v1"
        )
        cicada_v2 = CicadaV2((252,)).get_model()
        cicada_v2 = train_model(
            cicada_v2, X_train_gen_student, X_val_gen_student, "cicada-v2"
        )

    cicada_v1 = keras.models.load_model("saved_models/cicada-v1")
    cicada_v2 = keras.models.load_model("saved_models/cicada-v2")

    # Evaluation
    y_pred_background_teacher = teacher.predict(X_test, batch_size=128, verbose=0)
    y_loss_background_teacher = loss(X_test, y_pred_background_teacher)
    y_loss_background_cicada_v1 = cicada_v1.predict(
        X_test.reshape(-1, 252, 1), batch_size=128, verbose=0
    )
    y_loss_background_cicada_v2 = cicada_v2.predict(
        X_test.reshape(-1, 252, 1), batch_size=128, verbose=0
    )

    results_teacher, results_cicada_v1, results_cicada_v2 = dict(), dict(), dict()
    results_teacher["2023 Zero Bias (Test)"] = y_loss_background_teacher
    results_cicada_v1["2023 Zero Bias (Test)"] = y_loss_background_cicada_v1
    results_cicada_v2["2023 Zero Bias (Test)"] = y_loss_background_cicada_v2

    y_true, y_pred_teacher, y_pred_cicada_v1, y_pred_cicada_v2 = [], [], [], []
    for name, data in X_signal.items():
        y_loss_teacher = loss(data, teacher.predict(data, batch_size=128, verbose=0))
        y_loss_cicada_v1 = cicada_v1.predict(
            data.reshape(-1, 252, 1), batch_size=128, verbose=0
        )
        y_loss_cicada_v2 = cicada_v2.predict(
            data.reshape(-1, 252, 1), batch_size=128, verbose=0
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
    draw.plot_roc_curve(y_true, y_pred_teacher, [*X_signal], "roc-teacher")
    draw.plot_roc_curve(y_true, y_pred_cicada_v1, [*X_signal], "roc-cicada-v1")
    draw.plot_roc_curve(y_true, y_pred_cicada_v2, [*X_signal], "roc-cicada-v2")


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