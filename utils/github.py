import os
import pathlib

from git import Repo

from setup import setup_venv, stop_supervisor, start_supervisor


class Github:
    github_repo_url: str
    repo_folder: pathlib.Path
    repo: Repo

    def __init__(self, github_repo: str):
        self.github_repo_url = github_repo
        self.repo_folder = pathlib.Path(pathlib.Path.cwd() / "repo")
        self.repo_folder.mkdir(exist_ok=True)
        self.clone()
        self.repo = Repo(self.repo_folder)

    def clone(self):
        if len(os.listdir(self.repo_folder)) == 0:
            Repo.clone_from(self.github_repo_url, self.repo_folder)
            setup_venv(self.repo_folder)
            start_supervisor("repo")

    def pull(self):
        stop_supervisor("repo")
        self.repo.remotes.origin.pull()
        setup_venv(self.repo_folder)
        start_supervisor("repo")
