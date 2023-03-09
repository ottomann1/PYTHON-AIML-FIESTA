import tensorflow as tf
from tensorflow_transform.tf_metadata import schema_utils

# Define the features and their types
text_feature = tf.feature_column.categorical_column_with_identity(
    key="text", num_buckets=10000)
label_feature = tf.feature_column.numeric_column(key="label")

# Define the feature spec
feature_spec = {
    "text": text_feature,
    "label": label_feature,
}

# Create the schema from the feature spec
schema = schema_utils.schema_from_feature_spec(feature_spec)

# Write the schema to a file
schema_utils.write_schema_text(schema, "schema.pbtxt")
