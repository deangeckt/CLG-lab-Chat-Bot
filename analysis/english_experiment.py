import os
import json
data_path = r"C:\Users\t-deangeckt\OneDrive - Microsoft\Personal\HU\nlp_lab\code_and_data\map_task\data\english_ex_friends_jan_23"

print('english experiment with friends - jan 23')
for file_name in os.listdir(data_path):
    if not file_name.endswith('json'):
        continue
    with open(os.path.join(data_path, file_name), encoding='utf8') as json_file:
        data = json.load(json_file)

    print('Person: ', data['user_metadata']['name'], data['user_metadata']['age'], data['guid'])
    print('note on instructions: ', data['user_survey']['survey_instructions'])
    print('note on bot: ', data['user_survey']['survey_bot'])
    print()