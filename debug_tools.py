from pprint import pprint

def pretty_print(obj, level = 0):
    if (hasattr(obj, '__iter__') and not isinstance(obj, str)):
        for i in obj:
            pretty_print(i, level + 1)
    else:
        print((" " * 2 * level) + str(obj))

def error(token, *args):
    string = str(token) + ": "
    for i in args:
        string += str(i) + " "

    print string
