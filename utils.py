#!/usr/bin/env python

import os
import sys

def show_hand(player, hands):
    print "Player %s cards: " % str(player+1),
    for card in range(len(hands[player])):
        print colorize(hands[player][card]),
    print "\r"
    print

def colorize(val):
    if val in ['ET', 'DA', 'PP', 'RW']:
        cmd = u"\u001b[34m" + val + u"\u001b[0m"
    elif val in ['S ', 'OG', 'FT', 'A ', 'SL']:
        val = val.strip()
        cmd = u"\u001b[31m" + val + u"\u001b[0m"
    elif val in ['R ', 'G ', 'ST', 'RP', 'EL']:
        val = val.strip()
        cmd = u"\u001b[32m" + val + u"\u001b[0m"
    else:
        cmd = val
    return cmd

def show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, board, \
  trip_length, extension, delayed_action, cf_count):
    os.system('clear')
    print " Trip distance: %s" % str(trip_length)
    if extension:
        print "     Extension: " + u"\u001b[38;5;208m" + "ON" + u"\u001b[0m"
    if delayed_action:
        print "Delayed Action: " + u"\u001b[38;5;208m" + "ON" + u"\u001b[0m"
    if len(teams[0]) > 1:
        plr = 0
        print " "*15,
        for i in range(len(teams)):
            print "   Team %s" % str(i+1),
        print "\r"
        for i in range(len(teams[0])):
            print " "*15,
            for j in range(len(teams)):
                if plr == player:
                    print u"\u001b[38;5;208m" + " Player %s" % str(teams[j][i]+1) + u"\u001b[0m",
                else:
                    print " Player %s" % str(teams[j][i]+1),
                plr += 1
            print "\r"
    else:
        print " "*15,
        for i in range(len(hand_scores)):
            if i == player:
                print u"\u001b[38;5;208m" + " Player %s" % str(i+1) + u"\u001b[0m",
            else:
                print " Player %s" % str(i+1),
        print "\r"
    print " Current score:",
    for i in range(len(hand_scores)):
        print " "*(8 - len(str(game_scores[i]))), str(game_scores[i]),
    print "\r"
    print "Distance Piles:",
    for i in range(len(hand_scores)):
        two_huns = board[i][2].count('2%')
        if two_huns > 0:
            print " "*(7 - len(str(hand_scores[i])) - two_huns), "*"*two_huns, str(hand_scores[i]),
        else:
            print " "*(8 - len(str(hand_scores[i]))), str(hand_scores[i]),
    print "\r"
    print "   Battle Pile:",
    for i in range(len(hand_scores)):
        print " "*(8 - len(str(board[i][0]).strip())), colorize(str(board[i][0])),
    print "\r"
    print "    Speed Pile:",
    for i in range(len(hand_scores)):
        print " "*(8 - len(str(board[i][1]))), colorize(str(board[i][1])),
    print "\r"
    print "   Safety Area:",
    for i in range(len(hand_scores)):
        if cf_count[i] > 0:
            print " "*(8 - 3*len(board[i][3]) - cf_count[i]), "*"*cf_count[i], 
        else:
            print " "*(9 - 3*len(board[i][3])),
        for j in range(len(board[i][3])):
            print colorize(str(board[i][3][j])),
    print "\r"
    print

def team(player, teams):
    if len(teams) == 2:
        if player == 0 or player == 2:
            team = 0
        elif player == 1 or player == 3:
            team = 1
    else:
        if player == 0 or player == 3:
            team = 0
        elif player == 1 or player == 4:
            team = 1
        elif player == 2 or player == 5:
            team = 2
    return team

def sound_bell():
    sys.stdout.write('\a')
    sys.stdout.flush()
