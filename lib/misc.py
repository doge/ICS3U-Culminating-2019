'''

    misc.py
    fractal

'''

import random, string


def generate_token(token_length):
    ''' returns a random string with the length of token_length '''
    letters_plus_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_plus_digits) for x in range(token_length))
