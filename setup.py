import os
import pathlib
import subprocess

from utils import SupervisorConfig, Supervisor


def setup_supervisor():
    from dotenv import load_dotenv

    load_dotenv()

    log_folder = pathlib.Path(pathlib.Path.cwd() / "logs")

    if not log_folder.exists():
        log_folder.mkdir()

    github_config = SupervisorConfig(
        program="github",
        program_root_path=pathlib.Path(pathlib.Path.cwd()),
        log_path=log_folder,
        command=f"{pathlib.Path.cwd()}/venv/bin/python github.py",
        user="root"
    )
    repo_config = SupervisorConfig(
        program="repo",
        program_root_path=pathlib.Path(pathlib.Path.cwd() / "repo"),
        log_path=log_folder,
        command=f"{pathlib.Path(pathlib.Path.cwd() / 'repo')}/venv/bin/gunicorn -b 0.0.0.0:5000 -w 3 run:sgi",
        user="root",
        auto_start="false"
    )
    Supervisor(
        main_config_location=os.getenv("SUPERVISOR_CONFIG", pathlib.Path("/etc/supervisord.conf")),
        config_files_folder=pathlib.Path(pathlib.Path.cwd() / "configs"),
        configs=[github_config, repo_config]
    )


def setup_venv(program_path: pathlib.Path):
    if not pathlib.Path(program_path, "venv").exists():
        subprocess.call(['python3', '-m', 'venv', f'{program_path}/venv'])
    subprocess.call([f'{program_path}/venv/bin/python3', '-m', 'pip', 'install', '-r', f'{program_path}/requirements.txt'])


def setup_alpine():
    subprocess.call([f'ash', 'sh/alpine.sh'])


def restart_supervisor(program: str):
    subprocess.call(['supervisorctl', 'restart', f'{program}'])


def stop_supervisor(program: str):
    subprocess.call(['supervisorctl', 'stop', f'{program}'])


def start_supervisor(program: str):
    subprocess.call(['supervisorctl', 'start', f'{program}'])


if __name__ == '__main__':
    setup_alpine()
    setup_venv(pathlib.Path(pathlib.Path.cwd()))
    setup_supervisor()
    restart_supervisor("github")
