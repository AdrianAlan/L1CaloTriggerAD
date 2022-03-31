import tensorflow as tf

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    AveragePooling2D,
    BatchNormalization,
    Conv2D,
    Conv2DTranspose,
    LeakyReLU,
    Input,
    UpSampling2D)


def DummyAutoencoder(input_size, regularizer, initializer):
    # FIXME: Loss goes to inf with MP enabled
    # tf.keras.mixed_precision.set_global_policy('mixed_float16')

    inputs = Input(shape=input_size)
    x = Conv2D(10,
               kernel_size=(3, 3),
               kernel_initializer=initializer,
               kernel_regularizer=regularizer,
               use_bias=False,
               padding='same')(inputs)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)
    x = AveragePooling2D(pool_size=(2, 2))(x)
    x = Conv2D(20,
               kernel_size=(3, 3),
               kernel_initializer=initializer,
               kernel_regularizer=regularizer,
               use_bias=False,
               padding='same')(x)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)
    x = Conv2DTranspose(10,
                        kernel_size=(3, 3),
                        kernel_initializer=initializer,
                        kernel_regularizer=regularizer,
                        use_bias=False,
                        padding='same')(x)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(1,
                        kernel_size=(3, 3),
                        kernel_initializer=initializer,
                        kernel_regularizer=regularizer,
                        use_bias=False,
                        padding='same')(x)
    autoencoder = Model(inputs=inputs, outputs=x)
    return autoencoder
