import os

from dotenv import load_dotenv

from utils.github import Github

load_dotenv()

github = Github(os.getenv("GIT"))

github.pull()
