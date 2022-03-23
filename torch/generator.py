import h5py
import torch


class L1UCTRegionsDataset(torch.utils.data.Dataset):

    def __init__(self,
                 source,
                 device,
                 flip_prob=0.,
                 normalize=False,
                 standardize=True,
                 signal=False):
        """Generator for CMS Calorimeter Layer-1 Trigger with UCTRegions"""
        self.source = source
        self.device = device
        self.normalize = normalize
        self.standardize = standardize
        self.flip_prob = flip_prob
        self.label = int(signal)

    def __getitem__(self, index):
        if not hasattr(self, 'calo_regions'):
            self.open_hdf5()

        labels = self.get_labels()
        calorimeter = torch.unsqueeze(self.calo_regions[index], 0)

        if self.standardize:
            calorimeter = self._standardize(calorimeter,
                                            self.standardize)
        elif self.normalize:
            calorimeter = self._normalize(calorimeter,
                                          self.normalize)

        if self.flip_prob:
            if torch.rand(1) < self.flip_prob:
                calorimeter = self.flip_image(calorimeter, horizontal=True)
            if torch.rand(1) < self.flip_prob:
                calorimeter = self.flip_image(calorimeter, horizontal=False)

        return calorimeter, labels

    def __len__(self):
        if not hasattr(self, 'calo_regions'):
            self.open_hdf5()
        return self.dataset_size

    def flip_image(self, image, horizontal=True):
        axis = horizontal + 1
        image = torch.flip(image, [axis])
        return image

    def _normalize(self, t, data):
        m = torch.max(t) if isinstance(data, bool) else data
        return t.div(m) if m else t

    def _standardize(self, t, data):
        if isinstance(data, bool):
            m, s = torch.mean(t), torch.std(t)
        else:
            m, s = data
        return t.sub(m).div(s) if s else t

    def open_hdf5(self):
        self.hdf5_dataset = h5py.File(self.source, 'r')
        self.calo_regions = self.hdf5_dataset['CaloRegions']
        self.calo_regions = torch.from_numpy(self.calo_regions[:])
        self.calo_regions = self.calo_regions.to(self.device)
        self.calo_regions = self.calo_regions.float()
        self.dataset_size = len(self.calo_regions)

    def get_labels(self):
        return self.label
