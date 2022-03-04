import argparse
import awkward as ak
import numpy as np
import h5py
import uproot

from dataclasses import dataclass
from tqdm import tqdm
from utils import IsValidFile


@dataclass(frozen=True)
class Grid:
    span: dict
    steps: int
    offset: int
    epsilon: float = 0.00001

    def __post_init__(self):
        bins = (1 + self.epsilon) * np.linspace(self.span[0] + self.offset,
                                                self.span[1] + self.offset,
                                                self.steps + 1)
        object.__setattr__(self, 'bins', bins)


@dataclass
class DataSource:
    eta: ak.highlevel.Array
    phi: ak.highlevel.Array
    et: ak.highlevel.Array
    _vars = ['ieta', 'iphi', 'iet']

    def __init__(self, input_file, tree_name):
        in_file = uproot.open(input_file)
        tree = in_file[tree_name]
        arrays = tree.arrays(self._vars)
        self.eta = arrays['ieta']
        self.phi = arrays['iphi']
        self.et = arrays['iet']

    def __len__(self):
        return len(self.eta)


def create_dataset(hdf5_dataset, name, data):
    return hdf5_dataset.create_dataset(
        name=name,
        data=data,
        compression='gzip',
        dtype='i')


def main(input_file, output_file, tree_name):
    source = DataSource(input_file, tree_name)
    edges_eta = Grid((-28, 28), 14, 0)
    edges_phi = Grid((0, 72), 18, -2)

    events = len(source)
    placeholder = np.zeros((events, 18, 14))

    with tqdm(total=len(source), desc='Processing events') as progress_bar:
        for i in range(events):
            # Get raw data
            eta = ak.to_numpy(source.eta[i])
            phi = ak.to_numpy(source.phi[i])
            et = ak.to_numpy(source.et[i])

            # Mask eta
            mask = (eta > edges_eta.span[0]) & (eta <= edges_eta.span[1])
            eta, phi, et = eta[mask], phi[mask], et[mask]

            # Hack for phi (72, 71 to match phi=0)
            phi = phi % 70

            # Convert towers to regions
            regions, _, _ = np.histogram2d(phi,
                                           eta,
                                           bins=[edges_phi.bins,
                                                 edges_eta.bins],
                                           weights=et)
            placeholder[i, :, :] = regions
            progress_bar.update(1)

    with h5py.File(output_file, 'w') as dataset:
        create_dataset(dataset, 'CaloRegions', placeholder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        '''Converts CMS Calorimeter Layer-1 Trigger with UCTRegions data from
           ROOT format to HDF5''')

    parser.add_argument('filepath',
                        action=IsValidFile,
                        help='Input ROOT file',
                        type=str)

    parser.add_argument('savepath',
                        help='Output HDF5 files prefix',
                        type=str)

    parser.add_argument('--tree',
                        type=str,
                        default='l1CaloTowerEmuTree/L1CaloTowerTree',
                        help='Data tree')

    args = parser.parse_args()

    main(args.filepath, args.savepath, args.tree)
