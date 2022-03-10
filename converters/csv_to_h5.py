import argparse
import h5py
import numpy as np
import os
import pandas as pd
import yaml

from tqdm import tqdm
from utils import IsValidFile


def get_size(csv_file):
    with open(csv_file, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
        num_of_events = last_line.split(',')[0]
        num_of_events = int(num_of_events) + 1
        return num_of_events


def create_dataset(hdf5_dataset, name, data):
    return hdf5_dataset.create_dataset(
        name=name,
        data=data,
        compression='gzip',
        dtype='i')


def main(filepath, savepath, dataset_split, chunksize, events):
    if not events:
        events = get_size(filepath)
    events_per_file = events*np.array(dataset_split)
    events_per_file = events_per_file.astype(int)
    chunks = pd.read_csv(filepath, chunksize=chunksize)

    with tqdm(total=events, desc='Processing events') as progress_bar:
        for suffix, epf in enumerate(events_per_file):
            placeholder = np.zeros((epf, 18, 14))
            for i in range(epf):
                chunk = next(chunks)
                eta = chunk.eta.values
                phi = chunk.phi.values
                et = chunk.et.values
                placeholder[i, phi, eta] = et
                progress_bar.update(1)

            savepath_suffix = '{}_{}.h5'.format(savepath, suffix)
            with h5py.File(savepath_suffix, 'w') as dataset:
                create_dataset(dataset, 'CaloRegions', placeholder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        '''Converts CMS Calorimeter Layer-1 Trigger with UCTRegions data from
           CSV format to HDF5''')

    parser.add_argument('filepath',
                        action=IsValidFile,
                        help='Input CSV file',
                        type=str)

    parser.add_argument('savepath',
                        help='Output HDF5 files prefix',
                        type=str)

    parser.add_argument('config',
                        action=IsValidFile,
                        type=str,
                        help='Path to config file')

    parser.add_argument('-s',
                        default=252,
                        dest='chunksize',
                        help='Chunksize for CSV reader',
                        type=int)

    parser.add_argument('-e',
                        default=None,
                        dest='events',
                        help='Number of events in the file',
                        type=int)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))
    dataset_split = config['dataset_split']

    main(args.filepath,
         args.savepath,
         dataset_split,
         args.chunksize,
         args.events)
