import re
import string

def __tokenize(text):
    text = text.strip().lower()
    split = re.findall(fr'[${string.punctuation}]|\w+', text)
    return [t for t in split]

def is_basic_greeting(text) -> bool:
    greeting_words = {'hi', 'hello', 'hey', 'hiya', 'howdy'}
    for token in __tokenize(text):
        if token in greeting_words:
            return True
    return False

def is_how_are_you_greeting(text) -> bool:
    t = text.lower()
    match = bool(re.match("(.*)(are you today)(.*)", t))
    match |= bool(re.match("(.*)(how are you)(.*)", t))
    match |= bool(re.match("(.*)(you doing)(.*)", t))
    match |= bool(re.match("(.*)(going on)(.*)", t))
    return match


def is_goal_match(text) -> bool:
    t = text.lower()
    match = bool(re.match("(.*)(what is (the|my) goal?)(.*)", t))
    match |= bool(re.match("(what (do|should) i do?)", t))
    match |= bool(re.match("(what am i expected to do?)", t))
    match |= bool(re.match("(what to do?)", t))
    return match