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


# # data files

# All input files have data already sorted in Calo regions (i, j) ~ (18, 14)<br>
# i = 0 -> 17 corresponds to GCT_Phi = 0 -> 17<br>
# j = 0 -> 13 corresponds to RCT_Eta = 4 -> 17

# In[ ]:


X = np.concatenate((h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_0.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_0.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_0.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_1.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_1.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_1.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunB_2.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/ZB_RunD_2.h5', 'r')['CaloRegions'][:].astype('float32'),
                    h5py.File('/eos/project/c/cicada-project/data/2023/Background/EZB0_RunC_2.h5', 'r')['CaloRegions'][:].astype('float32'))
                  )

X = np.reshape(X, (-1,18,14,1))

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

print('X      shape: ' + str(X.shape))
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

MC_files = []
MC_files.append('/eos/project/c/cicada-project/data/2023/Signal/H_ToLongLived.h5')
MC_files.append('/eos/project/c/cicada-project/data/2023/Signal/SUEP.h5')
MC_files.append('/eos/project/c/cicada-project/data/2023/Signal/SUSYGGBBH.h5')
MC_files.append('/eos/project/c/cicada-project/data/2023/Signal/TT.h5')
MC_files.append('/eos/project/c/cicada-project/data/2023/Signal/VBFHto2C.h5')
    
MC = []
Acceptance_Flag = []
Acceptance_Filter = []
MC_flag = []
for i in range(len(MC_files)):
    MC.append(np.reshape(h5py.File(MC_files[i], 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1)))
    MC_flag.append(np.reshape(h5py.File(MC_files[i], 'r')['CaloRegions'][:].astype('float32'), (-1,18,14,1)))
    Acceptance_Flag.append(h5py.File(MC_files[i], 'r')['AcceptanceFlag'][:].astype('int32'))
    Acceptance_Filter.append([])
    for j in range(MC[i].shape[0]):
        if Acceptance_Flag[i][j] == 1:
            Acceptance_Filter[i].append(True)
        else:
            Acceptance_Filter[i].append(False)
    MC_flag[i] = MC_flag[i][Acceptance_Filter[i]]
    print('i = ' + str(i) + ': ' + str(MC_flag[i].shape) + ' / ' + str(MC[i].shape) + '; accepted ' + str(np.round(np.mean(Acceptance_Flag[i]), 4)))


# In[ ]:


train_ratio = 0.5
val_ratio = 0.1
test_ratio = 1 - train_ratio - val_ratio
X_train_val, X_test = train_test_split(X, test_size = test_ratio, random_state = 42)
X_train, X_val = train_test_split(X_train_val, test_size = val_ratio/(val_ratio + train_ratio), random_state = 42)
print('X_train shape: ' + str(X_train.shape))
print('X_val   shape: ' + str(X_val.shape))
print('X_test  shape: ' + str(X_test.shape))
del X_train_val


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




fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_A_0_mean.reshape(18, 14), vmin = 0, vmax = ZB_A_0_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunA_0)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_B_0_mean.reshape(18, 14), vmin = 0, vmax = ZB_B_0_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunB_0)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_C_0_mean.reshape(18, 14), vmin = 0, vmax = ZB_C_0_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunC_0)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_D_0_mean.reshape(18, 14), vmin = 0, vmax = ZB_D_0_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunD_0)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(EZB_C_0_mean.reshape(18, 14), vmin = 0, vmax = EZB_C_0_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (EphemeralZB2023RunC_0)')
plt.show()



fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_A_1_mean.reshape(18, 14), vmin = 0, vmax = ZB_A_1_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunA_1)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_B_1_mean.reshape(18, 14), vmin = 0, vmax = ZB_B_1_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunB_1)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_C_1_mean.reshape(18, 14), vmin = 0, vmax = ZB_C_1_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunC_1)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_D_1_mean.reshape(18, 14), vmin = 0, vmax = ZB_D_1_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunD_1)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(EZB_C_1_mean.reshape(18, 14), vmin = 0, vmax = EZB_C_1_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (EphemeralZB2023RunC_1)')
plt.show()




fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_A_2_mean.reshape(18, 14), vmin = 0, vmax = ZB_A_2_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunA_2)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_B_2_mean.reshape(18, 14), vmin = 0, vmax = ZB_B_2_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunB_2)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_C_2_mean.reshape(18, 14), vmin = 0, vmax = ZB_C_2_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunC_2)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(ZB_D_2_mean.reshape(18, 14), vmin = 0, vmax = ZB_D_2_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (ZB2023RunD_2)')
plt.show()

fig, ax = plt.subplots(figsize = (10,10))
ax = plt.subplot(2, 2, 2)
ax = sns.heatmap(EZB_C_2_mean.reshape(18, 14), vmin = 0, vmax = EZB_C_2_mean.max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_title('Mean Et (EphemeralZB2023RunC_2)')
plt.show()


# In[ ]:


plt.hist(ZB_A_0.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunA_0', log = True, histtype='step')
plt.hist(ZB_B_0.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunB_0', log = True, histtype='step')
plt.hist(ZB_C_0.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunC_0', log = True, histtype='step')
plt.hist(ZB_D_0.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunD_0', log = True, histtype='step')
plt.hist(EZB_C_0.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023EphemeralRunC_0', log = True, histtype='step')


plt.hist(ZB_A_1.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunA_1', log = True, histtype='step')
plt.hist(ZB_B_1.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunB_1', log = True, histtype='step')
plt.hist(ZB_C_1.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunC_1', log = True, histtype='step')
plt.hist(ZB_D_1.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunD_1', log = True, histtype='step')
plt.hist(EZB_C_1.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023EphemeralRunC_1', log = True, histtype='step')

plt.hist(ZB_A_2.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunA_2', log = True, histtype='step')
plt.hist(ZB_B_2.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunB_2', log = True, histtype='step')
plt.hist(ZB_C_2.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunC_2', log = True, histtype='step')
plt.hist(ZB_D_2.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023RunD_2', log = True, histtype='step')
plt.hist(EZB_C_2.reshape((-1)), bins = 100, range=(0,1024), density=1, label='2023EphemeralRunC_2', log = True, histtype='step')

plt.xlabel("ZB Et")
plt.legend(loc='best')
plt.show()

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



# # CNN AE (teacher model)

# In[ ]:


encoder_input = tf.keras.Input(shape=(18,14,1), name='input')

encoder = layers.Conv2D(20, (3,3), strides=1, padding='same', name='conv2d_1')(encoder_input)
encoder = layers.Activation('relu', name='relu_1')(encoder)
encoder = layers.AveragePooling2D((2,2), name='pool_1')(encoder)
encoder = layers.Conv2D(30, (3,3), strides=1, padding='same', name='conv2d_2')(encoder)
encoder = layers.Activation('relu', name='relu_2')(encoder)
encoder = layers.Flatten(name='flatten')(encoder)

encoder_output = layers.Dense(80, activation='relu', name='latent')(encoder)

encoder = tf.keras.models.Model(encoder_input, encoder_output)
encoder.summary()


# In[ ]:


decoder = layers.Dense(9*7*30, name='dense')(encoder_output)
decoder = layers.Reshape((9,7,30), name='reshape2')(decoder)
decoder = layers.Activation('relu', name='relu_3')(decoder)
decoder = layers.Conv2D(30, (3,3), strides=1, padding='same', name='conv2d_3')(decoder)
decoder = layers.Activation('relu', name='relu_4')(decoder)
decoder = layers.UpSampling2D((2,2), name='upsampling')(decoder)
decoder = layers.Conv2D(20, (3,3), strides=1, padding='same', name='conv2d_4')(decoder)
decoder = layers.Activation('relu', name='relu_5')(decoder)

decoder_output = layers.Conv2D(1, (3,3), activation='relu', strides=1, padding='same', name='output')(decoder)


# In[ ]:


teacher = tf.keras.Model(encoder_input, decoder_output)
teacher.summary()


# In[ ]:


teacher.compile(optimizer = keras.optimizers.Adam(learning_rate=0.001), loss = 'mse')


# # Training

# In[ ]:


history = teacher.fit(X_train, X_train,
                      epochs = 40,
                      validation_data = (X_val, X_val),
                      batch_size = 128)


# In[ ]:


plt.figure(figsize = (15,10))
axes = plt.subplot(2, 2, 1)
axes.plot(history.history['loss'], label = 'train loss')
axes.plot(history.history['val_loss'], label = 'val loss')
axes.legend(loc = "upper right")
axes.set_xlabel('Epoch')
axes.set_ylabel('Loss')






