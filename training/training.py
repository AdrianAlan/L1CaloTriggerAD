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

draw = Draw("plots")

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

generator = RegionETGenerator()
X_train, X_val, _ = generator.get_background(datasets)
X_train = generator.get_generator(X_train, X_train, 128, True)
X_val = generator.get_generator(X_val, X_val, 128)




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

print('X_A_0    shape: ' + str(X_A_0.shape))
print('X_B_0    shape: ' + str(X_B_0.shape))
print('X_C_0    shape: ' + str(X_C_0.shape))
print('X_D_0    shape: ' + str(X_D_0.shape))
print('X_EphC_0 shape: ' + str(X_EphC_0.shape))


print('X_A_1    shape: ' + str(X_A_1.shape))
print('X_B_1    shape: ' + str(X_B_1.shape))
print('X_C_1    shape: ' + str(X_C_1.shape))
print('X_D_1    shape: ' + str(X_D_1.shape))
print('X_EphC_1 shape: ' + str(X_EphC_1.shape))


print('X_A_2    shape: ' + str(X_A_2.shape))
print('X_B_2    shape: ' + str(X_B_2.shape))
print('X_C_2    shape: ' + str(X_C_2.shape))
print('X_D_2    shape: ' + str(X_D_2.shape))
print('X_EphC_2 shape: ' + str(X_EphC_2.shape))


# Take a look at some ZB statistics.

# In[ ]:


ZB_A_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_B_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_C_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_D_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
EZB_C_0 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))


ZB_A_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_B_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_C_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_D_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
EZB_C_1 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))


ZB_A_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunA_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_B_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_C_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
ZB_D_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))
EZB_C_2 = np.reshape(h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1))

print('ZeroBias2023A_0   shape: ' + str(ZB_A_0.shape))
print('ZeroBias2023B_0   shape: ' + str(ZB_B_0.shape))
print('ZeroBias2023C_0   shape: ' + str(ZB_C_0.shape))
print('ZeroBias2023D_0   shape: ' + str(ZB_D_0.shape))
print('EZeroBias2023C_0  shape: ' + str(EZB_C_0.shape))


print('ZeroBias2023A_1   shape: ' + str(ZB_A_1.shape))
print('ZeroBias2023B_1   shape: ' + str(ZB_B_1.shape))
print('ZeroBias2023C_1   shape: ' + str(ZB_C_1.shape))
print('ZeroBias2023D_1   shape: ' + str(ZB_D_1.shape))
print('EZeroBias2023C_1  shape: ' + str(EZB_C_1.shape))

print('ZeroBias2023A_2   shape: ' + str(ZB_A_2.shape))
print('ZeroBias2023B_2   shape: ' + str(ZB_B_2.shape))
print('ZeroBias2023C_2   shape: ' + str(ZB_C_2.shape))
print('ZeroBias2023D_2   shape: ' + str(ZB_D_2.shape))
print('EZeroBias2023C_2  shape: ' + str(EZB_C_2.shape))

ZB_A_0_mean = np.mean(ZB_A_0, axis = 0)
ZB_B_0_mean = np.mean(ZB_B_0, axis = 0)
ZB_C_0_mean = np.mean(ZB_C_0, axis = 0)
ZB_D_0_mean = np.mean(ZB_D_0, axis = 0)
EZB_C_0_mean = np.mean(EZB_C_0, axis = 0)


ZB_A_1_mean = np.mean(ZB_A_1, axis = 0)
ZB_B_1_mean = np.mean(ZB_B_1, axis = 0)
ZB_C_1_mean = np.mean(ZB_C_1, axis = 0)
ZB_D_1_mean = np.mean(ZB_D_1, axis = 0)
EZB_C_1_mean = np.mean(EZB_C_1, axis = 0)


ZB_A_2_mean = np.mean(ZB_A_2, axis = 0)
ZB_B_2_mean = np.mean(ZB_B_2, axis = 0)
ZB_C_2_mean = np.mean(ZB_C_2, axis = 0)
ZB_D_2_mean = np.mean(ZB_D_2, axis = 0)
EZB_C_2_mean = np.mean(EZB_C_2, axis = 0)

draw.plot_regional_deposits(ZB_A_0_mean.reshape(18, 14), "ZB2023RunA_0")
draw.plot_regional_deposits(ZB_B_0_mean.reshape(18, 14), "ZB2023RunB_0")
draw.plot_regional_deposits(ZB_C_0_mean.reshape(18, 14), "ZB2023RunC_0")
draw.plot_regional_deposits(ZB_D_0_mean.reshape(18, 14), "ZB2023RunD_0")
draw.plot_regional_deposits(EZB_C_0_mean.reshape(18, 14), "EphemeralZB2023RunC_0")
draw.plot_regional_deposits(ZB_A_1_mean.reshape(18, 14), "ZB2023RunA_1")
draw.plot_regional_deposits(ZB_B_1_mean.reshape(18, 14), "ZB2023RunB_1")
draw.plot_regional_deposits(ZB_C_1_mean.reshape(18, 14), "ZB2023RunC_1")
draw.plot_regional_deposits(ZB_D_1_mean.reshape(18, 14), "ZB2023RunD_1")
draw.plot_regional_deposits(EZB_C_1_mean.reshape(18, 14), "EphemeralZB2023RunC_1")
draw.plot_regional_deposits(ZB_A_2_mean.reshape(18, 14), "ZB2023RunA_2")
draw.plot_regional_deposits(ZB_B_2_mean.reshape(18, 14), "ZB2023RunB_2")
draw.plot_regional_deposits(ZB_C_2_mean.reshape(18, 14), "ZB2023RunC_2")
draw.plot_regional_deposits(ZB_D_2_mean.reshape(18, 14), "ZB2023RunD_2")
draw.plot_regional_deposits(EZB_C_2_mean.reshape(18, 14), "EphemeralZB2023RunC_2")

draw.plot_deposits_distribution(
  [ZB_A_0, ZB_B_0, ZB_C_0, ZB_D_0, EZB_C_0, ZB_A_1, ZB_B_1, ZB_C_1, ZB_D_1, EZB_C_1, ZB_A_1, ZB_B_1, ZB_C_1, ZB_D_1, EZB_C_1],
  ["2023RunA_0", "2023RunB_0", "2023RunC_0", "2023RunD_0", "2023EphemeralRunC_0", "2023RunA_1", "2023RunB_1", "2023RunC_1", "2023RunD_1", "2023EphemeralRunC_1", "2023RunA_2", "2023RunB_2", "2023RunC_2", "2023RunD_2", "2023EphemeralRunC_2"],
   name="Zero Bias Energy Distribution"
)

print('Mean ZB2023A_0 pT = ' + str(np.mean(ZB_A_0.reshape(-1))))
print('Mean ZB2023B_0 pT = ' + str(np.mean(ZB_B_0.reshape(-1))))
print('Mean ZB2023C_0 pT = ' + str(np.mean(ZB_C_0.reshape(-1))))
print('Mean ZB2023D_0 pT = ' + str(np.mean(ZB_D_0.reshape(-1))))
print('Mean EphemeralZB2023C_0 pT = ' + str(np.mean(EZB_C_0.reshape(-1))))


print('Mean ZB2023A_1 pT = ' + str(np.mean(ZB_A_1.reshape(-1))))
print('Mean ZB2023B_1 pT = ' + str(np.mean(ZB_B_1.reshape(-1))))
print('Mean ZB2023C_1 pT = ' + str(np.mean(ZB_C_1.reshape(-1))))
print('Mean ZB2023D_1 pT = ' + str(np.mean(ZB_D_1.reshape(-1))))
print('Mean EphemeralZB2023C_1 pT = ' + str(np.mean(EZB_C_1.reshape(-1))))


print('Mean ZB2023A_2 pT = ' + str(np.mean(ZB_A_2.reshape(-1))))
print('Mean ZB2023B_2 pT = ' + str(np.mean(ZB_B_2.reshape(-1))))
print('Mean ZB2023C_2 pT = ' + str(np.mean(ZB_C_2.reshape(-1))))
print('Mean ZB2023D_2 pT = ' + str(np.mean(ZB_D_2.reshape(-1))))
print('Mean EphemeralZB2023C_2 pT = ' + str(np.mean(EZB_C_2.reshape(-1))))

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
