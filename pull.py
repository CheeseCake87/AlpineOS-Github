import os

from dotenv import load_dotenv

from setup import stop_supervisor, start_supervisor
from utils.github import Github

load_dotenv()

github = Github(os.getenv("GIT"))

stop_supervisor("repo")
github.pull()
start_supervisor("repo")
