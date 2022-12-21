import os
import pathlib
from dataclasses import dataclass

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

    def pull(self):
        stop_supervisor("repo")
        self.repo.remotes.origin.pull()
        setup_venv(self.repo_folder)
        start_supervisor("repo")


@dataclass
class SupervisorConfig:
    program: str
    program_root_path: pathlib.Path
    log_path: pathlib.Path
    command: str
    user: str


class Supervisor:
    main_config_location: pathlib.Path
    config_files_folder: pathlib.Path

    def __init__(
            self,
            main_config_location: pathlib.Path = pathlib.Path("/etc/supervisord.conf"),
            config_files_folder: pathlib.Path = pathlib.Path(pathlib.Path.cwd() / "configs"),
            configs: list[SupervisorConfig] = None
    ):
        self.main_config_location = main_config_location
        self.config_files_folder = config_files_folder
        self._check_main_config()
        if configs:
            for config in configs:
                self.write_config(config)

    def _check_main_config(self):
        if not self.main_config_location.exists():
            raise FileNotFoundError(f"Supervisor config file not found at {self.main_config_location}")
        if not self.config_files_folder.exists():
            self.config_files_folder.mkdir()
        with open(self.main_config_location, "r") as f:
            if self.config_files_folder.name in f.read():
                return
        with open(self.main_config_location, "w") as f:
            f.write(f"""
[unix_http_server]
file=/run/supervisord.sock

[supervisord]
logfile=/var/log/supervisord.log

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///run/supervisord.sock

[include]
files = {self.config_files_folder}/*.ini
            """.strip())

    def write_config(self, config: SupervisorConfig):
        with open(self.config_files_folder / f"{config.program}.ini", "w") as f:
            f.write((f"""
[program:{config.program}]
directory={config.program_root_path}
command={config.command}
user={config.user}
autostart=true
autorestart=true
stdout_logfile={config.log_path}/error.log
stderr_logfile={config.log_path}/general.log
            """.strip()))
