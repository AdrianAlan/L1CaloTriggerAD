import argparse
import awkward as ak
import h5py
import numpy as np
import uproot

from dataclasses import dataclass
from skimage.measure import block_reduce
from utils import IsReadableDir, absoluteFilePaths


@dataclass
class DataSource:
    ids: ak.highlevel.Array
    phi: ak.highlevel.Array
    eta: ak.highlevel.Array
    et: ak.highlevel.Array
    size: int
    _vars = ['ieta', 'iphi', 'iet']

    def __init__(self, input_file, tree_name):
        in_file = uproot.open(input_file)
        tree = in_file[tree_name]
        arrays = tree.arrays(self._vars)
        eta = arrays['ieta']
        phi = arrays['iphi']
        et = arrays['iet']
        self.size = len(eta)

        mask = (eta >= -28) & (eta <= 28)
        eta, phi, et = eta[mask], phi[mask], et[mask]
        eta = ak.where(eta < 0, eta, eta - 1)
        eta = eta + 28
        phi = (phi + 2) % 72

        ids = np.arange(len(eta))
        self.ids = ak.flatten(ak.broadcast_arrays(ids, eta)[0])
        self.phi = ak.flatten(phi, None)
        self.eta = ak.flatten(eta, None)
        self.et = ak.flatten(et, None)

    def __len__(self):
        return self.size


def create_dataset(hdf5_dataset, name, data):
    return hdf5_dataset.create_dataset(
        name=name,
        data=data,
        compression='gzip',
        dtype='i')


def main(input_dir, output_dir, tree_name):
    for input_file in absoluteFilePaths(input_dir):
        print("Processing {}".format(input_file.split('/')[-1]))

        source = DataSource(input_file, tree_name)
        events = len(source)
        deposits = np.zeros((events, 72, 56))

        # Get raw data
        ids = source.ids.to_numpy()
        phi = source.phi.to_numpy()
        eta = source.eta.to_numpy()
        et = source.et.to_numpy()

        deposits[ids, phi, eta] = et
        deposits = block_reduce(deposits, (1, 4, 4), np.sum)

        del source
        output_file = '{}/{}.h5'.format(output_dir, input_file.split('/')[-1])
        with h5py.File(output_file, 'w') as dataset:
            create_dataset(dataset, 'CaloRegions', deposits)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        '''Converts CMS Calorimeter Layer-1 Trigger with UCTRegions data from
           ROOT format to HDF5''')

    parser.add_argument('filepath',
                        action=IsReadableDir,
                        help='Input ROOT directory',
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
