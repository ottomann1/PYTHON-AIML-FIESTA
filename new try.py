import os

import apache_beam as beam
from apache_beam.testing import util as beam_test_util
import tensorflow as tf

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
    # NOTE: metadata is currently read in a non-deferred manner.
    self.assertEqual(metadata, test_metadata.COMPLETE_METADATA)
