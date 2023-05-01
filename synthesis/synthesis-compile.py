import argparse
import h5py
import math
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import hls4ml
import yaml

from pathlib import Path
from hls4ml.model.layers import Activation as ActivationHLS
from hls4ml.model.optimizer import OptimizerPass, register_pass
from huggingface_hub import from_pretrained_keras
from sklearn.metrics import roc_curve, auc
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
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


def load_keras_model(model_path: str):
    # Load the original model
    org_model = from_pretrained_keras(model_path)

    # Rename the input and fix outputs
    x = input_ = Input(shape=(252,), name="inputs_")
    for layer in org_model.layers[1:]:
        x = layer(x)
    output = Activation("relu", name="outputs")(x)
    return Model(input_, output, name="cicada"), org_model


def get_datasets(dataset_paths):
    datasets = {}
    for dataset_path in dataset_paths:
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
    # Additinal parameters needed for CICADAv2
    if "conv" in hls_config["LayerName"]:
        hls_config["LayerName"]["conv"]["Strategy"] = "Resource"
        hls_config["LayerName"]["conv"]["ReuseFactor"] = 1
        hls_config["LayerName"]["conv"]["ParallelizationFactor"] = 12
    return hls_config


def convert_to_hls4ml_model(keras_model, hls_config, version="1.0.0"):
    cfg = hls4ml.converters.create_config()
    cfg["IOType"] = "io_parallel"
    cfg["HLSConfig"] = hls_config
    cfg["KerasModel"] = keras_model
    cfg["ClockPeriod"] = 6.25
    cfg["OutputDir"] = "cicada-v{}".format(version)
    cfg["Part"] = "xc7vx690tffg1927-2"
    cfg["Version"] = version
    hls_model = hls4ml.converters.keras_to_hls(cfg)
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


def search_for_best(
    low,
    high,
    layer,
    parameter,
    hls_config,
    test_vector,
    keras_model,
    keras_out,
    accepted_error,
    int_=True,
    other=32,
):
    while low < high:
        mid = (high + low) // 2
        precision = [mid, other]
        if int_:
            precision = precision[::-1]
        hls_config["LayerName"][layer]["Precision"][
            parameter
        ] = "ap_fixed<{}, {}>".format(*precision)
        hls_model = convert_to_hls4ml_model(keras_model, hls_config, version="debug")
        hls4ml_out = hls_model.predict(test_vector)
        if np.all(np.abs(hls4ml_out - keras_out) < accepted_error):
            high = mid
        else:
            low = mid + 1
    return low


def adjust_additional_parameter(
    layer_name,
    parameter,
    int_,
    hls_config,
    test_vector,
    keras_model,
    keras_out,
    accepted_error,
):
    high_precision = re.findall(
        "\d+", hls_config["LayerName"][layer_name]["Precision"][parameter]
    )
    decimal = search_for_best(
        int_,
        int(high_precision[0]),
        layer_name,
        parameter,
        hls_config,
        test_vector,
        keras_model,
        keras_out,
        accepted_error,
        False,
        other=int_,
    )
    hls_config["LayerName"][layer_name]["Precision"][
        parameter
    ] = "ap_fixed<{}, {}>".format(decimal, int_)
    return hls_config


def tune_batch_norm_precision(
    layer_name,
    bn_layer,
    hls_config,
    test_vector,
    keras_model,
    keras_out,
    accepted_error,
):
    weights = [*bn_layer.get_weights()]
    int_scale = int(np.ceil(np.log(np.ceil(np.max(np.abs(weights[0].data))))) + 1)
    int_bias = int(np.ceil(np.log(np.ceil(np.max(np.abs(weights[1].data))))) + 1)
    hls_config = adjust_additional_parameter(
        layer_name,
        "scale",
        int_scale,
        hls_config,
        test_vector,
        keras_model,
        keras_out,
        accepted_error,
    )
    hls_config = adjust_additional_parameter(
        layer_name,
        "bias",
        int_bias,
        hls_config,
        test_vector,
        keras_model,
        keras_out,
        accepted_error,
    )
    return hls_config


def adjust_result_precision(
    layers, hls_config, profiling, test_vector, keras_model, keras_out, accepted_error
):
    for layer in layers[:-1]:
        result_precision = re.findall(
            "\d+", hls_config["LayerName"][layer]["Precision"]["result"]
        )
        int_ = math.ceil(math.log(int(np.max(np.abs(profiling[layer]))) + 1, 2)) + 1
        decimal = search_for_best(
            int_,
            int(result_precision[0]),
            layer,
            "result",
            hls_config,
            test_vector,
            keras_model,
            keras_out,
            accepted_error,
            False,
            other=int_,
        )
        hls_config["LayerName"][layer]["Precision"][
            "result"
        ] = "ap_fixed<{}, {}>".format(decimal, int_)
    hls_config["LayerName"][layers[-1]]["Precision"]["result"] = "ap_fixed<16, 8>"
    return hls_config


def adjust_accumulator_precision(
    layers, hls_config, test_vector, keras_model, keras_out, max_bits, accepted_error
):
    for layer in layers:
        result_precision = re.findall(
            "\d+", hls_config["LayerName"][layer]["Precision"]["result"]
        )
        int_ = search_for_best(
            int(result_precision[0]),
            max_bits,
            layer,
            "accum",
            hls_config,
            test_vector,
            keras_model,
            keras_out,
            accepted_error,
            True,
            other=max_bits,
        )
        decimal = search_for_best(
            max(int_, int(result_precision[1])),
            max_bits,
            layer,
            "accum",
            hls_config,
            test_vector,
            keras_model,
            keras_out,
            accepted_error,
            False,
            other=int_,
        )
        hls_config["LayerName"][layer]["Precision"][
            "accum"
        ] = "ap_fixed<{}, {}>".format(decimal, int_)
    return hls_config


def load_configuration():
    parser = argparse.ArgumentParser(description="Convert QKeras model to hls4ml model")
    parser.add_argument("--config", "-c", type=Path, help="Configuration file")
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))
    return config


def main():
    config = load_configuration()

    # Update default optimizers in hls4ml
    hls4ml.model.flow.flow.update_flow(
        "convert", remove_optimizers=["qkeras_factorize_alpha"]
    )
    hls4ml.model.flow.flow.update_flow(
        "optimize", remove_optimizers=["eliminate_linear_activation"]
    )
    register_pass(
        "overwrite_eliminate_linear_activation", EliminateLinearActivationCustom
    )
    hls4ml.model.flow.flow.update_flow(
        "convert", add_optimizers=["overwrite_eliminate_linear_activation"]
    )
    hls4ml.model.optimizer.get_optimizer("output_rounding_saturation_mode").configure(
        layers=config["optimizer_sat_layers"],
        rounding_mode="AP_RND",
        saturation_mode="AP_SAT",
        saturation_bits="AP_SAT",
    )

    # Load QKeras model
    keras_model, org_model = load_keras_model(
        "cicada-project/cicada-v{}".format(".".join(config["version"].split(".")[:-1]))
    )

    # Genrate hls4ml config
    hls_config = get_hls_config(keras_model)
    # Genrate hls4ml model
    hls_model = convert_to_hls4ml_model(keras_model, hls_config, config["version"])

    # Gather evaluation datasets
    datasets = get_datasets(config["datasets"])
    test_vector = np.vstack(list(datasets.values()))
    keras_out = keras_model.predict(test_vector)

    # Tune BatchNorm parameters in v1:
    bn_layers = [
        i for i in hls_model.get_layers() if "BatchNormalization" in type(i).__name__
    ]
    if len(bn_layers):
        bn_layer = bn_layers[0]
        hls_config = tune_batch_norm_precision(
            "QBN1",
            bn_layer,
            hls_config,
            test_vector,
            keras_model,
            keras_out,
            accepted_error=config["accepted_error"],
        )

    # Tune result and accumulator precision
    keras_trace = hls4ml.model.profiling.get_ymodel_keras(org_model, test_vector)
    adjust_result_precision(
        config["layers_to_tune"],
        hls_config,
        keras_trace,
        test_vector,
        keras_model,
        keras_out,
        accepted_error=config["accepted_error"],
    )
    adjust_accumulator_precision(
        config["layers_to_tune"],
        hls_config,
        test_vector,
        keras_model,
        keras_out,
        48,
        accepted_error=config["accepted_error"],
    )

    # Recomple the model
    hls_model = convert_to_hls4ml_model(keras_model, hls_config, config["version"])

    # Final tests of the final configuration
    testing(keras_model, hls_model, datasets, config["version"], config["mplstyle"])


if __name__ == "__main__":
    main()
