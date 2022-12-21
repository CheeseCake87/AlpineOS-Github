import os

from dotenv import load_dotenv

from setup import restart_supervisor
from utils.github import Github

load_dotenv()

github = Github(os.getenv("GIT"))

github.pull()
restart_supervisor("repo")
