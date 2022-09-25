import json
import os

from flask import Flask, Response
from flask import request
from flask_cors import CORS

from bots.rule_based.rule_based_bot import ruleBasedBot
from human_to_human_server import Server

app = Flask(__name__)
CORS(app)

chat_bot = ruleBasedBot()
server = Server()


@app.route('/api/v1/call_bot', methods=['POST'])
def call_bot():
    try:
        params = request.get_json()
        res = chat_bot.call(params['msg'], params['state'])
        return json.dumps({'res': res}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/call_human', methods=['POST'])
def call_human():
    try:
        params = request.get_json()
        id_ = params['id']
        msg = params['message']
        to_other_msg = f"{id_}__{msg}"
        server.announce(to_other_msg)
        return '', 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/event')
def event():
    def stream():
        messages = server.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


@app.route('/api/v1/assign_roles', methods=['GET'])
def health():
    role = server.assign_role_api()
    return json.dumps({'res': role}), 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
