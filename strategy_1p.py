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
        if player == 0:
            print "Player %s, your selection is" % str(player+1),
            raw_input(utils.colorize(play_card) + ". Press any key to continue. ")
    else:
        if player == 0:
            input_err = True
            while input_err:
                print "Player %s, select a card from [" % str(player+1),
                for card in unique_cards:
                    print utils.colorize(card),
                print "] [%s]:" % utils.colorize(default_card),
                play_card = raw_input()
                if play_card == '':
                    play_card = default_card
                if len(play_card) == 1:
                    play_card = play_card + " "
                play_card = play_card.upper()
                if play_card in hands[player]:
                    input_err = False
                    hands[player].remove(play_card)
                    if play_card != default_card:
                        default_option = ''
                else:
                    utils.sound_bell()
                    print
            print
            print "Player %s, you have selected:" % (str(player+1)),
            print utils.colorize(play_card.upper())
            print
        else:
            play_card = default_card
            hands[player].remove(play_card)
            print "Player %s has selected to play" % (str(player+1)),
            print utils.colorize(play_card.upper()),
            print "to %s." % default_option
            print
            raw_input("Press any key to continue. ")
            print
    return hands, play_card, default_option
