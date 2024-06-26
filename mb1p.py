#!/usr/bin/env python
import os
import sys
import init
import init_1p
import cards
import cards_1p
import utils
import strategy_1p
import score

game_count = 0
play_again = True

while play_again:

    #game loop
    os.system('clear')
    print
    print "Welcome to Mille Bornes! You are playing against the computer."
    print
    if len(sys.argv) not in [1, 2]:
        print "Invalid number of arguments. Script takes 0 or 1 arguments [number of players]."
        print
        exit()
    if len(sys.argv) == 2:
        if str(sys.argv[1]) in ["2", "3"]:
            num_players = int(sys.argv[1])
        else:
            print "Invalid argument values. Correct syntax: python mb.py [2, 3]."
            exit()
    else:
        players_input_err = True
        while players_input_err:
            num_players = raw_input("Enter number of players (2 or 3): ")
            print
            if str(num_players) not in ["2", "3"]:
                utils.sound_bell()
                pass
            else:
                num_players = int(num_players)
                players_input_err = False
    hand_count, game_scores, teams, deck, label, player, goes_first = init_1p.initialize_game(num_players)
    raw_input("Player %s goes first! Press any key to continue. " % str(goes_first+1))
    print

    continue_hand = True
    os.system('clear')
    while continue_hand:

        #hand loop
        play_count, hand_count, hand_scores, board, draw_pile, discard_pile, trip_length, \
          extension, delayed_action, trip_completed, player, draw_again, cf_count, cf, \
          play_possible = init.initialize_hand(num_players, teams, deck, label, player, hand_count, goes_first)
        hands = cards.deal(num_players, draw_pile)
        continue_turn = True
        while continue_turn:
            if (draw_again or cf) and not trip_completed[utils.team(player, teams)]:
                draw_again = False
                cf = False
                utils.sound_bell()
                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count)
                if player == 0:
                    utils.show_hand(player, hands)
                if len(draw_pile) > 0:
                    print "Player %s, draw again!" % str(player+1)
                    print
                else:
                    print "Player %s, play again!" % str(player+1)
                    print
            else:
                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count)
                if player == 0:
                    utils.show_hand(player, hands)
            if len(draw_pile) > 0:
                if player == 0:
                    raw_input("Player %s, press any key to draw a card. " % str(player+1))
                    print
                hands = cards_1p.draw_card(player, hands, draw_pile)
            elif not delayed_action:
                utils.sound_bell()
                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count)
                if player == 0:
                    utils.show_hand(player, hands)
                print "There are no more cards in the draw pile. Delayed action!"
                print
                raw_input("Press any key to continue. ")
                print
                delayed_action = True
                if player == num_players - 1:
                    player = 0
                else:
                    player += 1
                if player == 0:
                    utils.show_hand(player, hands)
                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                  board, trip_length, extension, delayed_action, cf_count)
            undo = True
            while undo:
                if delayed_action:
                    play_possible = cards.check_play_possible(hand_scores, board, hands, teams, trip_length)
                if len(hands[player]) > 0 and play_possible:
                    hands, play_card, default_option = strategy_1p.discard(board, trip_length, teams, hand_scores, \
                      label, player, hands, delayed_action)
                    plays = cards.valid_plays(teams, label, player, play_card, board, trip_length, hand_scores)
                    board, hand_scores, undo, draw_again, hands, victim, play_count, \
                      discard_pile = cards_1p.play(teams, label, player, play_card, board, plays, hand_scores, \
                      hands, default_option, play_count, discard_pile)
                else:
                    continue_turn = False
                    utils.sound_bell()
                    if play_possible:
                        raw_input("Player %s, you have no more cards in your hand so the hand is over. Press any key to continue. " % str(player+1))
                    else:
                        raw_input("Player %s, there are no remaining plays by any player so the hand is over. Press any key to continue. " % str(player+1))
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
                    if plr == 0:
                        respond_input_err = True
                        utils.sound_bell()
                        while respond_input_err:
                            respond_yn = raw_input("Player " + str(plr+1) + ", would you like to respond (Y/N)? ")
                            print
                            if respond_yn.upper() == "Y":
                                respond_input_err = False
                                utils.sound_bell()
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
                                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                                  game_scores, board, trip_length, extension, delayed_action, cf_count)
                                raw_input("Player %s scores a Coup Fourre!!! Press any key to continue. " % str(player+1))
                                if len(draw_pile) > 0:
                                    hands = cards_1p.draw_card(player, hands, draw_pile)
                            elif respond_yn.upper() == "N":
                                respond_input_err = False
                            else:
                                utils.sound_bell()
                    else:
                        utils.sound_bell()
                        utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                          game_scores, board, trip_length, extension, delayed_action, cf_count)
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
                        utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                          game_scores, board, trip_length, extension, delayed_action, cf_count)
                        raw_input("Player %s scores a Coup Fourre!!! Press any key to continue. " % str(player+1))
                        if len(draw_pile) > 0:
                            hands = cards_1p.draw_card(player, hands, draw_pile)
            else:
                if hand_scores[utils.team(player, teams)] == trip_length and trip_length == 1000:
                    trip_completed[utils.team(player, teams)] = True
                    continue_turn = False
                    utils.sound_bell()
                    utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                      board, trip_length, extension, delayed_action, cf_count)
                    if player == 0:
                        print(label + " " + str(utils.team(player, teams)+1) + ", you have completed 1000 miles!")
                    else:
                        print(label + " " + str(utils.team(player, teams)+1) + " has completed 1000 miles!")
                    print
                    raw_input("Press any key to continue. ")
                elif hand_scores[utils.team(player, teams)] == trip_length and trip_length == 700 and not extension:
                    utils.sound_bell()
                    utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, game_scores, \
                      board, trip_length, extension, delayed_action, cf_count)
                    if player == 0:
                        utils.show_hand(player, hands)
                        print(label + " " + str(utils.team(player, teams)+1) + ", you have completed 700 miles!")
                        print
                        extend_input_err = True
                        while extend_input_err:
                            extend_yn = raw_input("Player " + str(player+1) + ", would you like to extend the trip to 1000 miles (Y/N)? ")
                            if extend_yn.upper() == "Y":
                                extend_input_err = False
                                trip_length = 1000
                                extension = True
                                utils.sound_bell()
                                utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                                  game_scores, board, trip_length, extension, delayed_action, cf_count)
                                if player == 0:
                                    utils.show_hand(player, hands)
                                print "The trip has been extended to 1000 miles."
                                print
                                raw_input("Press any key to continue. ")
                            elif extend_yn.upper() == "N":
                                extend_input_err = False
                                trip_completed[utils.team(player, teams)] = True
                                continue_turn = False
                                break
                            else:
                                utils.sound_bell()
                                print
                    else:
                        print(label + " " + str(utils.team(player, teams)+1) + " has completed 700 miles!")
                        print
                        raw_input("Press any key to continue. ")
                        # miles in hand (target 200 or more)
                        miles = 0
                        for card in hands[player]: 
                            if card in ['2%', '1%', '75', '50', '25']:
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
                            utils.show_board(player, teams, game_count, play_count, hand_count, hand_scores, \
                              game_scores, board, trip_length, extension, delayed_action, cf_count)
                            print "Player %s has extended the trip to 1000 miles." % str(player+1)
                            print
                            raw_input("Press any key to continue. ")
                            print
                        else:
                            trip_completed[utils.team(player, teams)] = True
                            continue_turn = False
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
        game_scores = score.score_hand(player, teams, hand_scores, game_scores, board, trip_length, \
          trip_completed, delayed_action, extension, cf_count, game_count, hand_count, play_count)
        high_score = max(game_scores)
        if high_score < 5000:
            raw_input("Press any key to continue. ")
        else:
            continue_hand = False
            print

    #end of game
    utils.sound_bell()
    high_player = []
    for i in range(len(teams)):
        if game_scores[i] == high_score:
            high_player.append(i)
    if len(high_player) == 1:
        print("The winner is " + label + " " + str(high_player[0]+1) + " with " + str(max(game_scores)) + " miles!")
    elif len(high_player) == 2:
        print('The winners are ' + label + 's'+ ' ' + str(high_player[0]+1) + ' and ' + str(high_player[1]+1) + ' with ' + str(max(game_scores)) + ' miles!')
    elif len(high_player) == 3:
        print('The winners are ' + label + 's'+ ' ' + str(high_player[0]+1) + ', ' + str(high_player[1]+1) + ' and ' + str(high_player[2]+1) + ' with ' + str(max(game_scores)) + ' miles!')
    print
    print "Game Over."
    print
    again_input_err = True
    while again_input_err:
        again_yn = raw_input("Would you like to play again? (Y/N) ")
        if again_yn.upper() == "Y":
            again_input_err = False
            print
        elif again_yn.upper() == "N":
            again_input_err = False
            play_again = False
            print
            print "Thank you for playing!"
            print
        else:
            utils.sound_bell()
            print
