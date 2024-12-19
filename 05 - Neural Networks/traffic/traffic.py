import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from keras import models, layers

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = []
    labels = []

    for file in os.listdir(data_dir):

        if not int(file):
            continue

        base_dir = os.path.join(data_dir, file)
        # Load each individual image within each file directory
        for img_file in os.listdir(base_dir):
            # load individual image -> resize and normalise
            img = cv2.imread(os.path.join(base_dir, img_file))
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT)) / 255
            images.append(img)
            labels.append(int(file))

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = models.Sequential()

    model.add(layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (4, 4), activation='relu', padding='same'))
    model.add(layers.MaxPool2D((2, 2)))

    # Second Convolution & MaxPooling
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPool2D((2, 2)))

    # Flattening
    model.add(layers.Flatten())

    model.add(layers.Dense(156, activation='relu'))
    model.add(layers.Dropout(0.3))

    # Last layer - Classification Layer with 43 outputs, each corresponding to a different traffic sign
    model.add(layers.Dense(43, activation='softmax'))

    # Model compilation
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


if __name__ == "__main__":

    main()
