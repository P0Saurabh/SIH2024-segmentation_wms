import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Set up GPU configuration
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)  # Enable GPU memory growth
        print(f"Using GPU: {gpus}")
    except RuntimeError as e:
        print(e)

# Load the pre-trained DeepLabV3+ model from TensorFlow Hub
MODEL_URL = "https://tfhub.dev/tensorflow/deeplabv3/1"
model = tf.keras.Sequential([tf.keras.layers.InputLayer(input_shape=[None, None, 3]),
                             tf.keras.layers.Rescaling(1./255),
                             tf.keras.models.load_model(MODEL_URL)])

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (513, 513))
    img = np.expand_dims(img_resized, axis=0)
    return img

def run_segmentation(image):
    return model.predict(image)

def postprocess_output(output):
    segmentation_map = np.argmax(output[0], axis=-1)
    return segmentation_map

def display_segmentation(image, segmentation_map):
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.subplot(1, 2, 2)
    plt.imshow(segmentation_map, cmap='gray')
    plt.title("Segmented Output")
    plt.show()

image_path = "path_to_your_image.jpg"
image = preprocess_image(image_path)
segmentation_output = run_segmentation(image)
segmentation_map = postprocess_output(segmentation_output)
display_segmentation(cv2.imread(image_path), segmentation_map)
