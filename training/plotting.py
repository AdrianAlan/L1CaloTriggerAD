import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import random

from pathlib import Path
from sklearn.metrics import roc_curve, auc
from typing import List


class Draw:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        random.seed(42)

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
        plt.figure(figsize=(7, 9))
        im = plt.imshow(
            deposits.reshape(18, 14), vmin=0, vmax=deposits.max(), cmap="Purples"
        )
        ax = plt.gca()
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(r"E$_T$ (GeV)", rotation=-90, va="bottom")
        plt.axis("off")
        plt.title(rf"Mean E$_T$ {mean: .2f} ({name})")
        plt.savefig(
            f"{self.output_dir}/mean-deposits-{self._parse_name(name)}.png",
            bbox_inches="tight",
        )
        plt.close()

    def plot_deposits_distribution(
        self, deposits: List[npt.NDArray], labels: List[str], name: str
    ) -> None:
        plt.figure(figsize=(15, 10))
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
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
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
        name: str,
        cv: int = 5,
    ) -> None:
        colors = ["green", "red", "blue", "orange", "purple"]
        plt.figure(figsize=(13, 13))
        for y_true, y_pred, label, color in zip(y_trues, y_preds, labels, colors):
            merged = list(zip(y_true, y_pred))
            random.shuffle(merged)
            y_true, y_pred = list(zip(*merged))

            tprs, aucs = [], []
            mean_fpr = np.linspace(0, 1, 100)
            for y_true_cv, y_pred_cv in zip(
                np.array_split(y_true, cv), np.array_split(y_pred, cv)
            ):
                fpr, tpr, _ = roc_curve(y_true_cv, y_pred_cv)
                roc_auc = auc(fpr, tpr)
                interp_tpr = np.interp(mean_fpr, fpr, tpr)
                interp_tpr[0] = 0.0
                tprs.append(interp_tpr)
                aucs.append(roc_auc)

            mean_tpr = np.mean(tprs, axis=0)
            mean_tpr[-1] = 1.0
            mean_auc = auc(mean_fpr, mean_tpr)
            std_auc = np.std(aucs)

            mean_fpr *= 28.61  # Convert to trigger rate
            plt.plot(
                mean_fpr,
                mean_tpr,
                linestyle="-",
                lw=1.5,
                color=color,
                alpha=0.8,
                label=rf"{label} (AUC = {mean_auc: .4f} $\pm$ {std_auc: .4f})",
            )

            std_tpr = np.std(tprs, axis=0)
            tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
            tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
            plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color=color, alpha=0.1)

        plt.plot(
            [0.003, 0.003],
            [0, 1],
            linestyle="--",
            lw=1,
            color="black",
            label="3 kHz",
        )
        plt.xlim([0.00001, 28.61])
        plt.ylim([0.00001, 1.0])
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Trigger Rate (MHz)", size=15)
        plt.ylabel("Signal Efficiency", size=15)
        plt.legend(loc="best")
        plt.savefig(
            f"{self.output_dir}/{self._parse_name(name)}.png", bbox_inches="tight"
        )
        plt.close()
