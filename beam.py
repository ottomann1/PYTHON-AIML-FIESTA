import argparse
import logging
import os
import datetime
import pprint
import tempfile
import fileinput

import tensorflow as tf
import tensorflow_transform as tft
import apache_beam as beam

from tensorflow_transform.beam import impl as beam_impl
from tensorflow_transform.tf_metadata import schema_utils
import tensorflow_transform.beam as tft_beam
from tfx_bsl.public import tfxio

# Define your preprocessing function


def preprocess(inputs):
    # Define your feature transformations using TensorFlow Transform
    transformed_features = {}
    transformed_features['employer'] = tft.compute_and_apply_vocabulary(
        inputs['employer'])
    transformed_features['headline'] = tft.compute_and_apply_vocabulary(
        inputs['headline'])
    transformed_features['occupation'] = tft.compute_and_apply_vocabulary(
        inputs['occupation'])
    transformed_features['ai_industry'] = tft.compute_and_apply_vocabulary(
        inputs['ai_industry'])
    transformed_features['ai_locations'] = tft.compute_and_apply_vocabulary(
        inputs['ai_locations'])
    transformed_features['ai_technology'] = tft.compute_and_apply_vocabulary(
        inputs['ai_technology'])

    return transformed_features


_RAW_DATA_METADATA = tft.DatasetMetadata.from_feature_spec({
    'employer': tf.io.FixedLenFeature([], tf.string),
    'headline': tf.io.FixedLenFeature([], tf.string),
    'occupation': tf.io.FixedLenFeature([], tf.string),
    'ai_industry': tf.io.VarLenFeature(tf.string),
    'ai_locations': tf.io.VarLenFeature(tf.string),
    'ai_technology': tf.io.VarLenFeature(tf.string)
}).schema

# Define the data types of the columns in your CSV file
record_defaults = [tf.string] * 6

ordered_csv_columns = [
    'employer', 'headline', 'occupation', 'ai_industry', 'ai_locations', 'ai_technology'
]

# Load your data as a tf.data.Dataset
# data = tf.data.experimental.CsvDataset(
#     'C:/Users/ottok/OneDrive/Dokument/ai/sposimplified3ksimplified.csv',
#     record_defaults=record_defaults,
#     header=True
# )
with beam.Pipeline() as pipeline:
    with tft_beam.Context(temp_dir=tempfile.mkdtemp()):
        csv_tfxio = tfxio.BeamRecordCsvTFXIO(
            physical_format='text',
            column_names=ordered_csv_columns,
            schema=_RAW_DATA_METADATA)
        raw_data = (
            pipeline
            | 'ReadTrainData' >> beam.io.ReadFromText(
                'C:/Users/ottok/OneDrive/Dokument/ai/sposimplified3ksimplified.csv', coder=beam.coders.BytesCoder())
            | 'FixCommasTrainData' >> beam.Map(
                lambda line: line.replace(b', ', b','))
            | 'DecodeTrainData' >> csv_tfxio.BeamSource())
        print(raw_data)
        raw_dataset = (raw_data, csv_tfxio.TensorAdapterConfig())
      # The TFXIO output format is chosen for improved performance.

        with tft_beam.Context(temp_dir=tempfile.mkdtemp()):
            transformed_dataset, transform_fn = (
                raw_dataset | tft_beam.AnalyzeAndTransformDataset(
                    preprocess, output_record_batches=True))

        transformed_data, transformed_metadata = transformed_dataset  # pylint: disable=unused-variable
        pprint.pprint(transformed_data)

        data = (
            transformed_dataset
            | 'EncodeTrainData' >> tft_beam.EncodeTransformedDataset()
            | 'WriteTrainData' >> beam.io.WriteToTFRecord(
              os.path.join('C:/Users/ottok/OneDrive/Dokument/ai', 'train_transformed')))
        print(transformed_dataset, 'THIS IS DATA PRINT XXXXXXXXX#########')

        _ = (
            transform_fn
            | 'WriteTransformFn' >> tft_beam.WriteTransformFn('C:/Users/ottok/OneDrive/Dokument/ai'))
