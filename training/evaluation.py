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


# # Save/load trained models


# In[ ]:


teacher = tf.keras.models.load_model('saved_models/teacher2023_aug1')
teacher.summary()


# In[ ]:


tf.get_logger().setLevel('ERROR')
#student = qkeras.utils.load_qmodel('saved_models/student2023_aug1_v1') # 2023 v1



# # Loss distribution

# In[ ]:
train_ratio = 0.5
val_ratio = 0.1
test_ratio = 1 - train_ratio - val_ratio


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

X_train_val, X_test = train_test_split(X, test_size = test_ratio, random_state = 42)
X_train, X_val = train_test_split(X_train_val, test_size = val_ratio/(val_ratio + train_ratio), random_state = 42)

X_train_predict_teacher = teacher.predict(X_train)
X_val_predict_teacher = teacher.predict(X_val)
X_test_predict_teacher = teacher.predict(X_test)


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



MC_predict_teacher = []
MC_flag_predict_teacher = []
for i in range(len(MC)):
    MC_predict_teacher.append(teacher.predict(MC[i]))
    MC_flag_predict_teacher.append(teacher.predict(MC_flag[i]))


# In[ ]:


def loss(y_true, y_pred, choice):
    if choice == 'mse':
        loss = np.mean((y_true - y_pred)**2, axis = (1,2,3))
        return loss


# In[ ]:


X_train_loss_teacher = loss(X_train, X_train_predict_teacher, 'mse')
X_val_loss_teacher = loss(X_val, X_val_predict_teacher, 'mse')
X_test_loss_teacher = loss(X_test, X_test_predict_teacher, 'mse')

MC_loss_teacher = []
MC_flag_loss_teacher = []
for i in range(len(MC)):
    MC_loss_teacher.append(loss(MC[i], MC_predict_teacher[i], 'mse'))
    MC_flag_loss_teacher.append(loss(MC_flag[i], MC_flag_predict_teacher[i], 'mse'))


# In[ ]:


nbins = 80
rmin = 0
rmax = 100
plt.hist(X_train_loss_teacher, density = 1, bins = nbins, alpha = 0.1, label = 'train (ZeroBias)', range = (rmin, rmax), log = True)
plt.hist(X_val_loss_teacher, density = 1, bins = nbins, alpha = 0.1, label = 'val (ZeroBias)', range = (rmin, rmax), log = True)
plt.hist(X_test_loss_teacher, density = 1, bins = nbins, alpha = 0.1, label = 'test (ZeroBias)', range = (rmin, rmax), log = True)
plt.hist(MC_flag_loss_teacher[0], density = 1, bins = nbins, label = 'H_ToLongLived', color='green', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_teacher[1], density = 1, bins = nbins, label = 'SUEP', color='red', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_teacher[2], density = 1, bins = nbins, label = 'SUSYGGBBH', color='blue', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_teacher[3], density = 1, bins = nbins, label = 'TT', color='orange', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_teacher[4], density = 1, bins = nbins, label = 'VBFHto2C', color='purple', histtype = 'step', range = (rmin, rmax))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel("Anomaly score (teacher)")
plt.savefig("Anomaly score (teacher).png")
plt.close()

# # Comparison between original and reconstructed inputs

# In[ ]:


#show_ZB = True
show_ZB = False
n = 3
for i in range(280,300):
    fig, ax = plt.subplots(figsize = (17,17))
    if show_ZB == True:
        print('ZB test\nloss = ' + str(X_test_loss_teacher[i]))
    else:
        print(str(MC_files[n]) + '\nloss = ' + str(MC_flag_loss_teacher[n][i]))
    ax = plt.subplot(3, 3, 1)
    if show_ZB == True:
        ax = sns.heatmap(X_test[i].reshape(18, 14), vmin = 0, vmax = X_test[i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    else:
        ax = sns.heatmap(MC_flag[n][i].reshape(18, 14), vmin = 0, vmax = MC_flag[n][i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title('Original')
    
    ax = plt.subplot(3, 3, 2)
    if show_ZB == True:
        ax = sns.heatmap(X_test_predict_teacher[i].reshape(18, 14), vmin = 0, vmax = X_test[i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    else:
        ax = sns.heatmap(MC_flag_predict_teacher[n][i].reshape(18, 14), vmin = 0, vmax = MC_flag[n][i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title('Reconstructed')
    
    ax = plt.subplot(3, 3, 3)
    if show_ZB == True:
        ax = sns.heatmap(np.absolute(X_test_predict_teacher[i].reshape(18, 14) - X_test[i].reshape(18, 14)), vmin = 0, vmax = X_test[i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    else:
        ax = sns.heatmap(np.absolute(MC_flag_predict_teacher[n][i].reshape(18, 14) - MC_flag[n][i].reshape(18, 14)), vmin = 0, vmax = MC_flag[n][i].max(), cmap = "Purples", cbar_kws = {'label': 'ET (GeV)'})
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title('abs(original-reconstructed)')

    plt.savefig(f'Comparison between original and reconstructed inputs-{i}.png')
    plt.close()

# # Knowledge Distillation (+ quantizing with QKeras)
cicada_v1 = CicadaV1((252,)).get_model()
cicada_v2 = CicadaV2((252,)).get_model()
cicada_v1.compile(optimizer = 'adam', loss = 'mse')
cicada_v2.compile(optimizer = 'adam', loss = 'mse')

student = cicada_v2
history = student.fit(X_train.reshape((-1,252,1)), X_train_loss_teacher,
                      epochs = 2,
                      validation_data = (X_val.reshape((-1,252,1)), X_val_loss_teacher),
                      batch_size = 1024)

student.save('saved_models/student2023_aug1_v2/')
student = qkeras.utils.load_qmodel('saved_models/student2023_aug1_v2') # 2023 v2
student.summary()
student.get_config()

# In[ ]:


plt.figure(figsize = (15,10))
axes = plt.subplot(2, 2, 1)
axes.plot(history.history['loss'], label = 'train loss')
#axes.set_yscale(value = "log")
axes.plot(history.history['val_loss'], label = 'val loss')
axes.legend(loc = "upper right")
axes.set_xlabel('Epoch')
axes.set_ylabel('Loss')
plt.savefig('train-val-student.png')
plt.close()

# In[ ]:


X_train_loss_student = student.predict(X_train.reshape((-1,252,1)))
X_val_loss_student = student.predict(X_val.reshape((-1,252,1)))
X_test_loss_student = student.predict(X_test.reshape((-1,252,1)))
MC_loss_student = []
MC_flag_loss_student = []
for i in range(len(MC)):
    MC_loss_student.append(student.predict(MC[i].reshape((-1,252,1))))
    MC_flag_loss_student.append(student.predict(MC_flag[i].reshape((-1,252,1))))


# In[ ]:


nbins = 60
rmin = 0
rmax = 60
#plt.hist(X_train_loss_student, density = 1, bins = nbins, alpha = 0.1, label = 'ZB23train', range = (rmin, rmax), log = True)
#plt.hist(X_val_loss_student, density = 1, bins = nbins, alpha = 0.1, label = 'ZB23val', range = (rmin, rmax), log = True)
plt.hist(X_test_loss_student, density = 1, bins = nbins, alpha = 0.1, label = 'ZB23', range = (rmin, rmax), log = True)
plt.hist(MC_flag_loss_student[0], density = 1, bins = nbins, label = 'H_ToLongLived', color='green', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_student[1], density = 1, bins = nbins, label = 'SUEP', color='red', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_student[2], density = 1, bins = nbins, label = 'SUSYGGBBH', color='blue', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_student[3], density = 1, bins = nbins, label = 'TT', color='orange', histtype = 'step', range = (rmin, rmax))
plt.hist(MC_flag_loss_student[4], density = 1, bins = nbins, label = 'VBFHto2C', color='purple', histtype = 'step', range = (rmin, rmax))
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.legend(loc='center left', bbox_to_anchor=(0.57, 0.5))
plt.title('CICADA_v3_v2')
plt.legend(loc='best')
plt.xlabel("Score")
#plt.xticks(np.arange(rmin, rmax, step = 0.0002))
plt.savefig('CICADA_v3_v2.png')
plt.close()

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

# In[ ]:


nbins = 100
rmin = 0
rmax = 25
plt.hist(X_test_A_0_loss_student, density = 1, bins = nbins, label = 'ZB23A_0', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_B_0_loss_student, density = 1, bins = nbins, label = 'ZB23B_0', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_C_0_loss_student, density = 1, bins = nbins, label = 'ZB23C_0', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_D_0_loss_student, density = 1, bins = nbins, label = 'ZB23D_0', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_EphC_0_loss_student, density = 1, bins = nbins, label = 'EZB23C_0', range = (rmin, rmax), log = True, histtype = 'step')

plt.hist(X_test_A_1_loss_student, density = 1, bins = nbins, label = 'ZB23A_1', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_B_1_loss_student, density = 1, bins = nbins, label = 'ZB23B_1', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_C_1_loss_student, density = 1, bins = nbins, label = 'ZB23C_1', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_D_1_loss_student, density = 1, bins = nbins, label = 'ZB23D_1', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_EphC_1_loss_student, density = 1, bins = nbins, label = 'EZB23C_1', range = (rmin, rmax), log = True, histtype = 'step')


plt.hist(X_test_A_2_loss_student, density = 1, bins = nbins, label = 'ZB23A_2', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_B_2_loss_student, density = 1, bins = nbins, label = 'ZB23B_2', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_C_2_loss_student, density = 1, bins = nbins, label = 'ZB23C_2', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_D_2_loss_student, density = 1, bins = nbins, label = 'ZB23D_2', range = (rmin, rmax), log = True, histtype = 'step')
plt.hist(X_test_EphC_2_loss_student, density = 1, bins = nbins, label = 'EZB23C_2', range = (rmin, rmax), log = True, histtype = 'step')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.legend(loc='center left', bbox_to_anchor=(0.57, 0.5))
plt.title('CICADA_v3_v2, scores on different ZB runs')
plt.legend(loc='best')
plt.xlabel("Score")
#plt.xticks(np.arange(rmin, rmax, step = 0.0002))
plt.savefig('CICADA_v3_v2, scores on different ZB runs.png')
plt.close()

# # ROC plotting

# ### Assigning labels and arranging for ROC plotting

# In[ ]:


signal_acceptance_flag = True

#Assign labels for various signals (y = 1) and backgrounds (y = 0)
Y_bkg = np.zeros((X_test.shape[0], 1))
Y_sig = []
for i in range(len(MC)):
    if signal_acceptance_flag == False:
        Y_sig.append(np.ones((MC[i].shape[0], 1)))
    else:
        Y_sig.append(np.ones((MC_flag[i].shape[0], 1)))

#Concatenate datasets to make ROC curves

#True labels
Y_true = []
#Model scores
Y_teacher = []
Y_student = []

for i in range(len(MC)):
    if signal_acceptance_flag == False:
        Y_true.append(np.concatenate((Y_sig[i], Y_bkg)))
        Y_teacher.append(np.concatenate((MC_loss_teacher[i], X_test_loss_teacher)))
        Y_student.append(np.concatenate((MC_loss_student[i], X_test_loss_student)))
    else:
        Y_true.append(np.concatenate((Y_sig[i], Y_bkg)))
        Y_teacher.append(np.concatenate((MC_flag_loss_teacher[i], X_test_loss_teacher)))
        Y_student.append(np.concatenate((MC_flag_loss_student[i], X_test_loss_student)))


# ### Teacher model ROC

# In[ ]:


plt.figure(figsize = (13, 13))
axes = plt.subplot(2, 2, 1)
fpr_teacher = []
tpr_teacher = []
thresholds_teacher = []
roc_auc_teacher = []
for i in range(len(MC)):
    fpr_teacher.append(np.empty((Y_true[i].shape[0],1)))
    tpr_teacher.append(np.empty((Y_true[i].shape[0],1)))
    thresholds_teacher.append(np.empty((Y_true[i].shape[0],1)))
    roc_auc_teacher.append(np.empty((Y_true[i].shape[0],1)))
    fpr_teacher[i], tpr_teacher[i], thresholds_teacher[i] = roc_curve(Y_true[i], Y_teacher[i])
    roc_auc_teacher[i] = auc(fpr_teacher[i], tpr_teacher[i])
    fpr_teacher[i] *= 28.61
    if i == 0:
        axes.plot(fpr_teacher[0], tpr_teacher[0], linestyle = '-', lw = 1.5, color = 'green', label = 'H_ToLongLived (AUC = %.5f)' % (roc_auc_teacher[0]))
    if i == 1:
        axes.plot(fpr_teacher[1], tpr_teacher[1], linestyle = '-', lw = 1.5, color = 'red', label = 'SUEP (AUC = %.5f)' % (roc_auc_teacher[1]))
    if i == 2:
        axes.plot(fpr_teacher[2], tpr_teacher[2], linestyle = '-', lw = 1.5, color = 'blue', label = 'SUSYGGBBH (AUC = %.5f)' % (roc_auc_teacher[2]))
    if i == 3:
        axes.plot(fpr_teacher[3], tpr_teacher[3], linestyle = '-', lw = 1.5, color = 'orange', label = 'TT (AUC = %.5f)' % (roc_auc_teacher[3]))
    if i == 4:
        axes.plot(fpr_teacher[4], tpr_teacher[4], linestyle = '-', lw = 1.5, color = 'purple', label = 'VBFHto2C (AUC = %.5f)' % (roc_auc_teacher[4]))
axes.plot([0.003, 0.003], [0, 1], linestyle = '--', lw = 1, color = 'black', label = 'Trigger rate = 3 kHz')
#axes.set_xlim([0.00002861, 28.61])
axes.set_xlim([0.0001, 28.61])
axes.set_ylim([0.000001, 1.0])
axes.set_xscale(value = "log")
axes.set_yscale(value = "log")
axes.set_xlabel('Trigger Rate (MHz)',size=15)
axes.set_ylabel('Signal Efficiency',size=15)
axes.set_title('Teacher Network',size=15)
#axes.legend(loc='center left', bbox_to_anchor = (0.3, 0.3),fontsize=12)
axes.legend(loc='center left', bbox_to_anchor=(0.26, 0.3),fontsize=12)
plt.savefig('Teacher Network.png')
plt.close()

# ### Student model ROC

# In[ ]:


plt.figure(figsize = (13, 13))
axes = plt.subplot(2, 2, 1)
fpr_student = []
tpr_student = []
thresholds_student = []
roc_auc_student = []

for i in range(len(MC)):
    fpr_student.append(np.empty((Y_true[i].shape[0],1)))
    tpr_student.append(np.empty((Y_true[i].shape[0],1)))
    thresholds_student.append(np.empty((Y_true[i].shape[0],1)))
    roc_auc_student.append(np.empty((Y_true[i].shape[0],1)))
    fpr_student[i], tpr_student[i], thresholds_student[i] = roc_curve(Y_true[i], Y_student[i])
    roc_auc_student[i] = auc(fpr_student[i], tpr_student[i])
    fpr_student[i] *= 28.61
    if i == 0:
        axes.plot(fpr_student[0], tpr_student[0], linestyle = '-', lw = 1.5, color = 'green', label = 'H_ToLongLived (AUC = %.5f)' % (roc_auc_student[0]))
    if i == 1:
        axes.plot(fpr_student[1], tpr_student[1], linestyle = '-', lw = 1.5, color = 'red', label = 'SUEP (AUC = %.5f)' % (roc_auc_student[1]))
    if i == 2:
        axes.plot(fpr_student[2], tpr_student[2], linestyle = '-', lw = 1.5, color = 'blue', label = 'SUSYGGBBH (AUC = %.5f)' % (roc_auc_student[2]))
    if i == 3:
        axes.plot(fpr_student[3], tpr_student[3], linestyle = '-', lw = 1.5, color = 'orange', label = 'TT (AUC = %.5f)' % (roc_auc_student[3]))
    if i == 4:
        axes.plot(fpr_student[4], tpr_student[4], linestyle = '-', lw = 1.5, color = 'purple', label = 'VBFHto2C (AUC = %.5f)' % (roc_auc_student[4]))
axes.plot([0.003, 0.003], [0, 1], linestyle = '--', lw = 1, color = 'black', label = 'Trigger rate = 3 kHz')
#axes.set_xlim([0.00002861, 28.61])
axes.set_xlim([0.0001, 28.61])
axes.set_ylim([0.000001, 1])
axes.set_xscale(value = "log")
axes.set_yscale(value = "log")
axes.set_xlabel('Trigger Rate (MHz)',size=15)
axes.set_ylabel('Signal Efficiency',size=15)
axes.set_title('CICADA_v3_v2, signal(Run3) vs ZB(2023)',size=15)
axes.legend(loc='center left', bbox_to_anchor = (0.26, 0.3),fontsize=12)
#axes.legend(loc='center left', bbox_to_anchor=(1, 0.3),fontsize=12)
plt.savefig("CICADA_v3_v2, signal(Run3) vs ZB(2023).png")
plt.close()

# # cross-validation

# In[ ]:


signal_acceptance_flag = True

Y_bkg = np.zeros((X_test.shape[0], 1))
Y_sig = []
for i in range(len(MC)):
    if signal_acceptance_flag == False:
        Y_sig.append(np.ones((MC[i].shape[0], 1)))
    else:
        Y_sig.append(np.ones((MC_flag[i].shape[0], 1)))
        
Y_true = []
Y_student = []

for i in range(len(MC)):
    if signal_acceptance_flag == False:
        Y_true.append(np.concatenate((Y_sig[i], Y_bkg)))
        Y_student.append(np.concatenate((MC_loss_student[i], X_test_loss_student)))
    else:
        Y_true.append(np.concatenate((Y_sig[i], Y_bkg)))
        Y_student.append(np.concatenate((MC_flag_loss_student[i], X_test_loss_student)))

def kfold(y, k):
    N=y.shape[0]
    n=np.floor(N/k).astype(int)
    y_kf=[]
    for i in range(k):
        y_kf.append(y[i*n : (i+1)*n])
    return y_kf

kf=10
X_test_loss_model = X_test_loss_student
Y_model = Y_student
if signal_acceptance_flag == False:
    MC_loss_model = MC_loss_student
else:
    MC_loss_model = MC_flag_loss_student

X_test_loss_model_kf=kfold(X_test_loss_model,kf)
Y_bkg_kf=kfold(Y_bkg,kf)

plt.figure(figsize = (16, 16))
axes = plt.subplot(2, 2, 1)

fpr = []
tpr = []
thresholds = []
roc_auc = []

for j in range(len(MC)):
    fpr.append(np.empty((Y_true[j].shape[0],1)))
    tpr.append(np.empty((Y_true[j].shape[0],1)))
    thresholds.append(np.empty((Y_true[j].shape[0],1)))
    roc_auc.append(np.empty((Y_true[j].shape[0],1)))
    fpr[j], tpr[j], thresholds[j] = roc_curve(Y_true[j], Y_model[j])
    roc_auc[j] = auc(fpr[j], tpr[j])
    fpr[j] *= 28.61
    
    MC_loss_model_kf=kfold(MC_loss_model[j],kf)
    Y_sig_kf=kfold(Y_sig[j],kf)

    Y_true_kf=[]
    Y_model_kf=[]
    for i in range(kf):
        Y_true_kf.append(np.concatenate((Y_sig_kf[i],Y_bkg_kf[i])))
        Y_model_kf.append((np.concatenate((MC_loss_model_kf[i],X_test_loss_model_kf[i]))))

    fpr_mean=np.linspace(0,1,10000000)
    tpr_kf=[]
    fpr_kf=[]
    thresholds_kf=[]
    roc_auc_kf=[]
    for i in range(kf):
        tpr_kf.append(np.empty((Y_true_kf[i].shape[0],1)))
        fpr_kf.append(np.empty((Y_true_kf[i].shape[0],1)))
        thresholds_kf.append(np.empty((Y_true_kf[i].shape[0],1)))
        roc_auc_kf.append(np.empty((Y_true_kf[i].shape[0],1)))
        fpr_kf[i], tpr_kf[i], thresholds_kf[i] = roc_curve(Y_true_kf[i], Y_model_kf[i])
        roc_auc_kf[i] = auc(fpr_kf[i], tpr_kf[i])

    tpr_total=[]
    for i in range(kf):
        interp_tpr=np.interp(fpr_mean, fpr_kf[i], tpr_kf[i])
        interp_tpr[0]=0.0
        tpr_total.append(interp_tpr)
    tpr_mean=np.mean(tpr_total, axis=0)
    tpr_mean[-1]=1.0
    roc_auc_mean=auc(fpr_mean,tpr_mean)
    roc_auc_std=np.std(roc_auc_kf)
    
    tpr_std=np.std(tpr_total, axis=0)
    tpr_up=np.minimum(tpr_mean+tpr_std,1)
    tpr_down=np.maximum(tpr_mean-tpr_std,0)

    fpr_mean *= 28.61
    
    if j == 0:
        axes.plot(fpr_mean, tpr_mean, linestyle = '-', lw = 1.5, color = 'green', label = 'H_ToLongLived (AUC = %.5f $\pm$ %0.5f)' % (roc_auc_mean, roc_auc_std))
        axes.fill_between(fpr_mean, tpr_down, tpr_up, color='green', alpha=0.1)
    if j == 1:
        axes.plot(fpr_mean, tpr_mean, linestyle = '-', lw = 1.5, color = 'red', label = 'SUEP (AUC = %.5f $\pm$ %0.5f)' % (roc_auc_mean, roc_auc_std))
        axes.fill_between(fpr_mean, tpr_down, tpr_up, color='red', alpha=0.1)
    if j == 2:
        axes.plot(fpr_mean, tpr_mean, linestyle = '-', lw = 1.5, color = 'blue', label = 'SUSYGGBBH (AUC = %.5f $\pm$ %0.5f)' % (roc_auc_mean, roc_auc_std))
        axes.fill_between(fpr_mean, tpr_down, tpr_up, color='blue', alpha=0.1)
    if j == 3:
        axes.plot(fpr_mean, tpr_mean, linestyle = '-', lw = 1.5, color = 'orange', label = 'TT (AUC = %.5f $\pm$ %0.5f)' % (roc_auc_mean, roc_auc_std))
        axes.fill_between(fpr_mean, tpr_down, tpr_up, color='orange', alpha=0.1)
    if j == 4:
        axes.plot(fpr_mean, tpr_mean, linestyle = '-', lw = 1.5, color = 'purple', label = 'VBFHto2C (AUC = %.5f $\pm$ %0.5f)' % (roc_auc_mean, roc_auc_std))
        axes.fill_between(fpr_mean, tpr_down, tpr_up, color='purple', alpha=0.1)

axes.plot([0.003, 0.003], [0, 1], linestyle = '--', lw = 1, color = 'black', label = 'Trigger rate = 3 kHz')
axes.set_xlim([0.0001, 28.61])
axes.set_ylim([0.000001, 1])
axes.set_xscale(value = "log")
axes.set_yscale(value = "log")
axes.set_xlabel('Trigger Rate (MHz)',size=17)
axes.set_ylabel('Signal Efficiency',size=17)
axes.set_title('CICADA_v3_v2, signal(Run3) vs ZB(2023)',size=17)
axes.legend(loc='center left', bbox_to_anchor = (0.28, 0.3),fontsize=11)
plt.savefig("CICADA_v3_v2, signal(Run3) vs ZB(2023).png")
plt.close()

# In[ ]:




