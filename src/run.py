









if __name__ == '__main__':
    from src.views.views import index_blueprint, register_blueprint, login_blueprint, logout_blueprint, \
        translate_blueprint
    from src import app, db

    with app.app_context():
        app.register_blueprint(index_blueprint)
        app.register_blueprint(register_blueprint)
        app.register_blueprint(login_blueprint)
        app.register_blueprint(logout_blueprint)
        app.register_blueprint(translate_blueprint)
        db.init_app(app)
        db.create_all()
    app.run(debug=True, port=4000)
