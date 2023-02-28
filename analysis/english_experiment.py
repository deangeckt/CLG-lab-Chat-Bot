import os
import json
from sys import argv

from path_gt import gt_maps
from utils import dtw_distance

def run():
    print('english experiment with friends - new survey')
    for file_name in os.listdir(data_path):
        if not file_name.endswith('json'):
            continue
        with open(os.path.join(data_path, file_name), encoding='utf8') as json_file:
            data = json.load(json_file)

        map_idx = data['map_metadata']['map_idx']
        nav_path = data['user_map_path']
        gt_path = gt_maps[map_idx]
        path_score = dtw_distance(gt_path, nav_path)

        # print('Person: ', data['user_metadata']['name'], data['user_metadata']['age'], data['guid'])
        print('Map: ', map_idx + 1)
        print('Path DTW score: ', path_score)
        for qa in data['user_survery']:
            if qa['question'] == 'Age:':
                print(qa)
            if qa['question'] == 'Gender:':
                print(qa)
        print()


if __name__ == '__main__':
    data_path = argv[1]
    run()