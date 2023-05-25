import openai

openai.organization = "org-uDZtzijOHrdSPGJiRCBzAPac"
openai.api_key = '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'

# https://platform.openai.com/docs/api-reference/chat/create
# https://platform.openai.com/docs/guides/chat/introduction - finish code should be 'stop' only

def openai_call(messages: list[dict]) -> str:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    cs_resp = response.choices[0].message['content']
    finish_reason = response.choices[0]['finish_reason']

    if finish_reason != 'stop':
        print('openai err: ', finish_reason)
        return 'Something went wrong, try again'
    return cs_resp