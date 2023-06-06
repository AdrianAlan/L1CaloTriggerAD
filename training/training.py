import numpy as np
import tensorflow as tf
import qkeras
import yaml

from tensorflow import keras
from qkeras import *

from generator import RegionETGenerator
from models import TeacherAutoencoder, CicadaV1, CicadaV2
from plotting import Draw

tf.get_logger().setLevel("ERROR")


def loss(y_true, y_pred):
    mse = keras.losses.MeanSquaredError(reduction=keras.losses.Reduction.NONE)
    loss = mse(y_true, y_pred).numpy()
    return np.mean(loss, axis=(1, 2))


def train_model(model, X_train_gen, X_val_gen, name):
    draw = Draw("plots")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=keras.losses.MeanSquaredError(reduction=keras.losses.Reduction.AUTO),
    )
    history = model.fit(
        X_train_gen,
        steps_per_epoch=len(X_train_gen),
        epochs=2,
        validation_data=X_val_gen,
        validation_steps=len(X_val_gen),
        verbose=2,
    )
    draw.plot_loss_history(
        history.history["loss"], history.history["val_loss"], f"{name}-training-history"
    )
    model.save(f"saved_models/{name}")
    model = keras.models.load_model(f"saved_models/{name}")
    return model


def main():
    draw = Draw("plots")

    config = yaml.safe_load(open("config.yml"))

    datasets = [i["path"] for i in config["background"] if i["use"]]
    datasets = [path for paths in datasets for path in paths]

    generator = RegionETGenerator()
    X_train, X_val, X_test = generator.get_background_split(datasets)
    X_train_gen = generator.get_generator(X_train, X_train, 128, True)
    X_val_gen = generator.get_generator(X_val, X_val, 128)
    X_signal = generator.get_signal(config["signal"])

    teacher = TeacherAutoencoder((18, 14, 1)).get_model()
    teacher = train_model(teacher, X_train_gen, X_val_gen, "teacher")

    # Comparison between original and reconstructed inputs
    y_example = teacher.predict(X_test[:1], verbose=0)
    draw.plot_reconstruction_results(
        X_test[:1],
        y_example,
        loss=loss(X_test, y_example)[0],
        name="comparison-background",
    )
    y_example = teacher.predict(X_signal["SUSYGGBBH"][:1], verbose=0)
    draw.plot_reconstruction_results(
        X_signal["SUSYGGBBH"][:1],
        y_example,
        loss=loss(X_test, y_example)[0],
        name="comparison-signal",
    )

    # Prepare student datasets
    y_train = teacher.predict(X_train, batch_size=128, verbose=0)
    y_train = loss(X_train, y_train)
    X_train_gen_student = generator.get_generator(
        X_train.reshape((-1, 252, 1)), y_train, 128, True
    )

    y_val = teacher.predict(X_val, batch_size=128, verbose=0)
    y_val = loss(X_val, y_val)
    X_val_gen_student = generator.get_generator(
        X_val.reshape((-1, 252, 1)), y_val, 128, False
    )

    # Knowledge Distillation and Quantization Aware Training
    cicada_v1 = CicadaV1((252,)).get_model()
    cicada_v1 = train_model(
        cicada_v1, X_train_gen_student, X_val_gen_student, "cicada-v1"
    )
    cicada_v2 = CicadaV2((252,)).get_model()
    cicada_v2 = train_model(
        cicada_v1, X_train_gen_student, X_val_gen_student, "cicada-v2"
    )

    # Evaluation
    y_pred_background_teacher = teacher.predict(X_test, batch_size=128, verbose=0)
    y_loss_background_teacher = loss(X_test, y_pred_background_teacher)
    y_loss_background_cicada_v1 = cicada_v1.predict(
        X_test.reshape(-1, 252, 1), batch_size=128, verbose=0
    )
    y_loss_background_cicada_v2 = cicada_v2.predict(
        X_test.reshape(-1, 252, 1), batch_size=128, verbose=0
    )

    results_teacher, results_students = dict(), dict()
    results_teacher["2023 Zero Bias (Test)"] = y_loss_background_teacher
    results_students["cicada_v1"] = dict()
    results_students["cicada_v2"] = dict()
    results_students["cicada_v1"]["2023 Zero Bias (Test)"] = y_loss_background_cicada_v1
    results_students["cicada_v2"]["2023 Zero Bias (Test)"] = y_loss_background_cicada_v2

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
        results_students["cicada_v1"][name] = y_loss_cicada_v1
        results_students["cicada_v2"][name] = y_loss_cicada_v2

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
        results_teacher.values(),
        results_teacher.keys(),
        "anomaly-score-teacher",
    )
    draw.plot_anomaly_score_distribution(
        results_students["cicada_v1"].values(),
        results_students["cicada_v1"].keys(),
        "anomaly-score-cicada-v1",
    )
    draw.plot_anomaly_score_distribution(
        results_students["cicada_v2"].values(),
        results_students["cicada_v2"].keys(),
        "anomaly-score-cicada-v2",
    )

    # ROC Curves with Cross-Validation
    draw.plot_roc_curve(y_true, y_pred_teacher, X_signal.keys(), "roc-teacher")
    draw.plot_roc_curve(y_true, y_pred_cicada_v1, X_signal.keys(), "roc-cicada-v1")
    draw.plot_roc_curve(y_true, y_pred_cicada_v2, X_signal.keys(), "roc-cicada-v2")


if __name__ == "__main__":
    main()
