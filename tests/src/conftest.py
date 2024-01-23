import pytest
from src import create_app, db
from src.models.auth import User
from src.models.files import Files


def prepare_db(app):
    test_user = User(id=1, username="testuser", password="testpassword")

    filename = "example"
    file_record = Files(filename=filename, user_id=test_user.id)
    with app.app_context():
        db.session.add(file_record)
        db.session.add(test_user)
        db.session.commit()


@pytest.fixture()
def my_app():
    app = create_app(is_under_tests=True)
    app.config.update({"TESTING": True})
    prepare_db(app)

    yield app

    with app.app_context():
        db.session.remove()
        db.session.commit()
        db.drop_all()
        db.create_all()


@pytest.fixture()
def client(my_app):
    return my_app.test_client(use_cookies=True)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
