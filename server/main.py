import json
import os
from flask import Flask, Response
from flask import request
from flask_cors import CORS

from bot_server import BotServer
from google_cloud.storage import save_to_storage
from human_server import HumanServer

VERSION = '1.6.2_e' # TODO: tmp version of english only for friends
cs_strategy = "goldfish"

app = Flask(__name__)
CORS(app)

human_server = HumanServer()
bot_server = BotServer(cs_strategy)

game_roles = {'navigator': 0, 'instructor': 1}
game_roles_reverse = {0: 'navigator', 1: 'instructor'}


@app.route('/api/v1/call_bot', methods=['POST'])
def call_bot():
    try:
        params = request.get_json()
        res = bot_server.call_bot(params['guid'], params['msg'],
                                  params['map_index'], params['state'])
        return json.dumps({'res': res}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print('err:', e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/call_human', methods=['POST'])
def call_human():
    try:
        params = request.get_json()
        id_ = params['id']
        guid_ = params['guid']
        msg = params['msg']
        to_other_msg = f"{guid_}__{id_}__{msg}__dummy"
        human_server.announce(to_other_msg, guid_)
        return '', 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print('err:', e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/notify_end_human', methods=['POST'])
def notify_end_human():
    try:
        params = request.get_json()
        id_ = params['id']
        guid_ = params['guid']
        to_other_msg = f"{guid_}__{id_}__dummy__end"
        human_server.announce(to_other_msg, guid_)
        return '', 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print('err:', e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/event')
def event():
    guid = request.args.get('guid')

    def stream(guid: str):
        messages = human_server.listen(guid)  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(guid), mimetype='text/event-stream')


@app.route('/api/v1/register', methods=['POST'])
def register():
    try:
        params = request.get_json()

        game_mode = params['mode']
        map_index = params['map_index']
        if game_mode not in ['bot', 'human']:
            raise Exception('Invalid game mode')

        resp = {'version': VERSION}
        if game_mode == 'bot':
            resp['role'] = game_roles['navigator']
            guid = bot_server.register(map_index)
            resp['guid'] = guid
        elif game_mode == 'human':
            role, guid = human_server.assign_role_api(map_index)
            resp['role'] = game_roles[role]
            resp['guid'] = guid
        return resp, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print('err:', e)
        return "Server error", 500, {'Content-Type': 'application/json'}


@app.route('/api/v1/upload', methods=['POST'])
def upload_api():
    try:
        params = request.get_json()
        if 'guid' not in params:
            raise Exception('Missing guid!')
        if params['game_config']['game_mode'] == 'human':
            upload_data = human_server.upload(params)
        else:
            upload_data = params
            bot_server.un_register(params['guid'])
            upload_data['cs_strategy'] = cs_strategy

        if upload_data is not None:
            chat = upload_data['chat']
            for c in chat:
                c['id'] = game_roles_reverse[c['id']]
            if 'game_role' in upload_data['game_config']:
                upload_data['game_config']['game_role'] = game_roles_reverse[upload_data['game_config']['game_role']]

            upload_data['server_version'] = VERSION
            save_to_storage(upload_data)
        return '', 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print('err:', e)
        return "Server error", 500, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
