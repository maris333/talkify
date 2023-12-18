from decouple import config


class AWSConfig:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY_ACCESS = config("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = config("AWS_REGION")
    S3_BUCKET_NAME = config("S3_BUCKET_NAME")


class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"


class TestConfig:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_site.db"
    WTF_CSRF_ENABLED = False
