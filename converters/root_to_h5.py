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
    em: ak.highlevel.Array
    acceptanceFlag: ak.highlevel.Array
    size: int
    _calo_vars = ['iet', 'ieta', 'iphi', 'iem']
    _acceptance_vars = ['jetEta', 'jetPt']

    def __init__(self, input_file, tree_name, tree_gen=False):
        with uproot.open(input_file) as in_file:
            tree = in_file[tree_name]
            arrays = tree.arrays(self._calo_vars)
            eta = arrays['ieta']
            phi = arrays['iphi']
            et = arrays['iet']
            em = arrays['iem']
            self.size = len(eta)

            mask = (eta >= -28) & (eta <= 28)
            eta, phi, et, em = eta[mask], phi[mask], et[mask], em[mask]
            eta = ak.where(eta < 0, eta, eta - 1)
            eta = eta + 28
            phi = (phi + 2) % 72

            ids = np.arange(len(eta))
            self.ids = ak.flatten(ak.broadcast_arrays(ids, eta)[0])
            self.phi = ak.flatten(phi, None)
            self.eta = ak.flatten(eta, None)
            self.et = ak.flatten(et, None)
            self.em = ak.flatten(em, None)

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


@dataclass
class ExtraBits:
    egVeto: ak.highlevel.Array
    tauVeto: ak.highlevel.Array

    def __init__(self, deposits, region_et, region_ecal_et):
        activityFraction = 0.125
        miscActivityFraction = 0.25

        # Calculate tau and electron bits
        # Translated from https://github.com/pallabidas/cmssw/blob/l1t-integration-test-07Jul/L1Trigger/L1TCaloLayer1/src/UCTRegion.cc

        # Calculate treshold values per region L 133
        activityLevel = (region_et * activityFraction).astype(int)
        # Expand to the size of the detetor L137
        activityLevelUpDim = np.repeat(
            np.repeat(activityLevel, 4, axis=1), 4, axis=2
        )
        # Get the active tower information L139
        activeTower = deposits > activityLevelUpDim
        activeTowerET = block_reduce(activeTower * deposits, (1, 4, 4), np.sum)
        # Calculate active stips
        activeTowerEta = block_reduce(activeTower, (1, 1, 4), np.any)
        activeTowerPhi = block_reduce(activeTower, (1, 4, 1), np.any)
        # Calculate veto bits for eg and tau patterns
        veto_eta = block_reduce(activeTowerEta, (1, 4, 1), self.veto_bit_eta)
        veto_phi = block_reduce(activeTowerPhi, (1, 1, 4), self.veto_bit_phi)
        veto = veto_eta & veto_phi
        # L192
        maxMiscActivity = (region_et * miscActivityFraction).astype(int)
        self.egVeto = veto | ((region_et - region_ecal_et) > maxMiscActivity)
        self.tauVeto = veto | ((region_et - activeTowerET) > maxMiscActivity)

    def veto_bit_eta(self, pattern, axis=None):
        output = np.zeros(pattern.shape[:3]).astype(bool)
        bad_patterns = [[0, 1, 0, 1],
                        [0, 1, 1, 1],
                        [1, 0, 0, 1],
                        [1, 0, 1, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 0],
                        [1, 1, 1, 1]]
        for bad_pattern in bad_patterns:
            match = pattern == np.array(bad_pattern).reshape(1, 4, 1)
            match = match.all(axis=(axis))
            output |= match
        return ~output

    def veto_bit_phi(self, pattern, axis=None):
        output = np.zeros(pattern.shape[:3]).astype(bool)
        bad_patterns = [[0, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 0, 1, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1]]
        for bad_pattern in bad_patterns:
            match = pattern == np.array(bad_pattern).reshape(1, 1, 4)
            match = match.all(axis=(axis))
            output |= match
        return ~output


def get_split(events, split=[0.6, 0.2, 0.2]):
    split = [0] + split
    split = np.array(split)
    cumsum = np.cumsum(events*split).astype(int)
    return [(i, j) for i, j in zip(cumsum, cumsum[1:])]


def main(input_dir, savepath, tree_calo, tree_generator, split):
    create = True
    for input_file in absoluteFilePaths(input_dir):

        print("Processing {}".format(input_file.split('/')[-1]))

        source = DataSource(input_file, tree_calo, tree_generator)
        events = len(source)
        deposits = np.zeros((events, 72, 56))
        deposits_ecal = np.zeros((events, 72, 56))

        # Get raw data
        ids = source.ids.to_numpy()
        phi = source.phi.to_numpy()
        eta = source.eta.to_numpy()
        et = source.et.to_numpy()
        em = source.em.to_numpy()

        if tree_generator:
            flags = source.acceptanceFlag.to_numpy()
        del source

        # Calculate regional deposits
        deposits[ids, phi, eta] = et
        deposits_ecal[ids, phi, eta] = em

        # Reduce to towers
        region_et = block_reduce(deposits, (1, 4, 4), np.sum)
        region_et = np.where(region_et > 1023, 1023, region_et)
        region_ecal_et = block_reduce(deposits_ecal, (1, 4, 4), np.sum)
        region_ecal_et = np.where(region_ecal_et > 1023, 1023, region_ecal_et)

        source = ExtraBits(deposits, region_et, region_ecal_et)
        egVeto = source.egVeto
        tauVeto = source.tauVeto
        del source
        del deposits
        del deposits_ecal
        del region_ecal_et

        with h5py.File(savepath, 'a') as h5f:
            if create:
                h5f.create_dataset(
                    'CaloRegions',
                    data=region_et,
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                h5f.create_dataset(
                    'ElectronBit',
                    data=egVeto,
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                h5f.create_dataset(
                    'TauBit',
                    data=tauVeto,
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
            h5f["EGBit"].resize((size), axis=0)
            h5f["TauBit"].resize((size), axis=0)
            h5f["CaloRegions"][-region_et.shape[0]:] = region_et
            h5f["EGBit"][-region_et.shape[0]:] = egVeto
            h5f["TauBit"][-region_et.shape[0]:] = tauVeto
            if tree_generator:
                h5f["AcceptanceFlag"].resize((size), axis=0)
                h5f["AcceptanceFlag"][-flags.shape[0]:] = flags

    if split:
        with h5py.File(savepath, 'r') as h5f_in:
            cr = h5f_in["CaloRegions"]
            if tree_generator:
                fs = h5f_in["AcceptanceFlag"]
            for i, (s, e) in enumerate(get_split(cr.shape[0])):
                output = '{}_{}.h5'.format(savepath.split('.')[0], i)
                with h5py.File(output, 'w') as h5f_out:
                    h5f_out.create_dataset('CaloRegions', data=cr[s:e])
                    if tree_generator:
                        h5f_out.create_dataset('AcceptanceFlag', data=fs[s:e])


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

    parser.add_argument('--split',
                        action='store_true',
                        help='Store acceptance flag')

    args = parser.parse_args()

    if args.store_acceptance:
        gen = 'l1GeneratorTree/L1GenTree/Generator'
    else:
        gen = False

    main(args.filepath, args.savepath, args.tree_calo, gen, args.split)
