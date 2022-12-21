apk update &&
apk upgrade &&
apk add python3 &&
apk add python3-dev &&
apk add py3-pip &&
apk add musl-dev &&
apk add g++ &&
apk add supervisor &&
rc-update add supervisord boot &&
python3 -m pip install python-dotenv