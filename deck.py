

import re


def build_deck(decks = 1):
    suits = ['Hearts','Diamonds','Spades','Clubs']
    faces = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    ret_deck = []
    for x in range(decks):
        for s in suits:
            for f in faces:
                ret_deck.append({'F':f,'S':s})
    return ret_deck



