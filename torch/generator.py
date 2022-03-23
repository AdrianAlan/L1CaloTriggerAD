import h5py
import torch


class L1UCTRegionsDataset(torch.utils.data.Dataset):

    def __init__(self,
                 source,
                 device,
                 flatten=False,
                 flip_prob=None,
                 normalize=False,
                 standardize=True,
                 signal=False):
        """Generator for CMS Calorimeter Layer-1 Trigger with UCTRegions"""
        self.source = source
        self.device = device
        self.flatten = flatten
        self.flip_prob = flip_prob
        self.normalize = normalize
        self.standardize = standardize
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

        if self.flatten:
            bins = calorimeter.nonzero()
            eta, phi = bins[:, 2], bins[:, 1]
            et = calorimeter.squeeze()[phi, eta]
            order = torch.argsort(et, descending=True)
            eta, phi, et = eta[order], phi[order], et[order]
            c = torch.vstack((eta/14., phi/18., et))
            target = torch.zeros(3, 252)
            target[:, :c.shape[1]] = c
            return target.T, labels

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
