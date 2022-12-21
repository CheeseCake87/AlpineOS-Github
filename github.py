import os

from dotenv import load_dotenv
from flask import Flask, request

from setup import stop_supervisor, start_supervisor
from utils.github import Github

load_dotenv()

git = os.getenv("GIT")

github = Github(git)


def create_app():
    app = Flask(__name__)

    # Index
    @app.post('/')
    def webhook():
        if request.method == 'POST':
            json = request.json
            clone_url = json['repository']['clone_url']
            if clone_url == git:
                stop_supervisor("repo")
                github.pull()
                start_supervisor("repo")
            return 'ok', 200

    return app


if __name__ == "__main__":
    create_app().run(port=5500, host="0.0.0.0")
else:
    sgi = create_app()
