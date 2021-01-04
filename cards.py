#!/usr/bin/env python

import utils
import score

def deal(num_players, draw_pile):
    hands = []
    for i in range(num_players):
        hands.append([])
    for card in range(6):
        for player in range(num_players):
            hands[player].append(draw_pile.pop(0))
    return hands

def draw_card(player, hands, draw_pile):
    hands[player].append(draw_pile.pop(0))
    print "Player %s, you have drawn:" % str(player+1),
    print utils.colorize(hands[player][len(hands[player])-1])
    print
    return hands

def valid_plays(teams, label, player, play_card, board, trip_length, hand_scores):
    plays = ['Undo', 'Discard Pile']
    if play_card in ['ET', 'PP', 'DA', 'RW']:
        plays.append('Safety Area')
    elif (play_card == 'R ' and board[utils.team(player, teams)][0] not in ['R ', 'OG', 'FT', 'A '] \
      and not 'RW' in board[utils.team(player, teams)][3]) or (play_card == 'G ' and board[utils.team(player, \
      teams)][0] == 'OG' and not 'ET' in board[utils.team(player, teams)][3]) or (play_card == 'ST' and \
      board[utils.team(player, teams)][0] == 'FT' and not 'PP' in board[utils.team(player, teams)][3]) or \
      (play_card == 'RP' and board[utils.team(player, teams)][0] == 'A ' and not 'DA' in \
      board[utils.team(player, teams)][3]):
        plays.append('Battle Pile')
    elif play_card == 'EL' and board[utils.team(player, teams)][1] == 'SL' and not 'RW' in \
      board[utils.team(player, teams)][3]:
        plays.append('Speed Pile')
    elif play_card == 'SL':
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if board[i][1] != 'SL' and not 'RW' in board[i][3]:
                    plays.append(label + ' ' + str(i+1) + ' Speed Pile')
    elif play_card == 'S ':
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if board[i][0] in ['R ', 'G ', 'ST', 'RP', 'OG', 'FT', 'A '] and not 'RW' in board[i][3]:
                    plays.append(label + ' ' + str(i+1) + ' Battle Pile')
    elif play_card == 'OG':
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if (board[i][0] in ['', 'R ', 'G ', 'ST', 'RP', 'FT', 'A ', 'S '] or 'RW' in board[i][3]) \
                  and not 'ET' in board[i][3]:
                    plays.append(label + ' ' + str(i+1) + ' Battle Pile')
    elif play_card == 'FT':
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if (board[i][0] in ['', 'R ', 'G ', 'ST', 'RP', 'OG', 'A ', 'S '] or 'RW' in board[i][3]) \
                  and not 'PP' in board[i][3]:
                    plays.append(label + ' ' + str(i+1) + ' Battle Pile')
    elif play_card == 'A ':
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if (board[i][0] in ['', 'R ', 'G ', 'ST', 'RP', 'OG', 'FT', 'S '] or 'RW' in board[i][3]) \
                  and not 'DA' in board[i][3]:
                    plays.append(label + ' ' + str(i+1) + ' Battle Pile')
    elif play_card == '2%':
        if board[utils.team(player, teams)][2].count('2%') < 2 and hand_scores[utils.team(player, teams)] \
          + 200 <= trip_length and ('SL' not in board[utils.team(player, teams)][1] or 'RW' in \
          board[utils.team(player, teams)][3]) and (board[utils.team(player, teams)][0] == 'R ' or \
          ('RW' in board[utils.team(player, teams)][3] and board[utils.team(player, teams)][0] not in \
          ['OG', 'FT', 'A '])):
            plays.append('Distance Piles')
    elif play_card == '1%' and hand_scores[utils.team(player, teams)] + 100 <= trip_length \
      and ('SL' not in board[utils.team(player, teams)][1] or 'RW' in board[utils.team(player, teams)][3]) \
      and (board[utils.team(player, teams)][0] == 'R ' or ('RW' in board[utils.team(player, teams)][3] \
      and board[utils.team(player, teams)][0] not in ['OG', 'FT', 'A '])):
        plays.append('Distance Piles')
    elif play_card == '75' and hand_scores[utils.team(player, teams)] + 75 <= trip_length \
      and ('SL' not in board[utils.team(player, teams)][1] or 'RW' in board[utils.team(player, teams)][3]) \
      and (board[utils.team(player, teams)][0] == 'R ' or ('RW' in board[utils.team(player, teams)][3] \
      and board[utils.team(player, teams)][0] not in ['OG', 'FT', 'A '])):
        plays.append('Distance Piles')
    elif play_card == '50' and hand_scores[utils.team(player, teams)] + 50 <= trip_length \
      and (board[utils.team(player, teams)][0] == 'R ' or ('RW' in board[utils.team(player, teams)][3] \
      and board[utils.team(player, teams)][0] not in ['OG', 'FT', 'A '])):
        plays.append('Distance Piles')
    elif play_card == '25' and hand_scores[utils.team(player, teams)] + 25 <= trip_length \
      and (board[utils.team(player, teams)][0] == 'R ' or ('RW' in board[utils.team(player, teams)][3] \
      and board[utils.team(player, teams)][0] not in ['OG', 'FT', 'A '])):
        plays.append('Distance Piles')
    return plays

def check_play_possible(hand_scores, board, hands, teams, trip_length):
    team_unique_cards = []
    for team in range(len(teams)):
        team_unique_cards.append([])
    for team in range(len(teams)):
        for plr in teams[team]:
            for card in hands[plr]:
                if card in team_unique_cards[team]:
                    pass
                else:
                    team_unique_cards[team].append(card)
    play_possible = False
    for team in range(len(team_unique_cards)):
        for card in team_unique_cards[team]:
            if not play_possible and card in ['ET', 'PP', 'DA', 'RW']:
                play_possible = True
                break
            elif not play_possible and card == '2%':
                if board[team][2].count('2%') < 2 and hand_scores[team] + 200 <= trip_length \
                  and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
                  and (board[team][0] == 'R ' \
                  or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
                  or ('R ' in team_unique_cards[team] \
                  and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
                  or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
                  or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team])))):
                    play_possible = True
                    break
            elif not play_possible and card == '1%' and hand_scores[team] + 100 <= trip_length \
              and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team])))):
                play_possible = True
                break
            elif not play_possible and card == '75' and hand_scores[team] + 75 <= trip_length \
              and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team])))):
                play_possible = True
                break
            elif not play_possible and card == '50' and hand_scores[team] + 50 <= trip_length \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team])))):
                play_possible = True
                break
            elif not play_possible and card == '25' and hand_scores[team] + 25 <= trip_length \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team])))):
                play_possible = True
                break
            elif not play_possible and ((card == 'R ' and board[team][0] not in ['R ', 'OG', 'FT', 'A '] \
              and not 'RW' in board[team][3]) \
              or (card == 'G ' and board[team][0] == 'OG' and not 'ET' in board[team][3]) \
              or (card == 'ST' and board[team][0] == 'FT' and not 'PP' in board[team][3]) \
              or (card == 'RP' and board[team][0] == 'A ' and not 'DA' in board[team][3]) \
              or (card == 'EL' and board[team][1] == 'SL' and not 'RW' in board[team][3]) \
              and (('25' in team_unique_cards[team] and hand_scores[team] + 25 <= trip_length \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team]))))) \
              or ('50' in team_unique_cards[team] and hand_scores[team] + 50 <= trip_length \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team]))))) \
              or ('75' in team_unique_cards[team] and hand_scores[team] + 75 <= trip_length \
              and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team]))))) \
              or ('1%' in team_unique_cards[team] and card == '1%' and hand_scores[team] + 100 <= trip_length \
              and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team]))))) \
              or ('2%' in team_unique_cards[team] and board[team][2].count('2%') < 2 \
              and hand_scores[team] + 200 <= trip_length \
              and ('SL' not in board[team][1] or 'RW' in board[team][3]) \
              and (board[team][0] == 'R ' \
              or ('RW' in board[team][3] and (board[team][0] not in ['OG', 'FT', 'A '])) \
              or ('R ' in team_unique_cards[team] \
              and ((board[team][0] == 'OG' and 'G ' in team_unique_cards[team]) \
              or (board[team][0] == 'FT' and 'ST' in team_unique_cards[team]) \
              or (board[team][0] == 'A ' and 'RP' in team_unique_cards[team]))))))):
                play_possible = True
                break
    return play_possible

def play(teams, label, player, play_card, board, plays, hand_scores, hands, default_option, play_count, discard_pile):
    victim = -1
    play_list = {}
    undo = False
    draw_again = False
    for i in range(len(plays)):
        play_list.update({i:plays[i]})
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
