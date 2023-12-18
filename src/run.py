from src import create_app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000, host="0.0.0.0")
