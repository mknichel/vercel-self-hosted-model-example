from PIL import Image
import base64
import io
import json
import numpy as np
import tflite_runtime.interpreter as tflite

from http.server import BaseHTTPRequestHandler

_TFLITE_MODEL_PATH = 'modeling/mnist/models/model.tflite'


def prepare_image(img):
  """Prepares an image for the model.
  
  The model accepts 28x28 grayscale float32 images that have been normalized
  between 0 and 1.
  """
  gray = img.convert('L')
  resized_image = gray.resize((28, 28))
  resized_image = np.array(resized_image)
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
    img = Image.open(io.BytesIO(base64.b64decode(encoded_data)))
    img = prepare_image(img)
    predictions = self.call_tflite_model(img)
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(json.dumps(predictions.tolist()).encode('utf-8'))

  def call_tflite_model(self, img):
    self._interpreter = tflite.Interpreter(model_path=_TFLITE_MODEL_PATH,
                                           num_threads=2)
    input_details = self._interpreter.get_input_details()
    output_details = self._interpreter.get_output_details()
    self._interpreter.allocate_tensors()
    self._interpreter.set_tensor(input_details[0]['index'], [img])
    self._interpreter.invoke()
    predictions = self._interpreter.get_tensor(output_details[0]['index'])
    return predictions[0]
