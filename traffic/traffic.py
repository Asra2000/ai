import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

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

    # plt.figure(figsize=(10,10))
    # for i in range(25):
    #     plt.subplot(5,5,i+1)
    #     plt.xticks([])
    #     plt.yticks([])
    #     plt.grid(False)
    #     plt.imshow(x_train[i])
    #     plt.xlabel(1)
    # plt.show()

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
    labels = []
    images = []
    path = next(os.walk(data_dir))[0]
    directores =  next(os.walk(data_dir))[1]
 
    for dir in directores:
        dir_path = os.path.join(path, dir)
        for filename in next(os.walk(dir_path))[2]:
            try:
                image = cv2.imread(os.path.join(dir_path, filename))
                resized_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                images.append(resized_image)
                labels.append(int(dir))
            except Exception as e:
                print(str(e))
   
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """ 
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 3x3 pool size
        layers.MaxPooling2D(pool_size=(2, 2)),
        
        layers.Conv2D(
            32, 3, activation="relu"
        ),

        # Max-pooling layer, using 3x3 pool size
        layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Flatten units
        layers.Flatten(),
        layers.Dropout(0.2),

        # Add a hidden layer with dropout
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.2),

        # Add an output layer with output units for all categories
        layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
