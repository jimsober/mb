#!/usr/bin/env python

import utils

def score_card(play_card):
    if play_card == '2%':
        miles = 200
    elif play_card == '1%':
        miles = 100
    elif play_card == '75':
        miles = 75
    elif play_card == '50':
        miles = 50
    elif play_card == '25':
        miles = 25
    else:
        miles = 0
    return miles

def score_hand(player, teams, hand_scores, game_scores, board, trip_length, trip_completed, delayed_action, \
  extension, cf_count, game_count, hand_count, play_count):
    shut_out = []
    hand_total = []
    all4_score = []
    tripc_score = []
    delayeda_score = []
    safet_score = []
    ext_score = []
    shuto_score = []
    for i in range(len(game_scores)):
        shut_out.append(True)
        hand_total.append(0)
        all4_score.append(0)
        tripc_score.append(0)
        delayeda_score.append(0)
        safet_score.append(0)
        ext_score.append(0)
        shuto_score.append(0)
    utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, board, \
      trip_length, extension, delayed_action, cf_count)
    if len(teams[0]) > 1:
        print " "*28,
        for i in range(len(teams)):
            print "   Team %s" % str(i+1),
        print "\r"
        for i in range(len(teams[0])):
            print " "*28,
            for j in range(len(teams)):
                print " Player %s" % str(teams[j][i]+1),
            print "\r"
    else:
        print " "*28,
        for i in range(len(hand_scores)):
            print " Player %s" % str(i+1),
        print "\r"
    print "            Brought forward:",
    for i in range(len(game_scores)):
        print " "*(8 - len(str(game_scores[i]))), str(game_scores[i]),
    print "\r"
    print "                 Milestones:",
    for i in range(len(game_scores)):
        if hand_scores[i] > 0:
            shut_out[i] = False
            game_scores[i] += hand_scores[i]
            hand_total[i] += hand_scores[i]
        print " "*(8 - len(str(hand_scores[i]))), str(hand_scores[i]),
    print "\r"
    print "            Safeties (@100):",
    for i in range(len(game_scores)):
        safeties = len(board[i][3])
        game_scores[i] += safeties * 100
        hand_total[i] += safeties * 100
        print " "*(8 - len(str(safeties*100))), str(safeties*100),
    print "\r"
    print "All 4 safeties played (300):",
    for i in range(len(game_scores)):
        safeties = len(board[i][3])
        if safeties == 4:
            print "      300",
            game_scores[i] += 300
            hand_total[i] += 300
        else:
            print "        0",
    print "\r"
    print "        Coup-fourres (@300):",
    for i in range(len(game_scores)):
        if cf_count[i] > 0:
            game_scores[i] += cf_count[i]*300
            hand_total[i] += cf_count[i]*300
            print " "*(8 - len(str(cf_count[i]*300))), str(cf_count[i]*300),
        else:
            print "        0",
    print "\r"
    print "       Trip completed (400):",
    for i in range(len(game_scores)):
        if trip_completed[i]:
            print "      400",
            game_scores[i] += 400
            hand_total[i] += 400
        else:
            print "        0",
    print "\r"
    print "       Delayed action (300):",
    for i in range(len(game_scores)):
        if delayed_action and trip_completed[i]:
            print "      300",
            game_scores[i] += 300
            hand_total[i] += 300
        else:
            print "        0",
    print "\r"
    print "            Safe trip (300):",
    for i in range(len(game_scores)):
        if '2%' not in board[i][2] and trip_completed[i]:
            print "      300",
            game_scores[i] += 300
            hand_total[i] += 300
        else:
            print "        0",
    print "\r"
    print "            Extension (200):",
    for i in range(len(game_scores)):
        if extension and trip_completed[i]:
            print "      200",
            game_scores[i] += 200
            hand_total[i] += 200
        else:
            print "        0",
    print "\r"
    print "             Shut-out (500):",
    for i in range(len(game_scores)):
        if shut_out.count(False) == 1:
            if not shut_out[i] and trip_completed[i]:
                print "      500",
                game_scores[i] += 500
                hand_total[i] += 500
            else:
                print "        0",
        else:
            print "        0",
    print "\r"
    print "             Total for deal:",
    for i in range(len(game_scores)):
        print " "*(8 - len(str(hand_total[i]))), str(hand_total[i]),
    print "\r"
    print "             Combined total:",
    for i in range(len(game_scores)):
        print " "*(8 - len(str(game_scores[i]))), str(game_scores[i]),
    print "\r"
    print
    return game_scores
