from os import getenv
from uuid import uuid4
import functools
from flask_socketio import disconnect
from flask_login import current_user

# from presentation import cache



def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


# Redacts the user object for DyanmoDB
def object_to_json(class_object):
    resp = {}
    re
    redacted_keys = {
        'password_hash': True,
        'user_token': True
    }
    for att in class_object.__dict__.keys():
        if redacted_keys.get(str(att)):
            continue
        resp[str(att)] = getattr(class_object, att)
    return str(resp)


# PynamoDB specific attr getter for cache


def model_to_dict(class_object):
    resp = {}
    for att in class_object.get_attributes():
        resp[str(att)] = getattr(class_object, att)
    return resp


def load_schema():
    import os
    import json

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    schema_dir = os.path.join(APP_ROOT, '../schema.json')

    schema = {}
    with open(schema_dir) as f:
        schema = json.load(f)
    return convert_to_dlink_list(schema)


def convert_to_dlink_list(schema):
    dl = DList()

    description = None
    left = {}
    top = {}
    bottom = {}
    right = {}
    sound1 = {}
    sound2 = {}
    screen5 = {}

    dl.add({"description": "Welcome Page", "left": left, "top": top, "bottom": bottom, "right": right, "screen5": screen5, "sound1": sound1, "sound2": sound2})

    for segments in schema["course"]["segments"]:
        description = segments['description']
        for transition in segments['transitions']:
            description = transition.get('description', description)
            left = transition.get('left', left)
            top = transition.get('top', top)
            bottom = transition.get('bottom', bottom)
            right = transition.get('right', right)
            screen5 = transition.get('screen5', screen5)
            sound1 = transition.get('sound1', sound1)
            sound2 = transition.get('sound2', sound2)

            dl.add({"description": description, "left": left, "top": top, "bottom": bottom, "right": right, "screen5": screen5, "sound1": sound1, "sound2": sound2})
    return dl.start_node


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DList:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.size = 0

    def add(self, data):
        new_node = Node(data)
        if self.start_node == None:
            self.start_node = new_node
            self.end_node = new_node
        else:
            self.end_node.next = new_node
            new_node.prev = self.end_node
            self.end_node = self.end_node.next
        self.size += 1