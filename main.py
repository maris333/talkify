from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    from views import index_blueprint
    app.register_blueprint(index_blueprint)
    app.run(debug=True)
