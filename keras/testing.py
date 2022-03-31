import argparse
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sys
import yaml

from generator import get_generator
from sklearn.metrics import roc_curve, auc
from utils import IsValidFile
from tqdm import trange


def score(truth, predictions):
    truth = truth.reshape(predictions.shape)
    score = np.sum(np.sum(np.sum((np.abs(truth) - np.abs(predictions)), 3), 2), 1) / 252
    return score


def main(model_class,
         source_background,
         source_signals,
         model_path,
         model_name,
         plot_path,
         settings,
         plot_style,
         max_events):

    plt.style.use(plot_style)

    # Load the model
    model = tf.keras.models.load_model('{0}/{1}'.format(model_path, model_name))

    # Gather statistics and plot
    y_trues, y_scores = [], []

    # Load the datasets: background
    background = get_generator(source_background, 1, **settings)
    scores_background = []
    with trange(max_events, file=sys.stdout) as tr:
        tr.set_description('Testing background')
        for i, X in enumerate(background):
            if i >= max_events:
                break
            predictions_background = model.predict(X)
            scores_background.append(score(X, predictions_background))
            tr.update(1)

    plt.figure()

    for signal in source_signals:
        benchmark = get_generator(signal['path'], 1, **settings)
        scores_benchmark = []
        with trange(max_events, file=sys.stdout) as tr:
            tr.set_description('Testing {}'.format(signal['name']))
            for i, X in enumerate(benchmark):
                if i >= max_events:
                    break
                predictions_benchmark = model.predict(X)
                scores_benchmark.append(score(X, predictions_benchmark))
                tr.update(1)

        tprs, aucs = [], []
        mean_fpr = np.linspace(0, 1, 1000)
        for start_frac in np.arange(0, 1, 0.1):
            stop_frac = start_frac + 0.1
            len_b = len(scores_background)
            len_s = len(scores_benchmark)
            sc_b = scores_background[int(len_b*start_frac):int(len_b*stop_frac)]
            sc_s = scores_benchmark[int(len_s*start_frac):int(len_s*stop_frac)]
            fpr, tpr, _ = roc_curve(
                np.concatenate((np.zeros(len(sc_b)), np.ones(len(sc_s)))),
                np.concatenate((sc_b, sc_s))
            )
            tprs.append(np.interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)

        label = r'[{0:.3f} $\pm {1:.3f}$] {2}'.format(
            mean_auc,
            std_auc,
            signal['name']
        )

        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, alpha=0.5)
        plt.plot(mean_fpr, mean_tpr, label=label)

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

    parser.add_argument('--max-events',
                        default=100000,
                        dest='max_events',
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
         config['settings'],
         config['misc']['plot_style'],
         args.max_events)
