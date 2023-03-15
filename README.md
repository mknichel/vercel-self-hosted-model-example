# Example of using a self hosted TensorFlow model with Vercel

This repository shows an example of using a self trained and hosted TensorFlow
model running entirely on Vercel. In this example, you will build a TensorFlow
model for recognizing handwritten digits based off the MNIST dataset.

It's not recommended to self host your own
ML model, but this can be a convenient way to iterate on modeling while having
a web application to interact with the results of the model.

## Introduction

This example has three pieces:

- A TensorFlow Keras model trained in the `modeling/mnist` directory
- A Vercel serverless API route using the Python runtime
- A Next.js web application where you can draw digits and call the API route
  to view the results of the model.

## Getting started

### Training the model

First, the TensorFlow model needs to be trained.

```sh
cd modeling/mnist
```

and follow the instructions in the [Modeling README](/modeling/mnist/README.md).

### Running the server

After the model has been trained, run the server in the root of the repository:

```sh
vercel dev
```
