import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import hls4ml

from huggingface_hub import from_pretrained_keras
from sklearn.metrics import roc_curve, auc
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from qkeras import *


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def load_keras_model(model_path: str):
    # Load the original model
    org_model = from_pretrained_keras(model_path)

    # Rename the input and fix outputs
    input_ = Input(shape=(252,), name="inputs_")
    x = org_model.layers[1](input_)
    x = org_model.layers[2](x)
    x = org_model.layers[3](x)
    x = org_model.layers[4](x)
    output = Activation("relu", name="outputs")(x)

    return Model(input_, output, name="cicada")


def get_datasets():
    datasets = {}
    for dataset_path in [
        "/eos/project/c/cicada-project/data/2023/Signal/SUEP.h5",
        "/eos/project/c/cicada-project/data/2023/Signal/H_ToLongLived.h5",
        "/eos/project/c/cicada-project/data/2023/Signal/SUSYGGBBH.h5",
        "/eos/project/c/cicada-project/data/2023/Signal/TT.h5",
        "/eos/project/c/cicada-project/data/2023/Signal/VBFHto2C.h5",
        "/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_2.h5",
    ]:
        signal_name = dataset_path.split("/")[-1][:-3]
        X_test = h5py.File(dataset_path, "r")["CaloRegions"][:].reshape(-1, 252)
        datasets[signal_name] = X_test
    return datasets


def get_hls_config(keras_model, default_precision="fixed<48, 24>"):
    hls_config = hls4ml.utils.config_from_keras_model(
        keras_model,
        granularity="name",
        backend="Vitis",
        default_precision=default_precision,
    )
    hls_config["Model"]["ReuseFactor"] = 4
    hls_config["Model"]["Strategy"] = "Latency"
    hls_config["Model"]["ClockPeriod"] = 6.25
    hls_config["Model"]["Trace"] = False
    hls_config["Model"]["Precision"] = default_precision
    hls_config["LayerName"]["inputs_"]["Precision"]["accum"] = "ap_ufixed<10, 10>"
    hls_config["LayerName"]["inputs_"]["Precision"]["result"] = "ap_ufixed<10, 10>"
    hls_config["LayerName"]["outputs"]["Precision"]["result"] = "ap_ufixed<16, 8>"

    return hls_config


def convert_to_hls4ml_model(keras_model, hls_config, version="1.0.0"):
    hls4ml.model.optimizer.get_optimizer("output_rounding_saturation_mode").configure(
        layers=["relu1", "QBN1", "outputs"],
        rounding_mode="AP_RND",
        saturation_mode="AP_SAT",
        saturation_bits="AP_SAT",
    )

    # Finish setting up the config
    cfg = hls4ml.converters.create_config()
    cfg["IOType"] = "io_parallel"
    cfg["HLSConfig"] = hls_config
    cfg["KerasModel"] = keras_model
    cfg["ClockPeriod"] = 6.25
    cfg["OutputDir"] = "cicada-v1.1/"
    cfg["Part"] = "xc7vx690tffg1927-2"
    cfg["Version"] = "1.1.0"

    hls_model = hls4ml.converters.keras_to_hls(cfg)
    hls4ml.model.optimizer.get_optimizer("output_rounding_saturation_mode").configure(
        layers=[]
    )

    hls_model.compile()

    return hls_model


def testing(org_model, hls_model, datasets, acceptance_error=0.5):
    scores = {"scores_hls4ml": {}, "scores_keras": {}}
    for dataset_name, test_vectors in datasets.items():
        scores_hls4ml = hls_model.predict(test_vectors)
        scores_keras = org_model.predict(test_vectors)
        scores["scores_hls4ml"][dataset_name] = scores_hls4ml.flatten()
        scores["scores_keras"][dataset_name] = scores_keras.flatten()

    scores_hls4ml = np.concatenate(list(scores["scores_hls4ml"].values()))
    scores_keras = np.concatenate(list(scores["scores_keras"].values()))

    plt.xlabel("Anomaly Score, $S$", fontsize=18)
    plt.ylabel("Error, $|S_{Keras} - S_{hls4ml}|$", fontsize=18)
    plt.scatter(scores_keras, np.abs(scores_keras - scores_hls4ml), s=1)
    plt.savefig("plots/synthesis_error", bbox_inches="tight")
    plt.cla()
    plt.clf()
    plt.close()

    plt.hist(
        scores_keras - scores_hls4ml,
        fc="none",
        histtype="step",
        label="Error distribution",
        bins=100,
    )
    plt.yscale("log")
    plt.xlabel("Error, $S_{Keras} - S_{hls4ml}$", fontsize=18)
    plt.ylabel("Number of samples", fontsize=18)
    plt.savefig("plots/synthesis_error_dist", bbox_inches="tight")
    plt.cla()
    plt.clf()
    plt.close()

    fpr_model = []
    tpr_model = []
    cmap = ["green", "red", "blue", "orange", "brown"]

    scores_keras_normal = scores["scores_keras"]["EZB0_RunC_2"]
    scores_hls4ml_normal = scores["scores_hls4ml"]["EZB0_RunC_2"]

    for dataset_name, color in zip(list(scores["scores_keras"].keys())[:-1], cmap):
        scores_keras_anomaly = scores["scores_keras"][dataset_name]
        scores_hls4ml_anomaly = scores["scores_hls4ml"][dataset_name]

        y_true = np.append(
            np.zeros(len(scores_keras_normal)), np.ones(len(scores_hls4ml_anomaly))
        )
        y_score_keras = np.append(scores_keras_normal, scores_keras_anomaly)
        y_score_hls = np.append(scores_hls4ml_normal, scores_hls4ml_anomaly)

        for y_scores, model, ls in zip(
            [y_score_keras, y_score_hls], ["Keras", "hls4ml"], ["-", "--"]
        ):
            fpr, tpr, thresholds = roc_curve(y_true, y_scores)
            plt.plot(
                fpr * 28.61,
                tpr,
                linestyle=ls,
                color=color,
                label="{0}: {1}, AUC = {2:.4f}".format(
                    model, dataset_name, auc(fpr, tpr)
                ),
            )

    plt.plot(
        [0.003, 0.003],
        [0, 1],
        linestyle="--",
        color="black",
        label="3 kHz trigger rate",
    )
    plt.xlim([0.0002861, 28.61])
    plt.ylim([0.001, 1.0])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Trigger Rate (MHz)")
    plt.ylabel("Signal Efficiency")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.savefig("plots/synthesis_comparison", bbox_inches="tight")
    plt.cla()
    plt.clf()
    plt.close()

    hls4ml.utils.plot_model(
        hls_model,
        show_shapes=True,
        show_precision=True,
        to_file="plots/synthesis_model_v1.1.png",
    )


if __name__ == "__main__":
    plt.style.use("../misc/style.mplstyle")
    keras_model = load_keras_model("cicada-project/cicada-v1.1")
    hls_config = get_hls_config(keras_model)
    hls_model = convert_to_hls4ml_model(keras_model, hls_config, "1.1.0")
    datasets = get_datasets()
    testing(keras_model, hls_model, datasets)
