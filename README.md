# install
- client:
  install node/npm: https://nodejs.org/en/download/
- server:
  install python 3.7+
  pip install -r requirements

# Run
- client:
  * first time go to client folder:
    run: "npm install --global yarn"
    run: "yarn install"
  * to run locally - go to client folder:
    run: 'yarn start'
- server:
  * local run without the web client - run local.py
  * local run with the web client - run main.py
