from flask import Flask, render_template, request
import boto3
from decouple import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_to_convert = request.form['text_to_convert']

        aws_access_key_id = config('aws_access_key_id')
        aws_secret_access_key = config('aws_secret_access_key')
        aws_region = config('aws_region')
        s3_bucket_name = config('s3_bucket_name')

        polly_client = boto3.client('polly', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

        response = polly_client.synthesize_speech(
            Text=text_to_convert,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )

        output_file = 'output.mp3'
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())

        s3_client.upload_file(output_file, s3_bucket_name, output_file)

        return f'MP3 file was converted and saved: s3://{s3_bucket_name}/{output_file}'

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
