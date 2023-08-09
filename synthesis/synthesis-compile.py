import argparse
import glob
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import shutil
import yaml
import hls4ml

from pathlib import Path
from hls4ml.model.layers import Activation as ActivationHLS
from hls4ml.model.optimizer import OptimizerPass, register_pass
from huggingface_hub import from_pretrained_keras
from sklearn.metrics import roc_curve, auc
from qkeras import *

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class EliminateLinearActivationCustom(OptimizerPass):
    def match(self, node):
        return (
            isinstance(node, ActivationHLS) and node.get_attr("activation") == "linear"
        )

    def transform(self, model, node):
        model.remove_node(node)
        return True


def get_datasets(dataset_config):
    datasets = {}
    dataset_paths = yaml.safe_load(open(dataset_config))
    for dataset_path in dataset_paths:
        signal_name = dataset_path.split("/")[-1][:-3]
        X_test = h5py.File(dataset_path, "r")["CaloRegions"][:].reshape(-1, 252)
        datasets[signal_name] = X_test
    return datasets


def get_hls_config(keras_model, version):
    hls_config = hls4ml.utils.config_from_keras_model(keras_model, granularity="name")

    hls_config["Model"]["Strategy"] = "Latency"

    for layer in hls_config["LayerName"].keys():
        hls_config["LayerName"][layer]["ReuseFactor"] = 2

    hls_config["LayerName"]["inputs_"]["Precision"]["result"] = "ap_uint<10>"
    if version.startswith("1"):
        hls_config["LayerName"]["dense1"]["Precision"]["result"] = "ap_fixed<26, 20>"
        hls_config["LayerName"]["dense1"]["Precision"]["accum"] = "ap_fixed<26, 20>"
    else:
        hls_config["LayerName"]["conv"]["Strategy"] = "Resource"
        hls_config["LayerName"]["conv"]["ReuseFactor"] = 1
        hls_config["LayerName"]["conv"]["ParallelizationFactor"] = 21
        hls_config["LayerName"]["conv"]["Precision"]["result"] = "ap_fixed<30, 22>"
        hls_config["LayerName"]["conv"]["Precision"]["accum"] = "ap_fixed<30, 22>"
        hls_config["LayerName"]["dense1"]["Precision"]["result"] = "ap_fixed<26, 14>"
        hls_config["LayerName"]["dense1"]["Precision"]["accum"] = "ap_fixed<26, 14>"

    hls_config["LayerName"]["dense2"]["Precision"]["result"] = "ap_fixed<26, 14>"
    hls_config["LayerName"]["dense2"]["Precision"]["accum"] = "ap_fixed<26, 14>"

    return hls_config


def convert_to_hls4ml_model(keras_model, hls_config, version="1.0.0"):
    hls_model = hls4ml.converters.convert_from_keras_model(
        keras_model,
        clock_period=6.25,
        backend="Vitis",
        hls_config=hls_config,
        io_type="io_parallel",
        output_dir="cicada-v{}".format(version),
        part="xc7vx690tffg1927-2",
        project_name="cicada",
        version=version,
    )
    hls_model.compile()
    return hls_model


def testing(org_model, hls_model, datasets, version, mplstyle):
    scores = {"scores_hls4ml": {}, "scores_keras": {}}
    for dataset_name, test_vectors in datasets.items():
        scores_hls4ml = hls_model.predict(test_vectors)
        scores_keras = org_model.predict(test_vectors)
        scores["scores_hls4ml"][dataset_name] = scores_hls4ml.flatten()
        scores["scores_keras"][dataset_name] = scores_keras.flatten()

    scores_hls4ml = np.concatenate(list(scores["scores_hls4ml"].values()))
    scores_keras = np.concatenate(list(scores["scores_keras"].values()))

    # Load plottling style
    plt.style.use(mplstyle)

    plt.xlabel("Anomaly Score, $S$", fontsize=18)
    plt.ylabel("Error, $|S_{Keras} - S_{hls4ml}|$", fontsize=18)
    plt.scatter(scores_keras, np.abs(scores_keras - scores_hls4ml), s=1)
    plt.savefig("plots/synthesis_error_v{}.png".format(version), bbox_inches="tight")
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
    plt.savefig(
        "plots/synthesis_error_dist_v{}.png".format(version), bbox_inches="tight"
    )
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
    plt.ylim([0.01, 1.0])
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Trigger Rate (MHz)")
    plt.ylabel("Signal Efficiency")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.savefig(
        "plots/synthesis_comparison_v{}.png".format(version), bbox_inches="tight"
    )
    plt.cla()
    plt.clf()
    plt.close()

    hls4ml.utils.plot_model(
        hls_model,
        show_shapes=True,
        show_precision=True,
        to_file="plots/synthesis_model_v{}.png".format(version),
    )


def load_configuration():
    parser = argparse.ArgumentParser(description="Convert QKeras model to hls4ml model")
    parser.add_argument("--datasets", "-d", type=Path, help="Path to yml with datasets")
    parser.add_argument("--style", "-s", type=Path, help="Path to plotting style")
    parser.add_argument("--version", "-v", type=str, help="CICADA version")
    args = parser.parse_args()
    return args.datasets, args.style, args.version


def cleanup():
    for f in glob.glob("*.tar.gz"):
        os.remove(f)
    shutil.rmtree("cicada-vdebug")


def main():
    dataset_config, style, version = load_configuration()

    # Workaround for linear activation layer removal
    hls4ml.model.flow.flow.update_flow(
        "optimize", remove_optimizers=["eliminate_linear_activation"]
    )
    register_pass(
        "overwrite_eliminate_linear_activation", EliminateLinearActivationCustom
    )
    hls4ml.model.flow.flow.update_flow(
        "convert", add_optimizers=["overwrite_eliminate_linear_activation"]
    )

    # Load QKeras model
    keras_model = from_pretrained_keras(
        "cicada-project/cicada-v{}".format(".".join(version.split(".")[:-1]))
    )
    # Genrate hls4ml config
    hls_config = get_hls_config(keras_model)

    # Genrate hls4ml model
    hls_model = convert_to_hls4ml_model(keras_model, hls_config, version)

    # Gather evaluation datasets
    datasets = get_datasets(dataset_config)

    # Final tests of the final configuration
    testing(keras_model, hls_model, datasets, version, style)

    cleanup()


if __name__ == "__main__":
    main()
