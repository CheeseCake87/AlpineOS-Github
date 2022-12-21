This project allows a Alpine Linux VPS to accept github webhooks to automate deployments.

This only works with public repos.

Deploy this repo to the vps using git clone, then create a `.env` file with the value of the git url `GIT="https://github.com/[repo]/[git].git"`

Run the sh script to install Alpine Linux dependencies:

`ash sh/alpine.sh`

Run the setup script that will clone the repo and configure supervisor:

`python3 setup.py`

restart the alpine vps

You can now point the nginx proxy to the following:

website: `domain.com` -> `ip:5000`

github webhook: `github.domain.com` -> `ip:5500`