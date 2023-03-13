import os

import apache_beam as beam
from apache_beam.testing import util as beam_test_util
import tensorflow as tf
import pandas as pd
import numpy as np

import tensorflow_transform as tft
from tensorflow_transform.beam import tft_unit
from tensorflow_transform.beam.tft_beam_io import beam_metadata_io
from tensorflow_transform.beam.tft_beam_io import transform_fn_io
from tensorflow_transform.beam.tft_beam_io import test_metadata
from tensorflow_transform.tf_metadata import metadata_io

from tensorflow.python.lib.io import file_io

path = 'C:\\Users\\ottok\\OneDrive\\Dokument\\ai'
# NOTE: we don't need to create or write to the transform_fn directory since
# ReadTransformFn never inspects this directory.
transform_fn_dir = os.path.join(
    path, tft.TFTransformOutput.TRANSFORM_FN_DIR)
transformed_metadata_dir = os.path.join(
    path, tft.TFTransformOutput.TRANSFORMED_METADATA_DIR)

print(transform_fn_dir)
print(transformed_metadata_dir)
with beam.Pipeline() as pipeline:
    saved_model_dir_pcoll, metadata = (
        pipeline | transform_fn_io.ReadTransformFn(path))
    beam_test_util.assert_that(
        saved_model_dir_pcoll,
        beam_test_util.equal_to([transform_fn_dir]),
        label='AssertSavedModelDir')

dataset = tf.data.TFRecordDataset(
    ['C:\\Users\\ottok\\OneDrive\\Dokument\\ai\\train_transformed-00000-of-00001'])  # here you can use multiple tfrecords file


def parse_df_element(element):
    parser = {
        'ai_industry': tf.io.VarLenFeature(tf.int64),
        'ai_locations': tf.io.VarLenFeature(tf.int64),
        'ai_technology': tf.io.VarLenFeature(tf.int64),
        'employer': tf.io.VarLenFeature(tf.int64),
        'headline': tf.io.VarLenFeature(tf.int64),
        'occupation': tf.io.VarLenFeature(tf.int64)
    }
    # create an example:

    # content = tf.io.parse_single_example(element, parser)
    content = tf.io.parse_sequence_example(element, parser)
    # return content['employer'], \
    # content['ai_industry'], content['ai_locations'], content['ai_technology'], content['headline'], content['occupation']
    return content


parsed_tf_records = dataset.map(parse_df_element)
print(parsed_tf_records)
df = pd.DataFrame(
    parsed_tf_records.as_numpy_iterator(),
    columns=['ai_industry', 'ai_locations',
             'ai_technology', 'headline', 'occupation', 'employer']
)
print(df)
df.to_csv('C:\\Users\\ottok\\OneDrive\\Dokument\\ai\\intspo2.csv', index=False)

print(df)
# numpy_dataset = np.array(list(parsed_tf_records.as_numpy_iterator()))
# print(numpy_dataset)
# np.savetxt('C:\\Users\\ottok\\OneDrive\\Dokument\\ai\\intspo.csv',
#            numpy_dataset, delimiter=',')
