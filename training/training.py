#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import h5py
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.metrics import roc_curve, auc
import qkeras
from qkeras import *
import joblib
from models import TeacherAutoencoder
from generator import RegionETGenerator
from plotting import Draw
import yaml

draw = Draw("plots")
config = yaml.safe_load(open('config.yml'))

datasets = [i['path'] for i in config['background'] if i['use']]
datasets = [path for paths in datasets for path in paths]

generator = RegionETGenerator()
X_train, X_val, _ = generator.get_background_split(datasets)
X_train = generator.get_generator(X_train, X_train, 128, True)
X_val = generator.get_generator(X_val, X_val, 128)

# Dataset profiling
deposits, labels = [], []
for dataset in config['background']:
    name = dataset['name']
    X = generator.get_background(dataset['path'])
    X_mean = np.mean(X, axis = 0)
    pT = np.mean(X_mean)
    print(f'{name} shape: {X.shape}')
    print(f'Mean {name} pT is {pT}')
    draw.plot_regional_deposits(X_mean.reshape(18, 14), f'{name} Mean Deposits')
    deposits.append(X)
    labels.append(name)

draw.plot_deposits_distribution(deposits, labels, name="Zero Bias Energy Distribution")

# Model training

teacher = TeacherAutoencoder((18, 14, 1)).get_model()
teacher.summary()


# In[ ]:


teacher.compile(optimizer = keras.optimizers.Adam(learning_rate=0.001), loss = 'mse')


# # Training

# In[ ]:


history = teacher.fit(X_train,
                      steps_per_epoch=len(X_train),
                      epochs = 2,
                      validation_data = X_val,
                      validation_steps=len(X_val),
                      verbose = 1)

teacher.save('saved_models/teacher2023_aug1')

draw.plot_loss_history(history.history['loss'], history.history['val_loss'], 'teacher-training-history')
