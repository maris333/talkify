"""
This module contains routes and functions for a Flask application that utilizes AWS services
for file management and translation functionalities.
"""

import random
import string

import boto3
from flask import request, render_template, Blueprint, redirect
from flask_login import login_required, current_user

from src import db
from src.aws.manager import (
    upload_file,
    save_file,
    translate_text,
    get_translated_text,
    delete_file,
)
from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_KEY_ACCESS,
    AWS_REGION,
    S3_BUCKET_NAME,
)
from src.models.auth import Files

translate_blueprint = Blueprint("translate", __name__)
index_blueprint = Blueprint("index", __name__)
download_blueprint = Blueprint("download", __name__)
download_file_blueprint = Blueprint("download_file", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
def index():
    """
    Route for the home page.

    Returns:
    - str: The rendered HTML for the home page.
    """
    return render_template("index.html")


@translate_blueprint.route("/translate", methods=["GET", "POST"])
@login_required
def translate():
    """
    Route for translating text.

    Returns:
    - str: The rendered HTML for the translation page.
    """
    if request.method == "GET":
        return render_template("translate.html")

    text_to_convert = request.form["text_to_convert"]
    source_language = request.form["source_language"]
    target_language = request.form["target_language"]

    translated_text = translate_text(text_to_convert, source_language, target_language)

    response = get_translated_text(translated_text)

    letters = string.ascii_lowercase
    filename = "".join(random.choice(letters) for i in range(32))
    output_file = save_file(response, filename=filename)

    file_record = Files(filename=filename, user_id=current_user.id)
    db.session.add(file_record)
    db.session.commit()

    upload_file(output_file)
    delete_file(filename)

    return render_template("translate.html")


@download_blueprint.route("/download", methods=["GET"])
@login_required
def download():
    """
    Route for displaying a user's files for download.

    Returns:
    - str: The rendered HTML for the download page.
    """
    user_files = Files.query.filter_by(user_id=current_user.id).all()
    return render_template("download.html", user_files=user_files)


@download_file_blueprint.route("/download/<filename>", methods=["GET"])
@login_required
def download_file(filename):
    """
    Route for downloading a specific file.

    Parameters:
    - filename (str): The filename to be downloaded.

    Returns:
    - str or redirect: Either a redirect to the presigned URL for the file or an error message.
    """
    file_record = Files.query.filter_by(
        user_id=current_user.id, filename=filename
    ).first()

    if file_record:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY_ACCESS,
            region_name=AWS_REGION,
            config=boto3.session.Config(signature_version="s3v4"),
        )
        bucket_name = S3_BUCKET_NAME
        object_key = f"src/files/{filename}.mp3"

        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
        return redirect(presigned_url)

    return "Unauthorized access.", 403
