import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np


def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label


def main():
  (ds_train, ds_test), ds_info = tfds.load(
      'mnist',
      split=['train', 'test'],
      shuffle_files=True,
      as_supervised=True,
      with_info=True,
  )

  ds_train = ds_train.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
  ds_train = ds_train.cache()
  ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
  ds_train = ds_train.batch(128)
  ds_train = ds_train.prefetch(tf.data.AUTOTUNE)

  ds_test = ds_test.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
  ds_test = ds_test.batch(128)
  ds_test = ds_test.cache()
  ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

  model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10, activation='softmax')
  ])
  model.compile(
      optimizer=tf.keras.optimizers.Adam(0.001),
      loss=tf.keras.losses.SparseCategoricalCrossentropy(),
      metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
  )
  model.fit(
      ds_train,
      epochs=6,
      validation_data=ds_test,
  )
  print(np.argmax(model.predict(ds_test), axis=1).tolist())
  print(np.concatenate([y for x, y in ds_test], axis=0).tolist())
  print(np.concatenate([x for x, y in ds_test], axis=0).tolist()[0])

  model.save('./models/saved_model')

  converter = tf.lite.TFLiteConverter.from_keras_model(model)
  tflite_model = converter.convert()
  with open('./models/model.tflite', 'wb') as f:
    f.write(tflite_model)


if __name__ == '__main__':
  main()
