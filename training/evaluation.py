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

from models import CicadaV1, CicadaV2
from generator import RegionETGenerator
from plotting import Draw
 
draw = Draw("plots")

tf.get_logger().setLevel('ERROR')

datasets = [
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_0.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_0.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_0.h5',
   '/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_0.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_1.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_1.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_1.h5',
   '/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_1.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_2.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_2.h5',
   '/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_2.h5',
   '/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_2.h5']
signal_datasets = {
   'H_ToLongLived': '/eos/project/c/cicada-project/data/2023/Signal/H_ToLongLived.h5',
   'SUEP': '/eos/project/c/cicada-project/data/2023/Signal/SUEP.h5',
 'SUSYGGBBH': '/eos/project/c/cicada-project/data/2023/Signal/SUSYGGBBH.h5',
 'TT': '/eos/project/c/cicada-project/data/2023/Signal/TT.h5',
 'VBHFto2C': '/eos/project/c/cicada-project/data/2023/Signal/VBFHto2C.h5'}

generator = RegionETGenerator()
X_train, X_val, X_test = generator.get_background(datasets)
X_signal = generator.get_signal(signal_datasets)

teacher = tf.keras.models.load_model('saved_models/teacher2023_aug1')
teacher.summary()

# # Loss distribution
X_A_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_B_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_C_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_D_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_EphC_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))


X_A_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_B_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_C_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_D_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_EphC_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))


X_A_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_B_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_C_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_D_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
X_EphC_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))

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
  X_val_loss_teacher, 128, True
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


# In[ ]:


X_test_A_0_loss_student = student.predict(X_A_0.reshape((-1,252,1)))
X_test_B_0_loss_student = student.predict(X_B_0.reshape((-1,252,1)))
X_test_C_0_loss_student = student.predict(X_C_0.reshape((-1,252,1)))
X_test_D_0_loss_student = student.predict(X_D_0.reshape((-1,252,1)))
X_test_EphC_0_loss_student = student.predict(X_EphC_0.reshape((-1,252,1)))


X_test_A_1_loss_student = student.predict(X_A_1.reshape((-1,252,1)))
X_test_B_1_loss_student = student.predict(X_B_1.reshape((-1,252,1)))
X_test_C_1_loss_student = student.predict(X_C_1.reshape((-1,252,1)))
X_test_D_1_loss_student = student.predict(X_D_1.reshape((-1,252,1)))
X_test_EphC_1_loss_student = student.predict(X_EphC_1.reshape((-1,252,1)))

X_test_A_2_loss_student = student.predict(X_A_2.reshape((-1,252,1)))
X_test_B_2_loss_student = student.predict(X_B_2.reshape((-1,252,1)))
X_test_C_2_loss_student = student.predict(X_C_2.reshape((-1,252,1)))
X_test_D_2_loss_student = student.predict(X_D_2.reshape((-1,252,1)))
X_test_EphC_2_loss_student = student.predict(X_EphC_2.reshape((-1,252,1)))


scores = [
X_test_A_0_loss_student,
X_test_B_0_loss_student,
X_test_C_0_loss_student,
X_test_D_0_loss_student,
X_test_EphC_0_loss_student,
X_test_A_1_loss_student,
X_test_B_1_loss_student,
X_test_C_1_loss_student,
X_test_D_1_loss_student,
X_test_EphC_1_loss_student,
X_test_A_2_loss_student,
X_test_B_2_loss_student,
X_test_C_2_loss_student,
X_test_D_2_loss_student,
X_test_EphC_2_loss_student]

labels = [
'ZB23A_0'
'ZB23B_0'
'ZB23C_0'
'ZB23D_0'
'EZB23C_0'
'ZB23A_1'
'ZB23B_1'
'ZB23C_1'
'ZB23D_1'
'EZB23C_1'
'ZB23A_2'
'ZB23B_2'
'ZB23C_2'
'ZB23D_2'
'EZB23C_2']
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
