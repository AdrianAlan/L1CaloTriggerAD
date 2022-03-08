import argparse
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
import yaml

from generator import L1UCTRegionsDataset
from models import DummyAutoencoder
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader
from tqdm import trange
from utils import AverageMeter, IsValidFile


def run_epoch(model,
              loader,
              criterion,
              optimizer,
              scaler=None,
              backprop=True,
              prefix='Training'):
    loss = AverageMeter('Loss', ':1.5f')
    loss.reset()
    with trange(len(loader), file=sys.stdout) as tr:
        for (inputs, labels) in loader:
            optimizer.zero_grad()
            if not backprop:
                outputs = model(inputs)
                batch_loss = criterion(outputs, inputs)
            else:
                with autocast():
                    outputs = model(inputs)
                    batch_loss = criterion(outputs, inputs)
                scaler.scale(batch_loss).backward()
                scaler.step(optimizer)
                scaler.update()
            loss.update(batch_loss.item(), labels.size(0))
            tr.set_description('{0}: {1}'.format(prefix, loss))
            tr.update(1)


def weights_init(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
        init.xavier_uniform_(m.weight.data)


def main(model_class,
         source_train,
         source_val,
         save_path,
         save_name,
         batch_size,
         weight_decay,
         epochs,
         learning_rate,
         momentum):
    device = torch.device('cuda:0')

    X_train = DataLoader(
        L1UCTRegionsDataset(source_train, device),
        batch_size=batch_size,
        num_workers=0,
        shuffle=True)

    X_val = DataLoader(
        L1UCTRegionsDataset(source_train, device),
        batch_size=batch_size,
        num_workers=0,
        shuffle=False)

    # Initialize the model
    model = eval(model_class)().to(device)
    model.encoder.apply(weights_init)
    model.decoder.apply(weights_init)
    print(model)

    # Set optimization details
    optimizer = optim.SGD(
        model.parameters(),
        lr=learning_rate,
        momentum=momentum,
        weight_decay=weight_decay
    )

    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)
    criterion = nn.MSELoss().to(device)
    scaler = GradScaler()
    net = torch.nn.DataParallel(model)

    for epoch in range(epochs):
        print('Epoch {0}'.format(epoch + 1))

        model.train()
        run_epoch(net,
                  X_train,
                  criterion,
                  optimizer,
                  scaler=scaler)

        model.eval()
        run_epoch(net,
                  X_val,
                  criterion,
                  optimizer,
                  backprop=False,
                  prefix='Validation')

        torch.save(
            model.state_dict(),
            '{0}/{1}.pth'.format(save_path, save_name)
        )
        scheduler.step()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        """Train the dummy L1UCTRegions autoencoder for anomaly detection"""
    )

    parser.add_argument('config',
                        action=IsValidFile,
                        help='Model config file',
                        type=str)

    parser.add_argument('--batch-size',
                        default=25,
                        dest='batch_size',
                        help='Number of training samples in a batch',
                        type=int)

    parser.add_argument('--decay',
                        default=5e-4,
                        dest='weight_decay',
                        help='SGD weight decay',
                        type=float)

    parser.add_argument('--epochs',
                        default=50,
                        dest='epochs',
                        help='Set number of training epochs',
                        type=int)

    parser.add_argument('--lr',
                        default=0.001,
                        dest='learning_rate',
                        help='Set learning rate',
                        type=float)

    parser.add_argument('--momentum',
                        default=0.9,
                        dest='momentum',
                        help='SGD momentum',
                        type=float)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))

    if not os.path.isdir(config['output']['models']):
        os.mkdir(config['output']['models'])

    main(config['model']['class_name'],
         config['dataset']['train'],
         config['dataset']['validation'],
         config['output']['models'],
         config['output']['name'],
         args.batch_size,
         args.weight_decay,
         args.epochs,
         args.learning_rate,
         args.momentum)
