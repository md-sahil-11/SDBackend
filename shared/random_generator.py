import random
import string
from typing import List


def get_random_animal_name() -> str:
    animal_names: List[str] = [
        'lion', 'tiger', 'elephant', 'giraffe', 'zebra', 'monkey', 'kangaroo', 'koala',
        'crocodile', 'hippopotamus', 'rhinoceros', 'gorilla', 'penguin', 'panda', 'cheetah',
        'leopard', 'wolf', 'fox', 'bear', 'deer', 'camel', 'seal', 'dolphin', 'shark', 'eagle',
        'hawk', 'owl', 'parrot', 'peacock', 'duck', 'swan', 'flamingo', 'bee', 'ant', 'butterfly',
        'spider', 'snake', 'turtle', 'frog', 'lizard', 'whale', 'jaguar', 'panther', 'buffalo',
        'moose', 'horse', 'cow', 'sheep', 'goat', 'pig', 'chicken', 'rooster', 'turkey', 'rabbit',
        'hamster', 'guinea pig', 'rat', 'mouse', 'bat', 'dove', 'canary', 'goldfish', 'jellyfish',
        'octopus', 'lobster', 'crab', 'starfish', 'snail', 'ostrich', 'gorilla', 'orangutan', 'chimp',
        'blue jay', 'cockatoo', 'macaw', 'woodpecker', 'wasp', 'dragonfly', 'chameleon', 'hedgehog',
        'gazelle', 'lemur', 'toucan', 'mongoose', 'kookaburra', 'tarantula', 'scorpion', 'squirrel',
        'raccoon', 'platypus', 'seahorse', 'swordfish', 'salmon', 'trout', 'crayfish', 'badger',
        'beaver', 'otter', 'buffalo', 'panther', 'weasel'
    ]

    return random.sample(animal_names, 1)[0]


def get_random_string(length):
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for i in range(length))
    return code

