"""
Generates a random number between 1 and 7
"""

import random

def random_from_1_to_5():
    #this is the asummed given function
    return random.randint(1, 5)

def random_from_1_to_7():
    """
    Generates a random number from 1 to 7
    """
    source = [6, 7]
    for _ in xrange(1, 6):
        source.append(random_from_1_to_5())
    random_index = random.randint(0, 6)
    return source[random_index]


