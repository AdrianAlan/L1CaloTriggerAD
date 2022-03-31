import h5py
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_generator(source,
                  batch_size,
                  raw=False,
                  flatten=False,
                  flip=False,
                  normalize=False,
                  standardize=True):

    norm = None
    if normalize:
        norm = norm_m
    elif standardize:
        norm = norm_s

    data_gen_args = dict(
        preprocessing_function=norm,
        horizontal_flip=flip,
        vertical_flip=flip,
    )

    image_datagen = ImageDataGenerator(**data_gen_args)
    calo_regions = h5py.File(source, 'r')['CaloRegions'][:]
    calo_regions = calo_regions.reshape(-1, 18, 14, 1)
    image_generator = image_datagen.flow(
        calo_regions, None, batch_size=batch_size)
    return image_generator


def norm_m(t):
    m = tf.raw_ops.Max(input=t, axis=[0, 1])
    return t / m if m else t


def norm_s(t):
    m, s = tf.math.reduce_mean(t), tf.math.reduce_std(t)
    return (t - m) / s if s else t
