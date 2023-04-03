import os
import json

from bots.rule_based.shared_utils import find_closest_object

input_folder = "C:/Users/t-deangeckt/OneDrive - Microsoft/Personal/HU/nlp_lab/code_and_data/map_task/data/rb_bot_navigator"


no_resp_prefix_navigator = ["i'm not sure what you mean",
                            "i didn't quite understand that",
                            "not too sure about that",]

kb_path = f'../rule_based/maps_kb/map_1.json'
with open(kb_path, 'r') as f:
    kb = json.load(f)
kb_abs = kb['absolute']
kb_path_order = list(kb_abs.keys())

def squash_chat(chat):
    """
    since rb bot can have multiple utterances in a turn - we squash it to 1 uter per turn
    so the chat is consistent - ins -> nav -> ins etc...
    also removing default answer of the rb bot
    """
    squash_chat_ = []
    curr_nav_msg = ''
    for chat_obj in chat:
        id_ = chat_obj['id']
        if id_ == 'instructor':
            squash_chat_.append({"id": "navigator", "msg": curr_nav_msg.strip()})
            curr_nav_msg = ''
            squash_chat_.append(chat_obj)
        else:
            msg = chat_obj['msg'].lower()
            if msg in no_resp_prefix_navigator or msg[:len(msg)-1] in no_resp_prefix_navigator:
                continue
            curr_nav_msg += f'{msg} '

    if curr_nav_msg != '':
        squash_chat_.append({"id": "navigator", "msg": curr_nav_msg.strip()})

    return squash_chat_
def vectors_in_window(arr):
    k = 5  # context / window size
    min = 3  # keep the starting vectors of each uter

    result = [arr[0:min+i] for i in range(k-min)]
    result.extend([arr[i:i+k] for i in range(len(arr)-k+1)])
    return result
def parse_chat(chat):
    splits = vectors_in_window(chat)
    data_samples = []

    for split in splits:
        last_turn = split[-1]
        if last_turn['id'] == 'instructor':
            continue

        response = last_turn['msg']

        # last_turn_ins = split[-2]
        knowledge = f''

        context = []
        for idx, turn in enumerate(split):
            if idx == len(split) - 1:
                continue
            ctx_id = 'User:' if turn['id'] == 'instructor' else 'System:'
            msg = turn['msg']
            context.append(f'{ctx_id} {msg}')

        data_samples.append({'Context': context, 'Knowledge': knowledge, 'Response': response})

    return data_samples
def save_jsonl(data, filename):
    with open(filename, 'w') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n')


train_samples = []
val_samples = []
test_samples = []
val_files = ['32788f75-1c65-4fed-a6ef-20ee6499d597.json']
test_files = ['7710c3d7-aa15-4362-8b75-0a58931b24eb.json']


for file_name in os.listdir(input_folder):
    if not file_name.endswith('json'):
        continue
    with open(os.path.join(input_folder, file_name), encoding='utf8') as json_file:
        data = json.load(json_file)

    map_idx = data['map_metadata']['map_idx']
    if map_idx != 0:
        continue
    chat = data['chat']
    if len(chat) < 3:
        continue

    print(file_name)
    print('chat len orig', len(chat))
    chat = squash_chat(chat)
    print('sq chat len:', len(chat))
    samples = parse_chat(chat)
    print('samples:', len(samples))
    print()

    if file_name in val_files:
        val_samples.extend(samples)
    elif file_name in test_files:
        test_samples.extend(samples)
    else:
        train_samples.extend(samples)

print('train', len(train_samples))
print('test', len(test_samples))
print('val', len(val_samples))

save_jsonl(train_samples, 'nav_train.json')
save_jsonl(val_samples, 'nav_val.json')
save_jsonl(test_samples, 'nav_test.json')


