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
  * update models:
    bots/models/es_core_news_md-3.7.0/*
    bots/models/en_core_web_sm-3.7.1/*
    bots/models/spaeng-lid-lince/*
