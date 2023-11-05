from flask import request, render_template, Blueprint

from aws_manager import s3_bucket_name, upload_file, save_file, translate_text, get_translated_text

index_blueprint = Blueprint("index", __name__)


@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_to_convert = request.form['text_to_convert']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        translated_text = translate_text(text_to_convert, source_language, target_language)

        response = get_translated_text(translated_text)

        output_file = save_file(response)

        upload_file(output_file)

        return f'MP3 file was converted and saved: s3://{s3_bucket_name}/{output_file}'

    return render_template('index.html')
