import argparse
import h5py
import numpy as np
import os
import tensorflow as tf
import yaml

from generator import get_generator
from models import DummyAutoencoder
from utils import IsValidFile, draw_loss

from tensorflow.keras.initializers import GlorotUniform
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers.schedules import ExponentialDecay


def main(model_class,
         criterion,
         source_train,
         source_val,
         save_path,
         save_path_plots,
         save_name,
         settings,
         batch_size,
         weight_decay,
         epochs,
         learning_rate,
         momentum):

    # Prepare the dataset
    train_dataset = get_generator(source_train,
                            batch_size,
                            **settings)
    validation_dataset = get_generator(source_val,
                                 batch_size,
                                 **settings)
 
    # Initialize the model
    model = eval(model_class)((18, 14, 1),
                              regularizers.l2(weight_decay),
                              GlorotUniform(seed=None))
    model.summary()

    # Compile the model
    lr_schedule = ExponentialDecay(learning_rate,
                                   decay_steps=100000,
                                   decay_rate=0.96)
    optimizer = SGD(learning_rate=lr_schedule,
                    momentum=momentum)

    model.compile(loss=eval(criterion)(),
                  optimizer=optimizer)

    hist = model.fit(train_dataset,
                     epochs=epochs,
                     validation_data=validation_dataset,
                     use_multiprocessing=True)

    model.save('{0}/{1}'.format(save_path, save_name))
    draw_loss(hist.history['loss'],
              hist.history['val_loss'],
              '{0}/Loss-{1}.png'.format(save_path_plots, save_name))


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
         config['model']['criterion'],
         config['dataset']['train'],
         config['dataset']['validation'],
         config['output']['models'],
         config['output']['plots'],
         config['output']['name'],
         config['settings'],
         args.batch_size,
         args.weight_decay,
         args.epochs,
         args.learning_rate,
         args.momentum)
