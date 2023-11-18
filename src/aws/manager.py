import boto3

from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY_ACCESS, AWS_REGION, S3_BUCKET_NAME


def upload_file(output_file):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY_ACCESS,
                             region_name=AWS_REGION)
    s3_client.upload_file(output_file, S3_BUCKET_NAME, output_file)


def save_file(response):
    output_file = '../../output.mp3'
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())
    return output_file


def translate_text(text, source_language, target_language):
    translate_client = boto3.client('translate', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_KEY_ACCESS, region_name=AWS_REGION)

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response['TranslatedText']


def get_translated_text(translated_text):
    polly_client = boto3.client('polly', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_KEY_ACCESS, region_name=AWS_REGION)

    response = polly_client.synthesize_speech(
        Text=translated_text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    return response
