import os
import boto3
from src.config import AWSConfig


def upload_file(output_file):
    """
    Uploads a file to an AWS S3 bucket.

    Parameters:
    - output_file (str): The local file path to be uploaded.

    Returns:
    - None
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWSConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWSConfig.AWS_SECRET_KEY_ACCESS,
        region_name=AWSConfig.AWS_REGION,
    )
    s3_client.upload_file(output_file, AWSConfig.S3_BUCKET_NAME, output_file)


def save_file(response, filename):
    """
    Saves the audio response from AWS Polly to a local file.

    Parameters:
    - response (dict): The AWS Polly response containing an "AudioStream".
    - filename (str): The desired filename for the saved file.

    Returns:
    - str: The local file path where the file is saved.
    """
    output_file = f"src/files/{filename}.mp3"
    with open(output_file, "wb") as f:
        f.write(response["AudioStream"].read())
    return output_file


def delete_file(filename):
    """
    Deletes a local file.

    Parameters:
    - filename (str): The filename to be deleted.

    Returns:
    - None
    """
    output_file = f"src/files/{filename}.mp3"
    try:
        os.remove(output_file)
    except OSError as e:
        print(f"Error deleting file {output_file}: {e}")
    else:
        print(f"File {output_file} deleted successfully")


def translate_text(text, source_language, target_language):
    """
    Translates text from a source language to a target language using AWS Translate.

    Parameters:
    - text (str): The text to be translated.
    - source_language (str): The source language code.
    - target_language (str): The target language code.

    Returns:
    - str: The translated text.
    """
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=AWSConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWSConfig.AWS_SECRET_KEY_ACCESS,
        region_name=AWSConfig.AWS_REGION,
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return response["TranslatedText"]


def get_translated_text(translated_text):
    """
    Synthesizes speech from translated text using AWS Polly.

    Parameters:
    - translated_text (str): The translated text.

    Returns:
    - dict: The AWS Polly response containing the synthesized speech.
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=AWSConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWSConfig.AWS_SECRET_KEY_ACCESS,
        region_name=AWSConfig.AWS_REGION,
    )

    response = polly_client.synthesize_speech(
        Text=translated_text, OutputFormat="mp3", VoiceId="Joanna"
    )

    return response
