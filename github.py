import os

from dotenv import load_dotenv
from flask import Flask, request

from setup import restart_supervisor
from utils import Github

load_dotenv()

github = Github(os.getenv("GIT"))


def create_app():
    app = Flask(__name__)

    # Index
    @app.post('/')
    def webhook():
        if request.method == 'POST':
            github.pull()
            restart_supervisor("repo")
            return 'ok', 200

    return app


if __name__ == "__main__":
    create_app().run(port=5500, debug=True)
else:
    sgi = create_app()
