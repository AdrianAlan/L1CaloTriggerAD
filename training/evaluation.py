#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import h5py
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.metrics import roc_curve, auc
import qkeras
from qkeras import *
#import tensorflow_probability as tfp
#import keras_tuner
#from keras_tuner import Hyperband
import joblib
import yaml

from models import CicadaV1, CicadaV2
from generator import RegionETGenerator
from plotting import Draw
 
tf.get_logger().setLevel('ERROR')

draw = Draw("plots")

config = yaml.safe_load(open('config.yml'))
datasets = [i['path'] for i in config['background'] if i['use']]
datasets = [path for paths in datasets for path in paths]

generator = RegionETGenerator()
X_train, X_val, X_test = generator.get_background_split(datasets)
X_signal = generator.get_signal(config['signal'])

teacher = tf.keras.models.load_model('saved_models/teacher2023_aug1')
teacher.summary()

X_train_predict_teacher = teacher.predict(X_train)
X_val_predict_teacher = teacher.predict(X_val)
X_test_predict_teacher = teacher.predict(X_test)

def loss(y_true, y_pred, choice):
    if choice == 'mse':
        mse = tf.keras.losses.MeanSquaredError(reduction=tf.keras.losses.Reduction.NONE)
        loss = mse(y_true, y_pred).numpy()
    return np.mean(loss, axis=(1, 2))

MC_flag_loss_teacher = []
MC_flag_predict_teacher = []
for name, data in X_signal.items():
    y_pred = teacher.predict(data)
    MC_flag_predict_teacher.append(y_pred)
    MC_flag_loss_teacher.append(loss(data, y_pred, 'mse'))

X_train_loss_teacher = loss(
    X_train,
    X_train_predict_teacher, 'mse')
X_val_loss_teacher = loss(X_val,
   X_val_predict_teacher, 'mse')
X_test_loss_teacher = loss(X_test,
   X_test_predict_teacher, 'mse')

scores = [
X_train_loss_teacher,
X_val_loss_teacher,
X_test_loss_teacher,
MC_flag_loss_teacher[0],
MC_flag_loss_teacher[1],
MC_flag_loss_teacher[2],
MC_flag_loss_teacher[3],
MC_flag_loss_teacher[4]
]
labels = [
'train (ZeroBias)',
'val (ZeroBias)',
'test (ZeroBias)',
'H_ToLongLived',
'SUEP',
'SUSYGGBBH',
'TT', 
 'VBHFto2C']

draw.plot_anomaly_score_distribution(scores, labels, "anomaly-score-teacher")


# # Comparison between original and reconstructed inputs

draw.plot_reconstruction_results(X_test[0], X_test_predict_teacher[0], loss=X_test_loss_teacher[0], name="comparison-background")
draw.plot_reconstruction_results(X_signal['SUSYGGBBH'][0], MC_flag_predict_teacher[2][0], loss=MC_flag_loss_teacher[2][0] ,name="comparison-signal")

# # Knowledge Distillation (+ quantizing with QKeras)
cicada_v1 = CicadaV1((252,)).get_model()
cicada_v2 = CicadaV2((252,)).get_model()
cicada_v1.compile(optimizer = 'adam', loss = 'mse')
cicada_v2.compile(optimizer = 'adam', loss = 'mse')

student = cicada_v2
X_train_gen = generator.get_generator(
  X_train.reshape((-1, 252, 1)),
  X_train_loss_teacher, 128, True
)
X_val_gen = generator.get_generator(
  X_val.reshape((-1, 252, 1)),
  X_val_loss_teacher, 128, False
)
history = student.fit(X_train_gen,
  steps_per_epoch=len(X_train_gen),
  epochs = 2,
  validation_data = X_val_gen,
  validation_steps=len(X_val_gen),
  verbose = 1)

student.save('saved_models/student2023_aug1_v2/')
student = qkeras.utils.load_qmodel('saved_models/student2023_aug1_v2') # 2023 v2
student.summary()
student.get_config()

draw.plot_loss_history(history.history['loss'], history.history['val_loss'], 'student-training-history')

X_train_loss_student = student.predict(X_train.reshape((-1,252,1)))
X_val_loss_student = student.predict(X_val.reshape((-1,252,1)))
X_test_loss_student = student.predict(X_test.reshape((-1,252,1)))
MC_loss_student = []
MC_flag_loss_student = []
for name, data in X_signal.items():
    MC_loss_student.append(student.predict(data.reshape((-1,252,1))))
    MC_flag_loss_student.append(student.predict(data.reshape((-1,252,1))))


scores = [
X_test_loss_student,
MC_flag_loss_student[0],
MC_flag_loss_student[1],
MC_flag_loss_student[2],
MC_flag_loss_student[3],
MC_flag_loss_student[4]
]
labels = [
'ZeroBias 2023',
'H_ToLongLived',
'SUEP',
'SUSYGGBBH',
'TT', 
 'VBHFto2C']

draw.plot_anomaly_score_distribution(scores, labels, "anomaly-score-student")


scores, labels = [], []
for dataset in config['background']:
    name = dataset['name']
    X = generator.get_background(dataset['path'])
    y_pred = student.predict(X.reshape((-1,252,1)))
    scores.append(y_pred)
    labels.append(name)
draw.plot_anomaly_score_distribution(scores, labels, "anomaly-score-student-background")

#Assign labels for various signals (y = 1) and backgrounds (y = 0)
Y_bkg = np.zeros((X_test.shape[0], 1))
Y_sig = []
for name, data in X_signal.items():
    Y_sig.append(np.ones((data.shape[0], 1)))

#Concatenate datasets to make ROC curves

Y_true, Y_teacher, Y_student = [], [], []
for i, (name, data) in enumerate(X_signal.items()):
    Y_true.append(np.concatenate((Y_sig[i], Y_bkg)))
    Y_teacher.append(np.concatenate((MC_flag_loss_teacher[i], X_test_loss_teacher)))
    Y_student.append(np.concatenate((MC_flag_loss_student[i], X_test_loss_student)))

# ROC Curves with Cross-Validation
draw.plot_roc_curve(Y_true, Y_teacher, X_signal.keys(), "roc-teacher")
draw.plot_roc_curve(Y_true, Y_student, X_signal.keys(), "roc-student")
