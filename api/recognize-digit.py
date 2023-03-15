import base64
import cv2
import json
import numpy as np
import tensorflow as tf

from http.server import BaseHTTPRequestHandler

_MODEL_PATH = 'modeling/mnist/models/saved_model'
_TFLITE_MODEL_PATH = 'modeling/mnist/models/model.tflite'


def prepare_image(img):
  """Prepares an image for the model.
  
  The model accepts 28x28 grayscale float32 images that have been normalized
  between 0 and 1.
  """
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  resized_image = cv2.resize(gray, (28, 28))
  resized_image = resized_image.astype(np.float32)
  resized_image = (255 - resized_image)
  resized_image /= 255
  return resized_image


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    content_len = int(self.headers.get('Content-Length'))
    post_body = self.rfile.read(content_len)
    # The POST body contains the entire data URL. This gets just the encoded
    # data portion.
    encoded_data = post_body.decode('utf-8').split('base64,')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = prepare_image(img)
    predictions = self.call_model(img)
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(json.dumps(predictions.tolist()).encode('utf-8'))

  def call_model(self, img):
    """Runs prediction on the TensorFlow saved model."""
    model = tf.keras.models.load_model(_MODEL_PATH, compile=False)
    predictions = model.predict(np.expand_dims(img, 0))
    return predictions[0]

  def call_tflite_model(self, img):
    self._interpreter = tf.lite.Interpreter(model_path=_TFLITE_MODEL_PATH,
                                            num_threads=2)
    input_details = self._interpreter.get_input_details()
    output_details = self._interpreter.get_output_details()
    self._interpreter.allocate_tensors()
    self._interpreter.set_tensor(input_details[0]['index'], [img])
    self._interpreter.invoke()
    predictions = self._interpreter.get_tensor(output_details[0]['index'])
    return predictions[0]
