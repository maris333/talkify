from flask_testing import TestCase

from src import create_app, db
from src.models.auth import User


class TestYourApp(TestCase):
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        return app

    def setUp(self):
        db.create_all()
        test_user = User(username="testuser", password="testpassword")
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        data = {"username": "testuser1", "password": "testpassword1"}
        response = self.client.post("/register", data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/login", data=data)
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 200)

    def test_translate_route(self):
        self.client.post(
            "/login", data={"username": "testuser", "password": "testpassword"}
        )
        response = self.client.get("/translate")
        self.assertEqual(response.status_code, 200)

    def test_download_route(self):
        self.client.post(
            "/login", data={"username": "testuser", "password": "testpassword"}
        )
        response = self.client.get("/download")
        self.assertEqual(response.status_code, 200)

    def test_download_file_route(self):
        self.client.post(
            "/login", data={"username": "testuser", "password": "testpassword"}
        )
        filename = "example"
        response = self.client.get(f"/download/{filename}")
        self.assertEqual(response.status_code, 302)
