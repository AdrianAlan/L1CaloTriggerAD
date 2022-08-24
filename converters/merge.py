import argparse
import h5py
import numpy as np
from utils import absoluteFilePaths, IsReadableDir 


def main(in_dir, savepath):

    with h5py.File(savepath, 'a') as h5f:
        for x, f in enumerate(absoluteFilePaths(in_dir, 'h5')):
            print(f)

            with h5py.File(f, 'r') as h5f_in:
                cr = h5f_in["CaloRegions"][:]
                eb = h5f_in["ElectronBit"][:]
                tb = h5f_in["TauBit"][:]
                #fs = h5f_in["AcceptanceFlag"][:]
       
            if x:
                size = h5f["CaloRegions"].shape[0] + cr.shape[0]
                h5f["CaloRegions"].resize((size), axis=0)
                h5f["ElectronBit"].resize((size), axis=0)
                h5f["TauBit"].resize((size), axis=0)
                #h5f["AcceptanceFlag"].resize((size), axis=0)

                h5f["CaloRegions"][-cr.shape[0]:] = cr
                h5f["ElectronBit"][-cr.shape[0]:] = eb
                h5f["TauBit"][-cr.shape[0]:] = tb
                #h5f["AcceptanceFlag"][-cr.shape[0]:] = fs
            else:
                h5f.create_dataset(
                    'CaloRegions',
                    data=cr[:],
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                h5f.create_dataset(
                    'ElectronBit',
                    data=eb[:],
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                h5f.create_dataset(
                    'TauBit',
                    data=tb[:],
                    maxshape=(None, 18, 14),
                    chunks=True
                )
                #h5f.create_dataset(
                #        'AcceptanceFlag',
                #        data=fs[:],
                #        maxshape=(None,),
                #        chunks=True
                #    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Merge HDF5 files')

    parser.add_argument('in_directory',
                        action=IsReadableDir,
                        help='Input directory with HDF5 files',
                        type=str)

    parser.add_argument('savepath',
                        help='Output HDF5',
                        type=str)

    args = parser.parse_args()

    main(args.in_directory, args.savepath)
