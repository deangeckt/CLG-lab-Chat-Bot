import random

direction_mapping_to_phrasing = {'right': ['east', 'right'],
                                 'left': ['west', 'left'],
                                 'up': ['north', 'above'],
                                 'down': ['south', 'below'],
                                 }
direction_mapping = {'right': ['east', 'right'],
                     'left': ['west', 'left'],
                     'up': ['north', 'up'],
                     'down': ['south', 'down'],
                     }
angle_directions = ['east', 'west', 'south', 'north']
verb_options = ['keep going', 'continue']


def get_direction_phrase(direction):
    direction_phrase = random.choice(direction_mapping_to_phrasing[direction])
    if direction_phrase in angle_directions:
        direction_phrase += ' of the'
    elif direction_phrase in ['above', 'below']:
        direction_phrase += ' the'
    else:
        direction_phrase += ' to the'

    return direction_phrase

def informative_statement2(obj, direction):
    """
    e.g. 'keep going <direction> to / by the <object>'
    :param obj: an object from the kb
    :param direction: up, down, right, left
    :return: random phrasing of informative statement
    """
    direction_phrase = get_direction_phrase(direction)
    main_verb = random.choice(verb_options)
    return f'{main_verb} {direction_phrase} {obj}'


def informative_statement3(direction):
    """
    e.g. 'keep going <direction>'
    :param direction: up, down, right, left
    :return: random phrasing of informative statement
    """
    direction_phrase = random.choice(direction_mapping[direction])
    main_verb = random.choice(verb_options)
    return f'{main_verb} {direction_phrase}'


def engage_question(obj):
    """
    e.g. 'do you see the <obj>'
    :param obj: an object from the kb
    :return: random phrasing engaging question
    """
    return f'do you see the {obj}?'

