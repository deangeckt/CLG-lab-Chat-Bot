import re
import string

greeting_words = {'hi', 'hello', 'hey', 'hiya', 'howdy'}
question_words = {'what', 'when', 'where', 'why', 'which', 'who', 'whose', 'how', 'do', 'did', 'does', 'are', 'is',
                  'would', 'will', 'can', 'could', 'any'}
wh_questions_words = {'what', 'when', 'where', 'why', 'which', 'who', 'whose', 'how'}


def tokenize(text):
    text = text.strip().lower()
    split = re.findall(fr'[${string.punctuation}]|\w+', text)
    return [t for t in split]


def is_greeting(text):
    for token in tokenize(text):
        if token in greeting_words:
            return True
    return False


def is_question(text):
    """
    :param text: user message
    :return: str: 'none' - no question, 'wh' - wh question, 'yn' - yes no question
    """
    is_q = False

    tokens = tokenize(text)
    if tokens[-1] == '?':
        is_q = True
    else:
        for token in tokens:
            if token in question_words:
                is_q = True
    if not is_q:
        return 'none'
    for token in tokens:
        if token in wh_questions_words:
            return 'wh'
    return 'yn'


def is_map_object_included(text, objects):
    for token in tokenize(text):
        if token in objects:
            return True
    return False


def is_simple_answer(text):
    return text == 'yes' or text == 'no'
