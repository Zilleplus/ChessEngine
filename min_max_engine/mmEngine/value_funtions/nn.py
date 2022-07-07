from random import shuffle
import tensorflow as tf  # type: ignore
import tensorflow.keras as keras  # type: ignore
import tensorflow.keras.layers as layers  # type: ignore
import numpy as np


def CreateModel() -> keras.Model:
    # 8*8 board -> one hot encoding of 12 states
    model = keras.Sequential([
        layers.InputLayer(input_shape=(8, 8, 12)),
        layers.Conv2D(
            filters=64,
            kernel_size=1,
            padding="same",
            activation="relu",
            input_shape=(8,8,12)),
        layers.MaxPooling2D(),
        layers.Conv2D(
            filters=32,
            kernel_size=1,
            padding="same",
            activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(
            filters=32,
            kernel_size=1,
            padding="same",
            activation="relu"),
        layers.Dense(units=1, activation="tanh")])
    model.compile(optimizer="Nadam", loss='mse', metrics=["accuracy"])

    return model


def TrainModel(model: keras.Model, dataset: np.ndarray):
    batch_size: int = 1000

    X = \
        tf.data.Dataset.from_tensors(dataset["X"]) \
        .unbatch() \
        .prefetch(512) \
    
    X_reshaped = X \
        .map(lambda x: tf.reshape(x, (8, 8)))

    X_one_hot = X_reshaped \
        .map(lambda x: tf.one_hot(x, 12))

    Y = tf.data.Dataset.from_tensors(dataset["Y"]) \
        .map(lambda x: tf.cast(x, tf.float32)) \
        .unbatch()

    data = tf.data.Dataset.zip((X_one_hot, Y))\
        .shuffle(10000) \
        .batch(batch_size=batch_size)

    # Take 1000 batches of data as validation set.
    # The shuffle made sure there spread out from
    # all kings of games.
    validation_size = 1000
    validation_data = data.take(validation_size)
    train_data = data.skip(validation_size)

    model.fit(x=train_data, validation_data=validation_data, epochs=10)

    return

class NNValueFunction:
    pass