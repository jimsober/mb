#!/usr/bin/env python
import os
import sys
import csv
import init
import cards
import cards_auto
import utils
import utils_auto
import strategy_auto
import score
import score_auto

game_count = 0

os.system('clear')
print
print "Welcome to Mille Bornes!"
print

if len(sys.argv) not in [1, 4]:
    print "Invalid number of arguments. Script takes 0 or 3 arguments [number of players, number of games, pause between hands flag (Y/N)]."
    print
    exit()
if len(sys.argv) == 4:
    if str(sys.argv[1]) in ["2", "3", "4", "6"] and int(sys.argv[2]) > 0 and str(sys.argv[3]).upper() in ["N", "Y"]:
        num_players = int(sys.argv[1])
        num_games = int(sys.argv[2])
        pause_flag = str(sys.argv[3])
    else:
        print "Invalid argument values. Correct syntax: python mb_auto.py [2, 3, 4, 6] [>0] [Y, N]."
        exit()
else:
    players_input_err = True
    while players_input_err:
        num_players = raw_input("Enter number of players (2, 3, 4, or 6): ")
        print
        if str(num_players) not in ["2", "3", "4", "6"]:
            utils.sound_bell()
            pass
        else:
            num_players = int(num_players)
            players_input_err = False

# CSV file headers are created one time per file
#csvfile =  open('mb_' + str(num_players) + 'p_results.csv', 'w')
#filewriter = csv.writer(csvfile)
#filewriter.writerow(['Go First Player', 'Game Winner', 'Game', 'Round', 'Team or Player', 'Milestones', 'Safeties', 'All 4 safeties played', 'Coup-fourres', 'Trip completed', 'Delayed action', 'Safe trip', 'Extension', 'Shut-out', 'Total for deal', 'Combined total'])
#csvfile.close()

if len(sys.argv) == 1:
    games_input_err = True
    while games_input_err:
        num_games = raw_input("Enter number of games: ")
        print
        try:
            if int(num_games) > 0:
                games_input_err = False
                num_games = int(num_games)
            else:
                utils.sound_bell()
        except ValueError:
            utils.sound_bell()
    pause_input_err = True
    while pause_input_err:
        pause_flag = raw_input("Pause between hands? (Y/N): ")
        print
        if pause_flag.upper() in ["N", "Y"]:
            pause_input_err = False
        else:
            utils.sound_bell()

while game_count < num_games:

    #game loop
    game_count += 1
    hand_count, game_scores, teams, deck, label, player, goes_first = init.initialize_game(num_players)
    csvfile =  open('mb_' + str(num_players) + 'p_results.csv', 'a')
    filewriter = csv.writer(csvfile)
    filewriter.writerow([str(goes_first+1), "", str(game_count)])
    csvfile.close()

    os.system('clear')
    continue_hand = True
    while continue_hand:

        #hand loop
        play_count, hand_count, hand_scores, board, draw_pile, discard_pile, trip_length, \
          extension, delayed_action, trip_completed, player, draw_again, cf_count, cf, play_possible = \
          init.initialize_hand(num_players, teams, deck, label, player, hand_count, goes_first)
        hands = cards.deal(num_players, draw_pile)
        continue_turn = True
        while continue_turn:
            if (draw_again or cf) and not trip_completed[utils.team(player, teams)]:
                draw_again = False
                cf = False
                utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                utils.show_hand(player, hands)
                if len(draw_pile) > 0:
                    print "Player %s, draw again!" % str(player+1)
                    print
                else:
                    print "Player %s, play again!" % str(player+1)
                    print
            else:
                utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                utils.show_hand(player, hands)
            if len(draw_pile) > 0:
                hands = cards.draw_card(player, hands, draw_pile)
            elif not delayed_action:
                utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                utils.show_hand(player, hands)
                print "There are no more cards in the draw pile. Delayed action!"
                print
                delayed_action = True
                if player == num_players - 1:
                    player = 0
                else:
                    player += 1
                utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                utils.show_hand(player, hands)
            undo = True
            while undo:
                if delayed_action:
                    play_possible = cards.check_play_possible(hand_scores, board, hands, teams, trip_length)
                if len(hands[player]) > 0 and play_possible:
                    hands, play_card, default_option = strategy_auto.discard(board, trip_length, teams, hand_scores, \
                      label, player, hands, delayed_action)
                    plays = cards.valid_plays(teams, label, player, play_card, board, trip_length, hand_scores)
                    board, hand_scores, undo, draw_again, hands, victim, play_count, \
                      discard_pile = cards_auto.play(teams, label, player, play_card, board, plays, hand_scores, \
                      hands, default_option, play_count, discard_pile)
                else:
                    continue_turn = False
                    if player == 0:
                        player = num_players-2
                    elif player == 1:
                        player = num_players-1
                    else:
                        player -= 2
                    break
            if victim != -1:
                response_possible = False
                for plr in teams[utils.team(victim, teams)]:
                    if play_card in ['S ', 'SL']  and  'RW' in hands[plr] \
                      or play_card == 'A ' and 'DA' in hands[plr] \
                      or play_card == 'OG' and 'ET' in hands[plr] \
                      or play_card == 'FT' and 'PP' in hands[plr]:
                        response_possible = True
                        victim = plr
                        break
                if response_possible:
                    utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                      game_scores, board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                    cf = True
                    player = plr
                    cf_count[utils.team(plr, teams)] += 1
                    if play_card in ['S ', 'SL']:
                        safety_card = 'RW'
                    elif play_card == 'A ':
                        safety_card = 'DA'
                    elif play_card == 'OG':
                        safety_card = 'ET'
                    elif play_card == 'FT':
                        safety_card = 'PP'
                    hands[player].remove(safety_card)
                    board[utils.team(player, teams)][3].append(safety_card)
                    if safety_card == 'RW':
                        if board[utils.team(player, teams)][0] == 'S ':
                            board[utils.team(player, teams)][0] = 'R '
                        if board[utils.team(player, teams)][1] == 'SL':
                            board[utils.team(player, teams)][1] = 'EL'
                    elif safety_card == 'DA':
                        if board[utils.team(player, teams)][0] == 'A ':
                            board[utils.team(player, teams)][0] = 'RP'
                    elif safety_card == 'ET':
                        if board[utils.team(player, teams)][0] == 'OG':
                            board[utils.team(player, teams)][0] = 'G '
                    elif safety_card == 'PP':
                        if board[utils.team(player, teams)][0] == 'FT':
                            board[utils.team(player, teams)][0] = 'ST'
                    utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                      game_scores, board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                    if len(draw_pile) > 0:
                        hands = cards.draw_card(player, hands, draw_pile)
            else:
                if hand_scores[utils.team(player, teams)] == trip_length and trip_length == 1000:
                    trip_completed[utils.team(player, teams)] = True
                    continue_turn = False
                    utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                      game_scores, board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                    print(label + " " + str(utils.team(player, teams)+1) + ", you have completed 1000 miles!")
                    print
                    break
                elif hand_scores[utils.team(player, teams)] == trip_length and trip_length == 700 and not extension:
                    utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                      game_scores, board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                    utils.show_hand(player, hands)
                    print(label + " " + str(utils.team(player, teams)+1) + ", you have completed 700 miles!")
                    print
                    # miles in hand (target 200 or more)
                    miles = 0
                    for card in hands[player]:
                        miles += score.score_card(card)
                    # hand scores within 200
                    close_hand = False
                    for i in range(len(teams)):
                        if i == utils.team(player, teams):
                            pass
                        else:
                            if hand_scores[i] >= 500:
                                close_hand = True
                    # game scores within 1000
                    close_game = False
                    for i in range(len(teams)):
                        if i == utils.team(player, teams):
                            pass
                        else:
                            if game_scores[i] >= 4000:
                                close_game = True
                    if (miles >= 200 and not close_hand) or close_game:
                        trip_length = 1000
                        extension = True
                        utils_auto.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                          game_scores, board, trip_length, extension, delayed_action, cf_count, draw_pile, discard_pile)
                        utils.show_hand(player, hands)
                        print "The trip has been extended to 1000 miles."
                        print
                    else:
                        trip_completed[utils.team(player, teams)] = True
                        continue_turn = False
                        break
            if (cf or draw_again) and not trip_completed[utils.team(player, teams)]:
                pass
            elif not trip_completed[utils.team(player, teams)] and (len(draw_pile) > 0 or delayed_action):
                if player == num_players - 1:
                    player = 0
                else:
                    player += 1
                print

        #end of round
        print
        game_scores = score_auto.score_hand(player, teams, hand_scores, game_scores, board, trip_length, \
          trip_completed, delayed_action, extension, cf_count, game_count, hand_count, play_count, num_players)
        high_score = max(game_scores)
        if pause_flag.upper() == "N":
            if high_score >= 5000:
                continue_hand = False
                print
        else:
            if high_score < 5000:
                raw_input("Press any key to continue. ")
            else:
                continue_hand = False
                print

    #end of game
    high_player = []
    for i in range(len(teams)):
        if game_scores[i] == high_score:
            high_player.append(i)
    csvfile =  open('mb_' + str(num_players) + 'p_results.csv', 'a')
    filewriter = csv.writer(csvfile)
    if len(high_player) == 1:
        print("The winner is " + label + " " + str(high_player[0]+1) + " with " + str(max(game_scores)) + " miles!")
        filewriter.writerow(["", label + " " + str(high_player[0]+1), str(game_count)])
    elif len(high_player) == 2:
        print('The winners are ' + label + 's'+ ' ' + str(high_players[0]+1) + ' and ' + str(high_players[1]+1) + ' with ' + str(max(game_scores)) + ' miles!')
        filewriter.writerow(['', label + ' ' + str(high_players[0]+1) + ' and ' + str(high_players[1]+1), str(game_count)])
    elif len(high_player) == 3:
        print('The winners are ' + label + 's'+ ' ' + str(high_players[0]+1) + ', ' + str(high_players[1]+1) + ' and ' + str(high_players[2]+1) + ' with ' + str(max(game_scores)) + ' miles!')
        filewriter.writerow(['', label + 's ' + str(high_players[0]+1) + ', ' + str(high_players[1]+1) + ' and ' + str(high_players[2]+1), str(game_count)])
    csvfile.close()
    print
    print "Game Over."
    print
    if pause_flag.upper() == "Y" and game_count < num_games:
        raw_input("Press any key to continue. ")
