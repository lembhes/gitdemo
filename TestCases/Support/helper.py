from urllib.parse import quote_plus
import base64
import random
import uuid


def get_base64secrets(client_id, client_secret):
    s = client_id + ':' + client_secret
    encoded = base64.b64encode(s.encode("utf-8"))
    return str(encoded.decode("utf-8"))


def urlEncoder(query):
    return quote_plus(query)


def update_dictionary(dictionary, **kwarg):
    for key in kwarg.keys():
        dictionary[key] = kwarg[key]
    return dictionary


def delete_key(dictionary, *arg):
    for key in arg:
        if key in dictionary:
            del dictionary[key]
    return dictionary


def get_random_pairs(dictionary):
    n = random.randint(1, len(dictionary) - 1)
    pair = random.sample(dictionary.items(), n)
    return dict(pair)


def factorial(num):
    if num == 1:
        return num
    else:
        return num * factorial(num - 1)


def random_title():
    base_text = 'ques_'
    final_ques_name = base_text + uuid.uuid4().hex
    return final_ques_name