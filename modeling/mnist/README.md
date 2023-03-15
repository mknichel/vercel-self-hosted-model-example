# MNIST Model

This directory trains a model to recognize handwritten digits based off of the
MNIST dataset. It is the basic example that can be found at
https://www.tensorflow.org/datasets/keras_example.

## Training the model

This directory uses `pipenv` to install Python dependencies and run the
training script. See https://pipenv-fork.readthedocs.io/en/latest/basics.html
for more details.

First, install `pipenv`:

```bash
pip install --user pipenv
```

Install the Python dependencies needed for the package:

```bash
pipenv install
```

Then run the training script:

```bash
pipenv run python train.py
```

The model will be saved to `modeling/mnist/models/model.tflite`.

A TensorFlow Lite model will be saved because of restrictions in running
TensorFlow models on Vercel serverless functions. See
[api/README.md](/api/README.md) for more information.
