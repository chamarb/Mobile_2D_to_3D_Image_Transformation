import os
import tensorflow as tf
import keras_hub

# Set the Keras backend to JAX (if applicable)
os.environ["KERAS_BACKEND"] = "jax"

# Load the Backbone model from Keras Hub
model_name = "hf://google/paligemma2-3b-pt-448-keras"
backbone = keras_hub.models.Backbone.from_preset(model_name)

# Print model summary
backbone.summary()

# Converting a tf.Keras model to a TensorFlow Lite model.
converter = tf.lite.TFLiteConverter.from_keras_model(backbone)
tflite_model = converter.convert()

# Save the TF Lite model.
with tf.io.gfile.GFile('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted to TFLite and saved as 'model.tflite'")
