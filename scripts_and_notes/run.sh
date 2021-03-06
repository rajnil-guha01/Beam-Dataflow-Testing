export PROJECT_ID=<>
export RUNNER=DataflowRunner
export TEMP_LOCATION=gs://dataflow-projects/tmp
export STAGING_LOCATION=gs://dataflow-projects/tmp
export REGION=us-central1
export INPUT_FILE=<>
export OUTPUT_BUCKET=gs://deadletter-sink/duplicate-records
export OUTPUT_TABLE=my_test_dataset.users_history

python beam_avro.py --project=$PROJECT_ID \
--runner=$RUNNER \
--temp_location=$TEMP_LOCATION \
--staging_location=$STAGING_LOCATION \
--region=$REGION \
--setup_file ./setup.py  \
--input=$INPUT_FILE \
--output_bucket=$OUTPUT_BUCKET \
--output_table=$OUTPUT_TABLE
