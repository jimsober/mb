#!/usr/bin/env python

import utils
import score

def draw_card(player, hands, draw_pile):
    hands[player].append(draw_pile.pop(0))
    if player == 0:
        print "Player %s, you have drawn:" % str(player+1),
        print utils.colorize(hands[player][len(hands[player])-1])
        print
    return hands

def play(teams, label, player, play_card, board, plays, hand_scores, hands, default_option, play_count, discard_pile):
    victim = -1
    play_list = {}
    undo = False
    draw_again = False
    for i in range(len(plays)):
        play_list.update({i:plays[i]})
    if player == 0:
        print "These are the valid options:"
        for k, v in play_list.iteritems():
            print k,
            print "-",
            print v
        print
        input_err = True
        while input_err:
            if len(play_list) == 2:
                default_option = 'Discard Pile'
            if default_option == '' and play_card in ['2%', '1%', '75', '50', '25']:
                default_option = 'Distance Piles'
            if default_option == '' and play_card in ['RW', 'DA', 'ET', 'PP']:
                default_option = 'Safety Area'
            if default_option == '':
                play_num = raw_input("Select one of the options above by number: ")
            else:
                play_num = raw_input("Select one of the options above by number [%s]: " \
                  % play_list.values().index(default_option))
            print
            if play_num == '':
                if default_option != '':
                    input_err = False
                    play_num = int(play_list.values().index(default_option))
                else:
                    utils.sound_bell()
            else:
                try:
                    if int(play_num) in play_list.keys():
                        input_err = False
                        play_num = int(play_num)
                    else:
                        utils.sound_bell()
                except ValueError:
                    utils.sound_bell()
    else:
        play_num = play_list.values().index(default_option)
    if play_list[play_num] == 'Undo':
        hands[player].append(play_card)
        undo = True
    if play_list[play_num] == 'Discard Pile':
        discard_pile.append(play_card)
        play_count += 1
    elif play_list[play_num] == 'Battle Pile':
        board[utils.team(player, teams)][0] = play_card
        play_count += 1
    elif play_list[play_num] == 'Speed Pile':
        board[utils.team(player, teams)][1] = play_card
        play_count += 1
    elif play_list[play_num] == 'Distance Piles':
        board[utils.team(player, teams)][2].append(play_card)
        play_count += 1
        hand_scores[utils.team(player, teams)] += score.score_card(play_card)
    elif play_list[play_num] == 'Safety Area':
        board[utils.team(player, teams)][3].append(play_card)
        play_count += 1
        draw_again = True
        if play_card == 'RW':
            if board[utils.team(player, teams)][0] == 'S ':
                board[utils.team(player, teams)][0] = 'R '
            if board[utils.team(player, teams)][1] == 'SL':
                board[utils.team(player, teams)][1] = 'EL'
        elif play_card == 'DA':
            if board[utils.team(player, teams)][0] == 'A ':
                board[utils.team(player, teams)][0] = 'RP'
        elif play_card == 'ET':
            if board[utils.team(player, teams)][0] == 'OG':
                board[utils.team(player, teams)][0] = 'G '
        elif play_card == 'PP':
            if board[utils.team(player, teams)][0] == 'FT':
                board[utils.team(player, teams)][0] = 'ST'
    else:
        for i in range(len(hand_scores)):
            if play_list[play_num] == label + ' ' + str(i+1) + ' Battle Pile':
                board[i][0] = play_card
                victim = i
                play_count += 1
            if play_list[play_num] == label + ' ' + str(i+1) + ' Speed Pile':
                board[i][1] = play_card
                victim = i
                play_count += 1
    return board, hand_scores, undo, draw_again, hands, victim, play_count, discard_pile
