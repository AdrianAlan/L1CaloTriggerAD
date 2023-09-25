import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import argparse
import numpy as np
import numpy.typing as npt
import tensorflow as tf
import qkeras
import yaml

from tensorflow import keras
from tensorflow.keras import layers, models
from keras.callbacks import ModelCheckpoint

from generator import RegionETGenerator
from models import SupervisedModel
from drawing import Draw
from utils import IsValidFile

from huggingface_hub import from_pretrained_keras
from scipy import interpolate
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from pathlib import Path
from typing import List, Optional, TypedDict


def supervised_training(background, signal, name, epochs, verbose):
    X_train = np.expand_dims(np.append(background, signal, axis=0), axis=-1)
    y_train = np.append(np.zeros(len(background)), np.ones(len(signal)), axis=0)
    y_train = keras.utils.to_categorical(y_train, 2)
    model = SupervisedModel(
        (
            18,
            14,
            1,
        ),
        name,
    ).get_model()
    model.compile(loss="categorical_crossentropy", metrics="accuracy", optimizer="adam")
    model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=2048,
        verbose=verbose,
        shuffle=True,
        validation_split=0.2,
        callbacks=[
            ModelCheckpoint(
                f"models/{name}.h5",
                monitor="val_loss",
                verbose=False,
                save_weights_only=False,
                save_best_only=True,
                mode="min",
            ),
        ],
    )


def gaussian_kernel(size, length=3, sigma=0.5, min_pu=20, max_pu=100):
    pu = np.random.uniform(min_pu, max_pu, size=size)
    eta = np.random.randint(0, 14 - length + 1, size=size)
    phi = np.random.randint(0, 18 - length + 1, size=size)
    ax = np.linspace(-(length - 1) / 2.0, (length - 1) / 2.0, length)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sigma))
    kernel = np.outer(gauss, gauss)
    regions = np.zeros((size, 18, 14))
    for s, (e, p, k) in enumerate(
        zip(eta, phi, np.repeat(pu, 9).reshape(-1, 3, 3) * kernel / np.max(kernel))
    ):
        regions[s, p : p + 3, e : e + 3] = k
    return regions.reshape(size, 18, 14, 1)


def run_training_and_evaluation(
    config: dict,
    train_size: int = 32000,
    test_size: int = 32000,
    epochs: int = 100,
    verbose: bool = False,
) -> None:
    draw = Draw()

    datasets = [i["path"] for i in config["background"] if i["use"]]
    datasets = [path for paths in datasets for path in paths]

    gen = RegionETGenerator()

    bgr_train, _, bgr_test = gen.get_data_split(datasets)
    bgr_train = bgr_train[:train_size]
    bgr_test = bgr_test[:test_size*5]
    X_signals, _ = gen.get_benchmark(config["signal"], filter_acceptance=False)

    config, blend = dict(), []
    for name, X in X_signals.items():
        X_train, X_test = train_test_split(
            X, train_size=train_size, random_state=42, shuffle=True
        )
        X_test = X_test[:test_size]
        config[name] = [X_train, X_test]
        blend.append(X_train[: int(train_size / 5)])
    synthetic = gaussian_kernel(train_size + test_size)
    synthetic_train, synthetic_test = train_test_split(
        synthetic, train_size=train_size, random_state=42, shuffle=True
    )
    config["Synthetic"] = [synthetic_train, synthetic_test]
    config["Blend"] = [np.vstack(blend), None]
    for name, signal in config.items():
        supervised_training(bgr_train, signal[0], name, epochs, verbose=verbose)
    cicada_v1 = from_pretrained_keras("cicada-project/cicada-v1.1")
    cicada_v2 = from_pretrained_keras("cicada-project/cicada-v2.1")

    # Evaluation
    datasets = [rf"$\mathcal{{D}}_{{{i}}}$" for i in list(config.keys())[:-1]]
    models = [rf"$\mathcal{{M}}_{{{i}}}$" for i in list(config.keys())]
    models.append(r"$\mathcal{M}_{Baseline}$")
    models.append(r"$\mathcal{M}_{CICADA.v1}$")
    models.append(r"$\mathcal{M}_{CICADA.v2}$")
    matrix_auc = np.zeros((6, 10))
    matrix_eff_5hz = np.zeros((6, 10))
    matrix_eff_3hz = np.zeros((6, 10))
    matrix_eff_1hz = np.zeros((6, 10))

    for x_idx, signal in enumerate(list(config.values())[:-1]):
        X_test = np.expand_dims(np.append(bgr_test, signal[1], axis=0), axis=-1)
        y_test = np.append(np.zeros(len(bgr_test)), np.ones(len(signal[1])), axis=0)
        for y_idx, (name, signal) in enumerate(config.items()):
            model = SupervisedModel(
                (
                    18,
                    14,
                    1,
                ),
                name,
            ).get_model()
            model.load_weights(f"models/{name}.h5")
            fpr, tpr, _ = roc_curve(y_test, model.predict(X_test)[:, -1])
            roc_auc = auc(fpr, tpr)
            interpolated = interpolate.interp1d(fpr * 28.61, tpr)
            matrix_auc[x_idx][y_idx] = roc_auc
            matrix_eff_5hz[x_idx][y_idx] = interpolated(0.005)
            matrix_eff_3hz[x_idx][y_idx] = interpolated(0.003)
            matrix_eff_1hz[x_idx][y_idx] = interpolated(0.001)

        # Add baseline
        fpr, tpr, _ = roc_curve(y_test, np.mean(X_test, axis=(1, 2, 3)))
        interpolated = interpolate.interp1d(fpr * 28.61, tpr)
        matrix_auc[x_idx][7] = auc(fpr, tpr)
        matrix_eff_5hz[x_idx][7] = interpolated(0.005)
        matrix_eff_3hz[x_idx][7] = interpolated(0.003)
        matrix_eff_1hz[x_idx][7] = interpolated(0.001)

        # Add CICADA_V1
        score = cicada_v1.predict(X_test.reshape(-1, 252))
        fpr, tpr, _ = roc_curve(y_test, score)
        interpolated = interpolate.interp1d(fpr * 28.61, tpr)
        matrix_auc[x_idx][8] = auc(fpr, tpr)
        matrix_eff_5hz[x_idx][8] = interpolated(0.005)
        matrix_eff_3hz[x_idx][8] = interpolated(0.003)
        matrix_eff_1hz[x_idx][8] = interpolated(0.001)

        # Add CICADA_V2
        score = cicada_v2.predict(X_test.reshape(-1, 252))
        fpr, tpr, _ = roc_curve(y_test, score)
        interpolated = interpolate.interp1d(fpr * 28.61, tpr)
        matrix_auc[x_idx][9] = auc(fpr, tpr)
        matrix_eff_5hz[x_idx][9] = interpolated(0.005)
        matrix_eff_3hz[x_idx][9] = interpolated(0.003)
        matrix_eff_1hz[x_idx][9] = interpolated(0.001)

    draw.plot_results_supervised(matrix_auc, "ROC AUC", models, datasets)
    draw.plot_results_supervised(matrix_eff_5hz, "Efficiency 5kHz", models, datasets)
    draw.plot_results_supervised(matrix_eff_3hz, "Efficiency 3kHz", models, datasets)
    draw.plot_results_supervised(matrix_eff_1hz, "Efficiency 1kHz", models, datasets)


def main(args_in: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser("""Profile training and evaluation datasets""")
    parser.add_argument(
        "-c",
        "--config",
        action=IsValidFile,
        type=Path,
        help="Path to the config file",
        default="misc/config.yml",
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
    run_training_and_evaluation(config, verbose=args.verbose, epochs=1, test_size=1000)


if __name__ == "__main__":
    main()
