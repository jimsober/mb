#!/usr/bin/env python

import utils
import strategy

def discard(board, trip_length, teams, hand_scores, label, player, hands, delayed_action):
    unique_cards = []
    for card in hands[player]:
        if card in unique_cards:
            pass
        else:
            unique_cards.append(card)
    default_card, default_option = strategy.defaults(hands, board, trip_length, teams, hand_scores, label, \
      player, unique_cards, delayed_action)
    if len(unique_cards) == 1:
        play_card = unique_cards[0]
        hands[player].remove(play_card)
    else:
        play_card = default_card
        hands[player].remove(play_card)
        print "Player %s, you have selected:" % (str(player+1)),
        print utils.colorize(play_card.upper())
    print
    return hands, play_card, default_option
