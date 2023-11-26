import random
import string

from flask import request, render_template, Blueprint
from flask_login import login_required, current_user

from src import db
from src.aws.manager import upload_file, save_file, translate_text, get_translated_text, delete_file
from src.models.auth import Files

translate_blueprint = Blueprint("translate", __name__)
index_blueprint = Blueprint("index", __name__)


@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@translate_blueprint.route('/translate', methods=['GET', 'POST'])
@login_required
def translate():
    if request.method == 'GET':
        return render_template('translate.html')

    text_to_convert = request.form['text_to_convert']
    source_language = request.form['source_language']
    target_language = request.form['target_language']

    translated_text = translate_text(text_to_convert, source_language, target_language)

    response = get_translated_text(translated_text)

    letters = string.ascii_lowercase
    filename = ''.join(random.choice(letters) for i in range(32))
    output_file = save_file(response, filename=filename)

    file_record = Files(filename=filename, user_id=current_user.id)
    db.session.add(file_record)
    db.session.commit()

    upload_file(output_file)
    delete_file(filename)

    return render_template("translate.html", msg=f'https://s3.console.aws.amazon.com/s3/object/maris333?region=eu-north-1&prefix={output_file}')