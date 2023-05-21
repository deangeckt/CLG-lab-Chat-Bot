import os
import openai


openai.organization = "org-uDZtzijOHrdSPGJiRCBzAPac"
openai.api_key = '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'

# r = openai.Model.list()
# response = openai.Completion.create(
#       model="gpt-3.5-turbo",
#       prompt=prompt,
#       temperature=0.81,
#       max_tokens=256,
#       top_p=1,
#       frequency_penalty=0,
#       presence_penalty=0
# )

# https://platform.openai.com/docs/api-reference/chat/create
# https://platform.openai.com/docs/guides/chat/introduction - finish code should be 'stop' only
system_content = "You are an English-Spanish bilingual speaker. Your responses MUST include words from both languages, and NOT a translation."
user_prefix = "Rewrite the following sentence in mixed English-Spanish:"
user_msg = 'The correct path is to visit the frog before walking over the crocodile. Then, at the frog, the path is to do a slight u-turn and head back left over the crocodile and onto a big black rock.'
user_content = f'{user_prefix} "{user_msg}"'

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]
)
cs_resp = response.choices[0].message['content']
finish_reason = response.choices[0]['finish_reason']

