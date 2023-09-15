import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import numpy.typing as npt
import hls4ml

from pathlib import Path
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from typing import List


class Draw:
    def __init__(self, output_dir: Path = "plots"):
        self.output_dir = output_dir
        self.cmap = ["green", "red", "blue", "orange", "purple", "brown"]
        hep.style.use("CMS")

    def _parse_name(self, name: str) -> str:
        return name.replace(" ", "-").lower()

    def plot_loss_history(
        self, training_loss: npt.NDArray, validation_loss: npt.NDArray, name: str
    ) -> None:
        plt.figure(figsize=(15, 10))
        plt.plot(np.arange(1, len(training_loss) + 1), training_loss, label="Training")
        plt.plot(
            np.arange(1, len(validation_loss) + 1), validation_loss, label="Validation"
        )
        plt.legend(loc="upper right")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.savefig(
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
        )
        plt.close()

    def plot_regional_deposits(
        self, deposits: npt.NDArray, mean: float, name: str
    ) -> None:
        im = plt.imshow(
            deposits.reshape(18, 14), vmin=0, vmax=deposits.max(), cmap="Purples"
        )
        ax = plt.gca()
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(r"E$_T$ (GeV)")  # , rotation=-90, va="bottom")
        plt.axis("off")
        plt.title(rf"Mean E$_T$ {mean: .2f} ({name})")
        plt.savefig(
            f"{self.output_dir}/profiling-mean-deposits-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()

    def plot_spacial_deposits_distribution(
        self, deposits: List[npt.NDArray], labels: List[str], name: str
    ) -> None:
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122)
        for deposit, label in zip(deposits, labels):
            bins = np.argwhere(deposit)
            phi, eta = bins[:, 1], bins[:, 2]
            ax1.hist(
                eta + 4,
                density=True,
                facecolor=None,
                bins=np.arange(4, 19),
                label=label,
                histtype="step",
            )
            ax2.hist(
                phi,
                density=True,
                facecolor=None,
                bins=np.arange(19),
                label=label,
                histtype="step",
            )
        ax1.set_ylabel("a.u.")
        ax1.set_xlabel(r"i$\eta$")
        ax2.set_xlabel(r"i$\phi$")
        plt.legend(loc="best")
        plt.savefig(
            f"{self.output_dir}/profiling-spacial-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()

    def plot_deposits_distribution(
        self, deposits: List[npt.NDArray], labels: List[str], name: str
    ) -> None:
        for deposit, label in zip(deposits, labels):
            plt.hist(
                deposit.reshape((-1)),
                bins=100,
                range=(0, 1024),
                density=1,
                label=label,
                log=True,
                histtype="step",
            )
        plt.xlabel(r"E$_T$")
        plt.legend(loc="best")
        plt.savefig(
            f"{self.output_dir}/profiling-deposits-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()

    def plot_reconstruction_results(
        self,
        deposits_in: npt.NDArray,
        deposits_out: npt.NDArray,
        loss: float,
        name: str,
    ) -> None:
        fig, ax = plt.subplots(figsize=(17, 17))

        max_deposit = max(deposits_in.max(), deposits_out.max())

        ax1 = plt.subplot(3, 3, 1)
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        ax1.set_title("Original")
        ax1.imshow(
            deposits_in.reshape(18, 14), vmin=0, vmax=max_deposit, cmap="Purples"
        )

        ax2 = plt.subplot(3, 3, 2)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        ax2.set_title("Reconstructed")
        ax2.imshow(
            deposits_out.reshape(18, 14), vmin=0, vmax=max_deposit, cmap="Purples"
        )

        ax3 = plt.subplot(3, 3, 3)
        ax3.get_xaxis().set_visible(False)
        ax3.get_yaxis().set_visible(False)
        ax3.set_title(f"Absolute Difference, MSE: {loss: .2f}")

        im = ax3.imshow(
            np.abs(deposits_in - deposits_out).reshape(18, 14),
            vmin=0,
            vmax=max_deposit,
            cmap="Purples",
        )
        cbar = ax3.figure.colorbar(im, ax=ax3)
        cbar.ax.set_ylabel(r"E$_T$ (GeV)", rotation=-90, va="bottom")

        plt.savefig(
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
        )
        plt.close()

    def plot_anomaly_score_distribution(
        self, scores: List[npt.NDArray], labels: List[str], name: str
    ) -> None:
        plt.figure(figsize=(15, 10))
        for score, label in zip(scores, labels):
            plt.hist(
                score.reshape((-1)),
                bins=100,
                range=(0, 256),
                density=1,
                label=label,
                log=True,
                histtype="step",
            )
        plt.xlabel(r"Anomaly Score")
        plt.legend(loc="best")
        plt.savefig(
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
        )
        plt.close()

    def plot_roc_curve(
        self,
        y_trues: List[npt.NDArray],
        y_preds: List[npt.NDArray],
        labels: List[str],
        inputs: List[npt.NDArray],
        name: str,
        cv: int = 3,
    ) -> None:
        plt.figure(figsize=(8, 8))
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
        for y_true, y_pred, label, color, d in zip(
            y_trues, y_preds, labels, self.cmap, inputs
        ):
            aucs = []
            for _, indices in skf.split(y_pred, y_true):
                fpr, tpr, _ = roc_curve(y_true[indices], y_pred[indices])
                aucs.append(auc(fpr, tpr))
            std_auc = np.std(aucs)

            fpr, tpr, _ = roc_curve(y_true, y_pred)
            roc_auc = auc(fpr, tpr)
            fpr_base, tpr_base, _ = roc_curve(y_true, np.mean(d**2, axis=(1, 2)))

            plt.plot(
                fpr * 28.61,
                tpr,
                linestyle="-",
                lw=1.5,
                color=color,
                alpha=0.8,
                label=rf"{label} (AUC = {roc_auc: .4f} $\pm$ {std_auc: .4f})",
            )

            plt.plot(
                fpr_base * 28.61,
                tpr_base,
                linestyle="--",
                lw=1.0,
                color=color,
                alpha=0.5,
                label=rf"{label}, Baseline",
            )

        plt.plot(
            [0.003, 0.003],
            [0, 1],
            linestyle="--",
            lw=1,
            color="black",
            label="3 kHz",
        )
        plt.xlim([0.0001, 28.61])
        plt.ylim([0.01, 1.0])
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Trigger Rate (MHz)", size=15)
        plt.ylabel("Signal Efficiency", size=15)
        plt.legend(loc="best")
        plt.savefig(
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
        )
        plt.close()

    def plot_compilation_error(self, scores_keras, scores_hls4ml, name):
        plt.figure(figsize=(8, 8))
        plt.scatter(scores_keras, np.abs(scores_keras - scores_hls4ml), s=1)
        plt.xlabel("Anomaly Score, $S$", fontsize=18)
        plt.ylabel("Error, $|S_{Keras} - S_{hls4ml}|$", fontsize=18)
        plt.savefig(
            f"{self.output_dir}/compilation-error-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()

    def plot_compilation_error_distribution(self, scores_keras, scores_hls4ml, name):
        plt.hist(scores_keras - scores_hls4ml, fc="none", histtype="step", bins=100)
        plt.xlabel("Error, $S_{Keras} - S_{hls4ml}$", fontsize=18)
        plt.ylabel("Number of samples", fontsize=18)
        plt.yscale("log")
        plt.savefig(
            f"{self.output_dir}/compilation-error-dist-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )

    def plot_cpp_model(self, hls_model, name):
        hls4ml.utils.plot_model(
            hls_model,
            show_shapes=True,
            show_precision=True,
            to_file=f"{self.output_dir}/cpp-model-{self._parse_name(name)}.png",
        )

    def plot_roc_curve_comparison(self, scores_keras, scores_hls4ml, name):
        fpr_model, tpr_model = [], []

        scores_keras_normal = scores_keras["Background"]
        scores_hls4ml_normal = scores_hls4ml["Background"]

        for dataset_name, color in zip(list(scores_keras.keys())[:-1], self.cmap):
            scores_keras_anomaly = scores_keras[dataset_name]
            scores_hls4ml_anomaly = scores_hls4ml[dataset_name]

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
            f"{self.output_dir}/compilation-roc-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()
