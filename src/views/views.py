from flask import request, render_template, Blueprint

from src.aws.manager import S3_BUCKET_NAME, upload_file, save_file, translate_text, get_translated_text

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

        return f'MP3 file was converted and saved: s3://{S3_BUCKET_NAME}/{output_file}'

    return render_template('index.html')


