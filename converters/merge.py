import argparse
import h5py
import numpy as np

from tqdm import tqdm
from utils import absoluteFilePaths, IsReadableDir 


def main(in_dir, savepath):

    with h5py.File(savepath, 'a') as h5f:
        for x, f in enumerate(absoluteFilePaths(in_dir, 'h5')):
            data = h5py.File(f, 'r')['CaloRegions'][:]
            if x:
                size = h5f["CaloRegions"].shape[0] + data.shape[0]
                h5f["CaloRegions"].resize((size), axis=0)
                h5f["CaloRegions"][-data.shape[0]:] = data
            else:
                h5f.create_dataset(
                    'CaloRegions',
                    data=data,
                    maxshape=(None, 18, 14),
                    chunks=True
                )

 
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
