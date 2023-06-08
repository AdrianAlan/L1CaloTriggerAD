import argparse
import numpy as np
import yaml

from generator import RegionETGenerator
from pathlib import Path
from plotting import Draw
from utils import IsValidFile
from typing import List, Optional


def dataset_profiling(datasets: dict, verbose: bool) -> None:
    draw = Draw(Path("plots"))
    generator = RegionETGenerator()
    deposits, labels = [], []
    for dataset in datasets:
        name = dataset["name"]
        labels.append(name)

        X = generator.get_background(dataset["path"])
        deposits.append(X)

        X_mean = np.mean(X, axis=0)
        pT = np.mean(X_mean)
        draw.plot_regional_deposits(X_mean.reshape(18, 14), pT, name)

        if verbose:
            print(f"{name} samples: {X.shape[0]}")

    draw.plot_deposits_distribution(
        deposits, labels, name="Zero Bias Energy Distribution"
    )


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
        "-v",
        "--verbose",
        action="store_true",
        help="Output verbosity",
        default=False,
    )
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))
    dataset_profiling(config["background"], args.verbose)


if __name__ == "__main__":
    main()
