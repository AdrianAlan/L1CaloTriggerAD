import os
import torch
import torch.nn as nn
import torch.nn.functional as F


class DummyAutoencoder(nn.Module):

    def __init__(self):
        super(DummyAutoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(1, 10, kernel_size=3),
            nn.LeakyReLU(True),
            nn.BatchNorm2d(10),
            nn.MaxPool2d(2),
            nn.Conv2d(10, 20, kernel_size=3),
            nn.LeakyReLU(True),
            nn.BatchNorm2d(20)
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(20, 10, kernel_size=3),
            nn.LeakyReLU(True),
            nn.BatchNorm2d(10),
            nn.Upsample(scale_factor=2),
            nn.ConvTranspose2d(10, 1, kernel_size=3)
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def load_weights(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext in ['.pkl', '.pth']:
            state_dict = torch.load(file_path, map_location=lambda s, loc: s)
            self.load_state_dict(state_dict, strict=False)
        else:
            raise InvalidFile(file_path)


class InvalidFile(Exception):

    def __init__(self, file_path, message='Invalid file passed'):
        self.file_path = file_path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.file_path} -> {self.message}'
