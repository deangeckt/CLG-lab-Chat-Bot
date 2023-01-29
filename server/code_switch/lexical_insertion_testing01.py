import json

translation_pairs = json.loads(open('translation_pairs.json', 'r').read())

# input_text = 'go from the start of the map and return back.'
input_text = 'nothing :('
text = input_text

replacement_found = False
for english_token in translation_pairs['en']:
	if text.find(english_token) > 0:  # Found in text
		replacement_found = True
		break

for english_token, spanish_token in zip(translation_pairs['en'], translation_pairs['es']):
	text = text.replace(english_token, spanish_token)

print(input_text)
print(text)
print(replacement_found)
