from flask import request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, login_user, logout_user


from src.aws.manager import S3_BUCKET_NAME, upload_file, save_file, translate_text, get_translated_text


translate_blueprint = Blueprint("translate", __name__)
register_blueprint = Blueprint("register", __name__)
login_blueprint = Blueprint("login", __name__)
logout_blueprint = Blueprint("logout", __name__)
index_blueprint = Blueprint("index", __name__)


@translate_blueprint.route('/translate', methods=['GET', 'POST'])
@login_required
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

    return render_template('translate.html')


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    from src.forms.auth import RegistrationForm
    from src import db
    from src.models.auth import User
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login.login'))

    return render_template('register.html', form=form)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    from src.forms.auth import LoginForm
    from src.models.auth import User
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('translate.index'))
        else:
            return render_template('login.html', form=form, error='Invalid credentials')

    return render_template('login.html', form=form, error=None)


@logout_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
