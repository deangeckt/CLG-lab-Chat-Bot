import os
import json
from path_gt import gt_maps
from utils import dtw_distance

data_path = r"C:\Users\t-deangeckt\OneDrive - Microsoft\Personal\HU\nlp_lab\code_and_data\map_task\data\english_ex_friends_jan_23"

print('english experiment with friends - jan 23')
for file_name in os.listdir(data_path):
    if not file_name.endswith('json'):
        continue
    with open(os.path.join(data_path, file_name), encoding='utf8') as json_file:
        data = json.load(json_file)

    map_idx = data['map_metadata']['map_idx']
    nav_path = data['user_map_path']
    gt_path = gt_maps[map_idx]
    path_score = dtw_distance(gt_path, nav_path)

    print('Person: ', data['user_metadata']['name'], data['user_metadata']['age'], data['guid'])
    print('Map: ', map_idx + 1)
    print('Path DTW score: ', path_score)
    print('note on instructions: ', data['user_survey']['survey_instructions'])
    print('note on bot: ', data['user_survey']['survey_bot'])
    print()