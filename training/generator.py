import h5py
import numpy as np

from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow import data
from typing import List


class RegionETGenerator:
    def __init__(
        self, train_size: float = 0.5, val_size: float = 0.1, test_size: float = 0.4
    ):
        self.train_size = train_size
        self.val_size = val_size
        self.test_size = test_size
        self.random_state = 42

    def get_generator(
        self, X: np.array, y: np.array, batch_size: int, drop_reminder: bool = False
    ) -> data.Dataset:
        dataset = data.Dataset.from_tensor_slices((X, y))
        return (
            dataset.shuffle(1000)
            .cache()
            .batch(batch_size, drop_remainder=drop_reminder)
            .prefetch(data.AUTOTUNE)
        )

    def get_background(
        self, datasets_paths: List[Path], batch_size=128
    ) -> (np.array, np.array, np.array):
        X = []
        for dataset_path in datasets_paths:
            X.append(h5py.File(dataset_path, "r")["CaloRegions"][:].astype("float32"))
        X = np.concatenate(X)
        X = np.reshape(X, (-1, 18, 14, 1))

        X_train, X_test = train_test_split(
            X, test_size=self.test_size, random_state=self.random_state
        )
        X_train, X_val = train_test_split(
            X_train,
            test_size=self.val_size / (self.val_size + self.train_size),
            random_state=42,
        )

        return X_train, X_val, X_test

    def get_signal(
        self, dataset_paths: dict[str, Path], filter_acceptance=True
    ) -> dict[str, np.array]:
        signals = {}
        for signal_name, dataset_path in dataset_paths.items():
            X = h5py.File(dataset_path, "r")["CaloRegions"][:].astype("float32")
            X = np.reshape(X, (-1, 18, 14, 1))
            if filter_acceptance:
                flags = h5py.File(dataset_path, "r")["AcceptanceFlag"][:].astype("bool")
                fraction = np.round(100 * sum(flags) / len(flags), 2)
                print(f"Accepted {signal_name} events: {fraction}%")
                X = X[flags]
            signals[signal_name] = X
        return signals
