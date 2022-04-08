import argparse
import awkward as ak
import numpy as np
import os
import h5py
import uproot

from dataclasses import dataclass
from tqdm import tqdm
from utils import IsReadableDir


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
    caloET: ak.highlevel.Array = ak.Array([])
    caloEta: ak.highlevel.Array = ak.Array([])
    caloPhi: ak.highlevel.Array = ak.Array([])
    acceptanceFlag: ak.highlevel.Array = ak.Array([])
    _calo_vars = ['iet', 'ieta', 'iphi']
    _acceptance_vars = ['jetEta', 'jetPt']

    def __init__(self, path, tree_calo, tree_gen, span):
        self.root_files = [i for i in os.listdir(path) if i.endswith(".root")]
        self.path = path
        self.tree_calo = tree_calo
        self.tree_gen = tree_gen
        iets, ietas, iphis, flags = (), (), (), ()
        n_files = len(self.root_files)
        with tqdm(total=n_files, desc='Processing files') as progress_bar:
            for root_file in self.root_files:
                in_file = uproot.open('{}{}'.format(self.path, root_file))
                # Process Calo Information
                tree_calo = in_file[self.tree_calo]
                arrays = tree_calo.arrays(self._calo_vars)
                iet = arrays['iet']
                ieta = arrays['ieta']
                iphi = arrays['iphi']
                mask = (ieta > span[0]) & (ieta <= span[1])
                iet, ieta, iphi = iet[mask], ieta[mask], iphi[mask]
                iets += (iet,)
                ietas += (ieta,)
                iphis += (iphi,)

                # Process Generator Information
                tree_gen = in_file[self.tree_gen]
                arrays = tree_gen.arrays(self._acceptance_vars)
                jetPT = arrays['jetPt']
                jetEta = arrays['jetEta']
                mask = (jetPT > 30.) & (abs(jetEta) < 2.4)
                flags += (ak.any(mask, axis=-1),)

                progress_bar.update(1)

        self.caloET = ak.concatenate(iets)
        self.caloEta = ak.concatenate(ietas)
        self.caloPhi = ak.concatenate(iphis)
        self.acceptanceFlag = ak.concatenate(flags)

    def __len__(self):
        return len(self.caloET)


def create_dataset(hdf5_dataset, name, data):
    return hdf5_dataset.create_dataset(
        name=name,
        data=data,
        compression='gzip',
        dtype='i')


def get_split_events_range(events, split=[0.6, 0.2, 0.2]):
    split = np.array(split)
    cumsum = np.cumsum(events*split).astype(int)
    cumsum = np.arange(1, 21)/100*5*events.astype(int)
    return [i for i in zip(np.array([0, *cumsum]), cumsum)]


def main(input_path, output_file, name_tree_calo, name_tree_gen, split=True):
    edges_eta = Grid((-28, 28), 14, 0)
    edges_phi = Grid((0, 72), 18, -2)
    source = DataSource(input_path,
                        name_tree_calo,
                        name_tree_gen,
                        edges_eta.span)
    events = len(source)
    with tqdm(total=len(source), desc='Processing events') as progress_bar:
        placeholder = np.zeros((events, 18, 14))
        for i in range(events):
            # Get raw data
            eta = ak.to_numpy(source.caloEta[i])
            phi = ak.to_numpy(source.caloPhi[i])
            et = ak.to_numpy(source.caloET[i])

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

    flags = ak.to_numpy(source.acceptanceFlag)

    if split:
        for i, (emin, emax) in enumerate(get_split_events_range(events)):
            output = '{}_{}.h5'.format(output_file.split('.')[0], i)
            with h5py.File(output, 'w') as dataset:
                create_dataset(dataset, 'CaloRegions', placeholder[emin:emax])
                create_dataset(dataset, 'AcceptanceFlag', flags[emin:emax])
    else:
        with h5py.File(output_file, 'w') as dataset:
            create_dataset(dataset, 'CaloRegions', placeholder)
            create_dataset(dataset, 'AcceptanceFlag', flags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        '''Converts CMS Calorimeter Layer-1 Trigger with UCTRegions data from
           ROOT format to HDF5''')

    parser.add_argument('filepath',
                        action=IsReadableDir,
                        help='Input ROOT file',
                        type=str)

    parser.add_argument('savepath',
                        help='Output HDF5 files prefix',
                        type=str)

    parser.add_argument('--tree-calo',
                        type=str,
                        default='l1CaloTowerEmuTree/L1CaloTowerTree',
                        help='Data tree')

    parser.add_argument('--tree-generator',
                        type=str,
                        default='l1GeneratorTree/L1GenTree/Generator',
                        help='Data tree')

    parser.add_argument('--split',
                        action='store_true',
                        help='Split the dataset?')

    args = parser.parse_args()

    main(args.filepath,
         args.savepath,
         args.tree_calo,
         args.tree_generator,
         args.split)
