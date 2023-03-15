# Model Request Handler

This directory contains the code for the request handler that takes the image
and runs the MNIST digit recognition model. It is based off of
https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python.

The `Pipfile` is used to define the dependent packages needed to run the
models. To get started, follow the documentation for `pipenv` at
https://pipenv-fork.readthedocs.io/en/latest/basics.html. This is needed by
Vercel when deploying to production.

Vercel serverless functions are limited to 50MB in size. The `tensorflow` and
`opencv-python` packages are too large to run on serverless. Instead, the
`tflite_runtime` and `pillow` packages are used which, when combined with the
rest of this code, only come out to ~29MB in size, far below the limit.

Additionally, you must use version `2.7.0` or below of the `tflite_runtime`
package on Vercel. Newer versions require a `glibc` that isn't available and
you will get this error:

```
[ERROR] Runtime.ImportModuleError: Unable to import module 'vc__handler__python': /lib64/libm.so.6: version `GLIBC_2.27' not found (required by /var/task/tflite_runtime/_pywrap_tensorflow_interpreter_wrapper.so)
Traceback (most recent call last):
```
