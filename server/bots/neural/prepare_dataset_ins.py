import os
import json

from bots.rule_based.shared_utils import find_closest_object

input_folder = "C:/Users/t-deangeckt/OneDrive - Microsoft/Personal/HU/nlp_lab/code_and_data/map_task/data/rb_bot_instructor"
ex = ['english_ex_new_survey_feb_23',
      'english_ex_friends_jan_23',
      'english_self_for_dataset']

no_resp_prefix_instructor = ["i'm not sure what you mean but maybe this will help",
                               "not too sure about that, but maybe this will help",
                               "mmm... just...",
                               "well, maybe...",
                               "let me clarify myself",
                               "let me rephrase that",
                               "i meant"]

kb_path = f'../rule_based/maps_kb/map_1.json'
with open(kb_path, 'r') as f:
    kb = json.load(f)
kb_abs = kb['absolute']
kb_path_order = list(kb_abs.keys())

def squash_chat(chat):
    """
    since rb ins bot can have multiple utterances in a turn - we squash it to 1 uter per turn
    so the chat is consistent - ins -> nav -> ins etc...
    also removing default answer of the rb bot
    """
    squash_chat_ = []
    curr_ins_msg = ''
    for chat_obj in chat:
        id_ = chat_obj['id']
        if id_ == 'navigator':
            squash_chat_.append({"id": "instructor", "msg": curr_ins_msg.strip()})
            curr_ins_msg = ''
            squash_chat_.append(chat_obj)
        else:
            msg = chat_obj['msg'].lower()
            if msg in no_resp_prefix_instructor or msg[:len(msg)-1] in no_resp_prefix_instructor:
                continue
            curr_ins_msg += f'{msg} '

    if curr_ins_msg != '':
        squash_chat_.append({"id": "instructor", "msg": curr_ins_msg.strip()})

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
        if last_turn['id'] == 'navigator':
            continue

        response = last_turn['msg']

        last_turn_nav = split[-2]
        curr_nav_cell = last_turn_nav['curr_nav_cell']
        curr_obj = find_closest_object(curr_nav_cell, kb_abs)
        knowledge = f'the User is now near the {curr_obj}.'
        curr_obj_idx = kb_path_order.index(curr_obj)
        next_obj_idx = curr_obj_idx + 1
        if next_obj_idx != len(kb_path_order):
            next_obj = kb_path_order[next_obj_idx]
            knowledge += f' the next stop is the {next_obj}'

        context = []
        for idx, turn in enumerate(split):
            if idx == len(split) - 1:
                continue
            ctx_id = 'User:' if turn['id'] == 'navigator' else 'System:'
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
val_files = ['ac2c6c2a-ca61-4645-be2a-7d63d6d07b10.json',
             '84c81ced-5a69-4f8c-b16b-dd8ee80daa48.json']
test_files = ['5f3e5e47-00d2-41f4-bd89-f9ddcc10f3f4.json',
              '44413763-4c0d-45fe-8215-80b1e2eff68b.json']

for e in ex:
    data_path = os.path.join(input_folder, e)
    print('ex:', e)
    for file_name in os.listdir(data_path):
        if not file_name.endswith('json'):
            continue
        with open(os.path.join(data_path, file_name), encoding='utf8') as json_file:
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

save_jsonl(train_samples, 'ins_train.json')
save_jsonl(val_samples, 'ins_val.json')
save_jsonl(test_samples, 'ins_test.json')


