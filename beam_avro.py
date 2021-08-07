import apache_beam as beam 
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.runners import DirectRunner, DataflowRunner
from apache_beam.transforms.combiners import Count
import logging
import argparse
import json
import datetime,time

def checkValueelement(element): 
    key = element[0]
    value = element[1]
    if (value != 1):
        return beam.pvalue.TaggedOutput("duplicates", element)

class CheckDupeTransform(beam.PTransform):
    def expand(self, pcol_element):
        count_per_keys = (pcol_element | "MapKeys" >> beam.Map(lambda x: (x["id"], x))
                                       | "CountPerKey" >> Count.PerKey()   
        )
        check_dupe_ids = (count_per_keys | "CountDuplicates" >> beam.FlatMap(checkValueelement).with_outputs())

        duplicate_records = check_dupe_ids.duplicates
        return duplicate_records


parser = argparse.ArgumentParser(description="Playing with Avro data in Beam")

#Google Cloud options
parser.add_argument("--runner", required=True, help="Please enter Apache Beam Runner")
parser.add_argument("--staging_location", required=True, help="Please enter staging GCS Bucket")
parser.add_argument("--temp_location", required=True, help="Please enter temporary GCS location")
parser.add_argument("--region", required=True, help="Please enter Apache Beam Runner")
parser.add_argument("--project", required=True, help="Please enter the GCP Project")

#Pipeline Specific Arguments
parser.add_argument("--input", required=True, help="Please enter the input GCS object path")
parser.add_argument("--output_bucket", required=True, help="Please enter the GCS bucket to write intermmidiate output")
parser.add_argument("--output_table", required=True, help="Please enter BQ table name")

opts, pipeline_opts = parser.parse_known_args()
options = PipelineOptions(pipeline_opts, save_main_session = True)
options.view_as(GoogleCloudOptions).project = opts.project
options.view_as(GoogleCloudOptions).region = opts.region
options.view_as(GoogleCloudOptions).staging_location = opts.staging_location
options.view_as(GoogleCloudOptions).temp_location = opts.temp_location
options.view_as(GoogleCloudOptions).runner = opts.runner
options.view_as(GoogleCloudOptions).job_name = f"avro-test-{time.time_ns()}"

input = opts.input
output_bucket = opts.output_bucket
output_table = opts.output_table

table_schema = {
        "fields": [

            {
                "name": "registration_dttm",
                "type": "TIMESTAMP"
            },
            {
                "name": "id",
                "type": "INTEGER"
            },
            {
                "name": "first_name",
                "type": "STRING"
            },
            {
                "name": "last_name",
                "type": "STRING"
            },
            {
                "name": "email",
                "type": "STRING"
            },
            {
                "name": "gender",
                "type": "STRING"
            },
            {
                "name": "ip_address",
                "type": "STRING"
            },
            {
                "name": "cc",
                "type": "INTEGER"
            },
            {
                "name": "country",
                "type": "STRING"
            },
            {
                "name": "birthdate",
                "type": "STRING"
            },
            {
                "name": "salary",
                "type": "FLOAT"
            },
            {
                "name": "title",
                "type": "STRING"
            },
            {
                "name": "comments",
                "type": "STRING"
            }
        ]
}

options = PipelineOptions(options=options)
with beam.Pipeline(options = options) as p:
    avro_records = (p 
                    | "ReadAvroRecords" >> beam.io.ReadFromAvro(input)
                    #| "WriteAsText" >> beam.io.WriteToText(output)
    )

    dupe_ids = (avro_records | "CheckDupeIds" >> CheckDupeTransform())

    write_dupe_ids = dupe_ids | "WriteAsText" >> beam.io.WriteToText(output_bucket, file_name_suffix=".txt")

    write_to_bq = (avro_records | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
        output_table,
        schema=table_schema,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
    )
    )