# install
- client:
  install node/npm: https://nodejs.org/en/download/
- server:
  install python 3.7+
  pip install -r requirements

# Run
- client:
  * first time and on every git pull run on cmd: 'npm install' in client/ dir
  * run on cmd: 'npm start' in client/ dir
- server:
  * local run without the web client - run local.py
  * local run with the web client - run main.py
