import unittest
from unittest.mock import patch, MagicMock

from src.aws.manager import (
    upload_file,
    translate_text,
    get_translated_text,
    save_file,
    delete_file,
)


class TestManager(unittest.TestCase):
    @patch("boto3.client")
    def test_upload_file(self, mock_boto_client):
        s3_client_mock = MagicMock()
        mock_boto_client.return_value = s3_client_mock

        upload_file("output_file.mp3")

        s3_client_mock.upload_file.assert_called_once_with(
            "output_file.mp3", "maris333", "output_file.mp3"
        )

    @patch("boto3.client")
    def test_translate_text(self, mock_boto_client):
        translate_client_mock = MagicMock()
        mock_boto_client.return_value = translate_client_mock

        translate_text("Hello", "en", "es")

        translate_client_mock.translate_text.assert_called_once_with(
            Text="Hello", SourceLanguageCode="en", TargetLanguageCode="es"
        )

    @patch("boto3.client")
    def test_get_translated_text(self, mock_boto_client):
        polly_client_mock = MagicMock()
        mock_boto_client.return_value = polly_client_mock

        get_translated_text("Hola")

        polly_client_mock.synthesize_speech.assert_called_once_with(
            Text="Hola", OutputFormat="mp3", VoiceId="Joanna"
        )

    @patch("builtins.open", create=True)
    def test_save_file(self, mock_open):
        response_mock = MagicMock()
        response_mock["AudioStream"].read.return_value = b"mock_audio_data"

        output_file = save_file(response_mock, "filename")

        mock_open.assert_called_once_with("src/files/filename.mp3", "wb")
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_once_with(b"mock_audio_data")

        self.assertEqual(output_file, "src/files/filename.mp3")

    @patch("os.remove")
    def test_delete_file(self, mock_os_remove):
        delete_file("filename")

        mock_os_remove.assert_called_once_with("src/files/filename.mp3")
