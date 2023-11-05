import boto3
from decouple import config

aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
aws_region = config('aws_region')
s3_bucket_name = config('s3_bucket_name')


def upload_file(output_file, s3_client):
    s3_client.upload_file(output_file, s3_bucket_name, output_file)


def save_file(response):
    output_file = 'output.mp3'
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())
    return output_file


def translate_text(text, source_language, target_language):
    translate_client = boto3.client('translate', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response['TranslatedText']


def get_translated_text(translated_text):
    polly_client = boto3.client('polly', aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                             region_name=aws_region)

    response = polly_client.synthesize_speech(
        Text=translated_text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    return response, s3_client
