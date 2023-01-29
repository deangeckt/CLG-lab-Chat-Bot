import json
json_file_path = 'translation_pairs.json'
with open(json_file_path, 'r') as j:
     contents = json.loads(j.read())

print(contents)

c1 = json.loads(open('translation_pairs.json', 'r').read())
print(c1)