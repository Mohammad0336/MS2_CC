import argparse
import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class PredictDoFn(beam.DoFn):
    def process(self, metric_json_val):
        # Filter out all values containing None
        for key, value in list(metric_json_val.items()):
            if value is None:
                return  # Skip processing for this record

        # Read in values from json
        temp = float(metric_json_val['temperature'])
        pres = float(metric_json_val['pressure'])

        # Convert to imperial units
        pres_imp = pres / 6.895
        temp_imp = temp * 1.8 + 32

        # Create a new Result dict
        result = {
            'time': metric_json_val['time'],
            'pressure-psi': pres_imp,
            'temperature-fahrenheit': temp_imp,
            'pressure-kpa': metric_json_val['pressure'],
            'temperature-celsius': metric_json_val['temperature'],
        }

        # Return created dict to be made into json
        return [result]

def run(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # input args
    parser.add_argument('--input', dest='input', required=True, help='Input file to process.')
    parser.add_argument('--output', dest='output', required=True, help='Output file to write results to.')

    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        # read data from topic, convert dict to json
        images = (p
                  | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=known_args.input)
                  | "toDict" >> beam.Map(lambda x: json.loads(x)))

        # convert data values, return converted json
        converted = images | 'convert units' >> beam.ParDo(PredictDoFn())

        # write converted json to output topic
        converted | 'to byte' >> beam.Map(lambda x: json.dumps(x).encode('utf8')) | 'to Pub/sub' >> beam.io.WriteToPubSub(topic=known_args.output)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
