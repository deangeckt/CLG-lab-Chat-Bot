import json
import os
import sys
import traceback
from flask import Flask
from flask import request
from flask_cors import CORS
from bots.rule_based.rule_based_bot import ruleBasedBot

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
chat_bot = ruleBasedBot()


@app.route('/api/v1/health', methods=['GET'])
def health():
    return json.dumps({'res': 200}), 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/call', methods=['POST'])
def run():
    try:
        params = request.get_json()
        res = chat_bot.call(params['msg'], params['state'])
        return json.dumps({'res': res}), 200, {'Content-Type': 'application/json'}
    except ValueError as e:
        return str(e), 505,
    except:
        exctype, _, exctb = sys.exc_info()
        print(str(traceback.format_tb(exctb)))
        return "", 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
