#!/usr/bin/env python

import os
import utils

def show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, board, \
  trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile):
    os.system('clear')
    print "         Games: " + " "*(len(str(trip_length))-len(str(game_count))) + str(game_count)
    print "        Rounds: " + " "*(len(str(trip_length))-len(str(hand_count))) + str(hand_count)
    print "         Plays: " + " "*(len(str(trip_length))-len(str(play_count))) + str(play_count)
    print "     Draw Pile: " + " "*(len(str(trip_length))-len(str(len(draw_pile)))) + str(len(draw_pile))
    print "  Discard Pile: " + " "*(len(str(trip_length))-len(str(len(discard_pile)))) + str(len(discard_pile))
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
        print " "*(8 - len(str(board[i][0]).strip())), utils.colorize(str(board[i][0])),
    print "\r"
    print "    Speed Pile:",
    for i in range(len(hand_scores)):
        print " "*(8 - len(str(board[i][1]))), utils.colorize(str(board[i][1])),
    print "\r"
    print "   Safety Area:",
    for i in range(len(hand_scores)):
        if cf_count[i] > 0:
            print " "*(8 - 3*len(board[i][3]) - cf_count[i]), "*"*cf_count[i], 
        else:
            print " "*(9 - 3*len(board[i][3])),
        for j in range(len(board[i][3])):
            print utils.colorize(str(board[i][3][j])),
    print "\r"
    print
