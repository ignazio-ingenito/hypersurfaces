"""Main Flask app."""
from webapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5090)

    # only for local development
    # app.run(host='127.0.0.1', port=8080)
