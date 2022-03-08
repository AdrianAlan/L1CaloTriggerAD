import argparse
import torch
import matplotlib.pyplot as plt
import yaml

from sklearn.metrics import roc_curve, auc
from generator import L1UCTRegionsDataset
from models import DummyAutoencoder
from torch.utils.data import DataLoader
from utils import IsValidFile, to_numpy


def main(model_class,
         source_background,
         source_signals,
         model_path,
         model_name,
         plot_path,
         plot_style,
         batch_size):

    device = torch.device('cuda:0')
    plt.style.use(plot_style)

    # Load the model
    model = eval(model_class)().to(device)
    model.load_weights('{0}/{1}.pth'.format(model_path, model_name))

    # Chose your metric
    metric = torch.nn.MSELoss(reduction='none')

    # Load the datasets: background
    background = DataLoader(
        L1UCTRegionsDataset(source_background, device),
        batch_size=batch_size,
        num_workers=0,
        shuffle=False)

    # Gather statistics and plot
    y_true, y_score = torch.empty(0).to(device), torch.empty(0).to(device)

    for X, y in background:
        y = y.to(device)
        distance = metric(model(X), X).mean(3).mean(2).mean(1)
        y_true = torch.cat((y_true, y), 0)
        y_score = torch.cat((y_score, distance), 0)

    plt.figure()

    for signal in source_signals:
        benchmark = DataLoader(
            L1UCTRegionsDataset(signal['path'], device, signal=True),
            batch_size=batch_size,
            num_workers=0,
            shuffle=False
        )

        y_true_signal = torch.empty(0).to(device)
        y_score_signal = torch.empty(0).to(device)

        for X, y in benchmark:
            y = y.to(device)
            distance = metric(model(X), X).mean(3).mean(2).mean(1)
            y_true_signal = torch.cat((y_true_signal, y), 0)
            y_score_signal = torch.cat((y_score_signal, distance), 0)

        fpr, tpr, _ = roc_curve(
            to_numpy(torch.cat((y_true, y_true_signal))),
            to_numpy(torch.cat((y_score, y_score_signal)))
        )

        roc_auc = auc(fpr, tpr)

        label = '[{0:0.3f}] {1}'.format(roc_auc, signal['name'])

        plt.plot(fpr, tpr, label=label)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel("False Positive Rate", horizontalalignment='right', x=1.0)
    plt.ylabel("True Positive Rate", horizontalalignment='right', y=1.0)
    plt.title("ROC Curve: {0}".format(type(model).__name__))
    plt.legend(bbox_to_anchor=(1., 1.))
    plt.savefig('{0}/ROC-{1}'.format(plot_path, model_name))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        """Train the dummy L1UCTRegions autoencoder for anomaly detection"""
    )

    parser.add_argument('config',
                        action=IsValidFile,
                        help='Model config file',
                        type=str)

    parser.add_argument('--batch-size',
                        default=100,
                        dest='batch_size',
                        help='Number of training samples in a batch',
                        type=int)

    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))

    main(config['model']['class_name'],
         config['dataset']['test_background'],
         config['dataset']['test_signal'],
         config['output']['models'],
         config['output']['name'],
         config['output']['plots'],
         config['misc']['plot_style'],
         args.batch_size)
