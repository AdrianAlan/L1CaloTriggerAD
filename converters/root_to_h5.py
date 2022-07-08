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
    acceptanceFlag: ak.highlevel.Array
    size: int
    _calo_vars = ['iet', 'ieta', 'iphi']
    _acceptance_vars = ['jetEta', 'jetPt']

    def __init__(self, input_file, tree_name, tree_gen=False):
        in_file = uproot.open(input_file)
        tree = in_file[tree_name]
        arrays = tree.arrays(self._calo_vars)
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

        if tree_gen:
            # Process Generator Information
            tree_gen = in_file[tree_gen]
            arrays = tree_gen.arrays(self._acceptance_vars)
            jetPT = arrays['jetPt']
            jetEta = arrays['jetEta']
            mask = (jetPT > 30.) & (abs(jetEta) < 2.4)
            self.acceptanceFlag = ak.any(mask, axis=-1)

    def __len__(self):
        return self.size


def create_dataset(hdf5_dataset, name, data):
    return hdf5_dataset.create_dataset(
        name=name,
        data=data,
        compression='gzip',
        dtype='i')


def main(input_dir, savepath, tree_name):
    create = True
    for input_file in absoluteFilePaths(input_dir):

        print("Processing {}".format(input_file.split('/')[-1]))

        source = DataSource(input_file, tree_calo, tree_generator)
        events = len(source)
        deposits = np.zeros((events, 72, 56))

        # Get raw data
        ids = source.ids.to_numpy()
        phi = source.phi.to_numpy()
        eta = source.eta.to_numpy()
        et = source.et.to_numpy()
        if tree_generator:
            flags = source.acceptanceFlag.to_numpy()
        del source

        # Calculate regional deposits
        deposits[ids, phi, eta] = et
        region_et = block_reduce(deposits, (1, 4, 4), np.sum)

        with h5py.File(savepath, 'a') as h5f:
            if create:
                h5f.create_dataset(
                    'CaloRegions',
                    data=region_et,
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                if tree_generator:
                    h5f.create_dataset(
                        'AcceptanceFlag',
                        data=flags,
                        maxshape=(None,),
                        chunks=True
                    )
                create = False
                continue

            size = h5f["CaloRegions"].shape[0] + region_et.shape[0]
            h5f["CaloRegions"].resize((size), axis=0)
            h5f["CaloRegions"][-region_et.shape[0]:] = region_et
            if tree_generator:
                h5f["AcceptanceFlag"].resize((size), axis=0)
                h5f["AcceptanceFlag"][-flags.shape[0]:] = flags


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

    parser.add_argument('--tree-calo',
                        type=str,
                        default='l1CaloTowerEmuTree/L1CaloTowerTree',
                        help='Data tree')

    parser.add_argument('--store-acceptance',
                        action='store_true',
                        help='Store acceptance flag')

    args = parser.parse_args()

    if args.store_acceptance:
        gen = 'l1GeneratorTree/L1GenTree/Generator'
    else:
        gen = False

    main(args.filepath, args.savepath, args.tree)
