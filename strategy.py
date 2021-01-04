#!/usr/bin/env python

import utils
import score

def offense(trip_length, hand_scores, teams, board, player, unique_cards, default_card, default_option):
    # Roll
    if 'R ' in unique_cards and (board[utils.team(player, teams)][0] not in ['R ', 'OG', 'FT', 'A '] \
      or board[utils.team(player, teams)][0] in [ 'G ', 'ST', 'RP']) \
      and not 'RW' in board[utils.team(player, teams)][3]:
        default_card = 'R '
        default_option = 'Battle Pile'
    # Distance Piles
    elif ('RW' in board[utils.team(player, teams)][3] \
      and board[utils.team(player, teams)][0] not in ['OG', 'FT', 'A ']) \
      or (board[utils.team(player, teams)][0] == 'R ' and board[utils.team(player, teams)][1] != 'SL'):
        if '2%' in unique_cards and board[utils.team(player, teams)][2].count('2%') < 2 \
          and hand_scores[utils.team(player, teams)] + 200 <= trip_length:
            default_card = '2%'
            default_option = 'Distance Piles'
        elif '1%' in unique_cards and hand_scores[utils.team(player, teams)] + 100 <= trip_length:
            default_card = '1%'
            default_option = 'Distance Piles'
        elif '75' in unique_cards and hand_scores[utils.team(player, teams)] + 75 <= trip_length:
            default_card = '75'
            default_option = 'Distance Piles'
        elif '50' in unique_cards and hand_scores[utils.team(player, teams)] + 50 <= trip_length:
            default_card = '50'
            default_option = 'Distance Piles'
        elif '25' in unique_cards and hand_scores[utils.team(player, teams)] + 25 <= trip_length:
            default_card = '25'
            default_option = 'Distance Piles'
    # Speed Limit, End Limit or Distance Piles
    elif board[utils.team(player, teams)][0] == 'R ' and board[utils.team(player, teams)][1] == 'SL' \
      and 'EL' in unique_cards:
        if  ('2%' in unique_cards and board[utils.team(player, teams)][2].count('2%') < 2 \
          and hand_scores[utils.team(player, teams)] + 200 <= trip_length) or ('1%' in unique_cards \
          and hand_scores[utils.team(player, teams)] + 100 <= trip_length) or ('75' in unique_cards \
          and hand_scores[utils.team(player, teams)] + 75 <= trip_length):
            default_card = 'EL'
            default_option = 'Speed Pile'
        elif '50' in unique_cards and hand_scores[utils.team(player, teams)] + 50 <= trip_length:
            default_card = '50'
            default_option = 'Distance Piles'
        elif '25' in unique_cards and hand_scores[utils.team(player, teams)] + 25 <= trip_length:
            default_card = '25'
            default_option = 'Distance Piles'
    elif board[utils.team(player, teams)][0] == 'R ' and board[utils.team(player, teams)][1] == 'SL' \
      and '50' in unique_cards and hand_scores[utils.team(player, teams)] + 50 <= trip_length:
        default_card = '50'
        default_option = 'Distance Piles'
    elif board[utils.team(player, teams)][0] == 'R ' and board[utils.team(player, teams)][1] == 'SL' \
      and '25' in unique_cards and hand_scores[utils.team(player, teams)] + 25 <= trip_length:
        default_card = '25'
        default_option = 'Distance Piles'
    # Remedies
    elif board[utils.team(player, teams)][0] == 'OG' and 'G ' in unique_cards:
        default_card = 'G '
        default_option = 'Battle Pile'
    elif board[utils.team(player, teams)][0] == 'FT' and 'ST' in unique_cards:
        default_card = 'ST'
        default_option = 'Battle Pile'
    elif board[utils.team(player, teams)][0] == 'A ' and 'RP' in unique_cards:
        default_card = 'RP'
        default_option = 'Battle Pile'
    elif board[utils.team(player, teams)][1] == 'SL' and 'EL' in unique_cards:
        default_card = 'EL'
        default_option = 'Speed Pile'
    # Safeties
    elif board[utils.team(player, teams)][0] == 'OG' and 'ET' in unique_cards:
        default_card = 'ET'
        default_option = 'Safety Area'
    elif board[utils.team(player, teams)][0] == 'FT' and 'PP' in unique_cards:
        default_card = 'PP'
        default_option = 'Safety Area'
    elif board[utils.team(player, teams)][0] == 'A ' and 'DA' in unique_cards:
        default_card = 'DA'
        default_option = 'Safety Area'
    elif (board[utils.team(player, teams)][0].strip() in [ '', 'S', 'G','ST', 'RP' ] \
      or board[utils.team(player, teams)][1] == 'SL') and 'RW' in unique_cards:
        default_card = 'RW'
        default_option = 'Safety Area'
    return default_card, default_option

def OG_hazard(player, unique_cards, teams, label, board, hand_scores, default_card, default_option):
    opponent = []
    opp_scores = {}
    if 'OG' in unique_cards:
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if not 'ET' in board[i][3] and (board[i][0] == 'R ' \
                  or ('RW' in board[i][3] and board[i][0].strip() in ['', 'G', 'ST', 'RP'])):
                    opponent.append(label + ' ' + str(i+1) + ' Battle Pile')
                    opp_scores[i] = hand_scores[i]
        if len(opponent) > 0:
            default_card = 'OG'
            if len(opp_scores) > 1:
                opp_score_max = max(opp_scores, key=opp_scores.get)
                opps_tied = True
                min_opp_score = opp_scores[min(opp_scores)]
                for i, v in opp_scores.iteritems():
                    if opp_scores[i] != min_opp_score:
                        opps_tied = False
                if opps_tied:
                    if utils.team(player, teams) == len(teams)-1:
                        default_option = label + ' 1 Battle Pile'
                    else:
                        default_option = label + ' ' + str(utils.team(player, teams)+2) + ' Battle Pile'
                else:
                    default_option = label + ' ' + str(opp_score_max+1) + ' Battle Pile'
            else:
                default_option = opponent[0]
    return default_card, default_option

def FT_hazard(player, unique_cards, teams, label, board, hand_scores, default_card, default_option):
    opponent = []
    opp_scores = {}
    if 'FT' in unique_cards:
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if not 'PP' in board[i][3] and (board[i][0] == 'R ' \
                  or ('RW' in board[i][3] and board[i][0].strip() in ['', 'G', 'ST', 'RP'])):
                    opponent.append(label + ' ' + str(i+1) + ' Battle Pile')
                    opp_scores[i] = hand_scores[i]
        if len(opponent) > 0:
            default_card = 'FT'
            if len(opp_scores) > 1:
                opp_score_max = max(opp_scores, key=opp_scores.get)
                opps_tied = True
                min_opp_score = opp_scores[min(opp_scores)]
                for i, v in opp_scores.iteritems():
                    if opp_scores[i] != min_opp_score:
                        opps_tied = False
                if opps_tied:
                    if utils.team(player, teams) == len(teams)-1:
                        default_option = label + ' 1 Battle Pile'
                    else:
                        default_option = label + ' ' + str(utils.team(player, teams)+2) + ' Battle Pile'
                else:
                    default_option = label + ' ' + str(opp_score_max+1) + ' Battle Pile'
            else:
                default_option = opponent[0]
    return default_card, default_option

def A_hazard(player, unique_cards, teams, label, board, hand_scores, default_card, default_option):
    opponent = []
    opp_scores = {}
    if 'A ' in unique_cards:
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if not 'DA' in board[i][3] and (board[i][0] == 'R ' \
                  or ('RW' in board[i][3] and board[i][0].strip() in ['', 'G', 'ST', 'RP'])):
                    opponent.append(label + ' ' + str(i+1) + ' Battle Pile')
                    opp_scores[i] = hand_scores[i]
        if len(opponent) > 0:
            default_card = 'A '
            if len(opp_scores) > 1:
                opp_score_max = max(opp_scores, key=opp_scores.get)
                opps_tied = True
                min_opp_score = opp_scores[min(opp_scores)]
                for i, v in opp_scores.iteritems():
                    if opp_scores[i] != min_opp_score:
                        opps_tied = False
                if opps_tied:
                    if utils.team(player, teams) == len(teams)-1:
                        default_option = label + ' 1 Battle Pile'
                    else:
                        default_option = label + ' ' + str(utils.team(player, teams)+2) + ' Battle Pile'
                else:
                    default_option = label + ' ' + str(opp_score_max+1) + ' Battle Pile'
            else:
                default_option = opponent[0]
    return default_card, default_option

def S_hazard(player, unique_cards, teams, label, board, hand_scores, default_card, default_option):
    opponent = []
    opp_scores = {}
    if 'S ' in unique_cards:
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if not 'RW' in board[i][3] and board[i][0] == 'R ':
                    opponent.append(label + ' ' + str(i+1) + ' Battle Pile')
                    opp_scores[i] = hand_scores[i]
        if len(opponent) > 0:
            default_card = 'S '
            if len(opp_scores) > 1:
                opp_score_max = max(opp_scores, key=opp_scores.get)
                opps_tied = True
                min_opp_score = opp_scores[min(opp_scores)]
                for i, v in opp_scores.iteritems():
                    if opp_scores[i] != min_opp_score:
                        opps_tied = False
                if opps_tied:
                    if utils.team(player, teams) == len(teams)-1:
                        default_option = label + ' 1 Battle Pile'
                    else:
                        default_option = label + ' ' + str(utils.team(player, teams)+2) + ' Battle Pile'
                else:
                    default_option = label + ' ' + str(opp_score_max+1) + ' Battle Pile'
            else:
                default_option = opponent[0]
    return default_card, default_option

def SL_hazard(player, unique_cards, teams, label, board, hand_scores, default_card, default_option):
    opponent = []
    opp_scores = {}
    if 'SL' in unique_cards:
        for i in range(len(teams)):
            if i == utils.team(player, teams):
                pass
            else:
                if board[i][1] != 'SL' and not 'RW' in board[i][3]:
                    opponent.append(label + ' ' + str(i+1) + ' Speed Pile')
                    opp_scores[i] = hand_scores[i]
        if len(opponent) > 0:
            default_card = 'SL'
            if len(opp_scores) > 1:
                opp_score_max = max(opp_scores, key=opp_scores.get)
                opps_tied = True
                min_opp_score = opp_scores[min(opp_scores)]
                for i, v in opp_scores.iteritems():
                    if opp_scores[i] != min_opp_score:
                        opps_tied = False
                if opps_tied:
                    if utils.team(player, teams) == len(teams)-1:
                        default_option = label + ' 1 Speed Pile'
                    else:
                        default_option = label + ' ' + str(utils.team(player, teams)+2) + ' Speed Pile'
                else:
                    default_option = label + ' ' + str(opp_score_max+1) + ' Speed Pile'
            else:
                default_option = opponent[0]
    return default_card, default_option

def defense(hand_scores, label, teams, board, player, unique_cards, default_card, default_option):
    #Hazards
    known_safeties = []
    preferred_hazards = []
    remaining_hazards = ['A ', 'OG', 'FT', 'S ', 'SL']
    for i in range(len(teams)):
        for safety in board[i][3]:
            known_safeties.append(safety)
    for card in unique_cards:
        if card in ['RW', 'DA', 'ET', 'PP']:
            known_safeties.append(card)
    for safety in known_safeties:
        if safety == 'RW':
            preferred_hazards.append('S ')
            remaining_hazards.remove('S ')
            preferred_hazards.append('SL')
            remaining_hazards.remove('SL')
        elif safety == 'DA':
            preferred_hazards.append('A ')
            remaining_hazards.remove('A ')
        elif safety == 'ET':
            preferred_hazards.append('OG')
            remaining_hazards.remove('OG')
        elif safety == 'PP':
            preferred_hazards.append('FT')
            remaining_hazards.remove('FT')
    for hazard in preferred_hazards:
        if default_option == '' and hazard == 'OG':
            default_card, default_option = OG_hazard(player, unique_cards, teams, label, board, \
              hand_scores, default_card, default_option)
        elif default_option == '' and hazard == 'FT':
            default_card, default_option = FT_hazard(player, unique_cards, teams, label, board, \
              hand_scores, default_card, default_option)
        elif default_option == '' and hazard == 'A ':
            default_card, default_option = A_hazard(player, unique_cards, teams, label, board, \
              hand_scores, default_card, default_option)
        elif default_option == '' and hazard == 'S ':
            default_card, default_option = S_hazard(player, unique_cards, teams, label, board, \
              hand_scores, default_card, default_option)
        elif default_option == '' and hazard == 'SL':
            default_card, default_option = SL_hazard(player, unique_cards, teams, label, board, \
              hand_scores, default_card, default_option)
    if default_option == '':
        for hazard in remaining_hazards:
            if default_option == '' and hazard == 'OG':
                default_card, default_option = OG_hazard(player, unique_cards, teams, label, board, \
                  hand_scores, default_card, default_option)
            elif default_option == '' and hazard == 'FT':
                default_card, default_option = FT_hazard(player, unique_cards, teams, label, board, \
                  hand_scores, default_card, default_option)
            elif default_option == '' and hazard == 'A ':
                default_card, default_option = A_hazard(player, unique_cards, teams, label, board, \
                  hand_scores, default_card, default_option)
            elif default_option == '' and hazard == 'S ':
                default_card, default_option = S_hazard(player, unique_cards, teams, label, board, \
                  hand_scores, default_card, default_option)
            elif default_option == '' and hazard == 'SL':
                default_card, default_option = SL_hazard(player, unique_cards, teams, label, board, \
                  hand_scores, default_card, default_option)
    return default_card, default_option

def defaults(hands, board, trip_length, teams, hand_scores, label, player, unique_cards, delayed_action):
    default_card = ''
    default_option = ''
    opponent = ''
    end_is_near = False
    walk_off = False
    for i in range(len(hand_scores)):
        if i == utils.team(player, teams):
            miles = hand_scores[i]
            dist_values = []
            for card in hands[i]:
                if card in ['2%', '1%', '75', '50', '25']:
                    dist_values.append(score.score_card(card))
            if (board[i][2].count('2%') == 2 and trip_length - hand_scores[i] in dist_values) \
              or (board[i][2].count('2%') < 2 and trip_length - hand_scores[i] in dist_values):
                end_is_near = True
                walk_off = True
        else:
            if (board[i][2].count('2%') == 2 and trip_length - hand_scores[i] in [100, 75, 50, 25]) \
              or (board[i][2].count('2%') < 2 and trip_length - hand_scores[i] in [200, 100, 75, 50, 25]):
                end_is_near = True
    if delayed_action and not end_is_near:
        end_is_near = True
    # Safeties
    if end_is_near:
        if 'RW' in unique_cards:
            default_card = 'RW'
            default_option = 'Safety Area'
        elif 'DA' in unique_cards:
            default_card = 'DA'
            default_option = 'Safety Area'
        elif 'ET' in unique_cards:
            default_card = 'ET'
            default_option = 'Safety Area'
        elif 'PP' in unique_cards:
            default_card = 'PP'
            default_option = 'Safety Area'
    if default_card == '' and walk_off:
        default_card, default_option = offense(trip_length, hand_scores, teams, board, player, \
          unique_cards, default_card, default_option)
    else:
        default_card, default_option = defense(hand_scores, label, teams, board, player, unique_cards, \
          default_card, default_option)
    if default_card == '':
        default_card, default_option = offense(trip_length, hand_scores, teams, board, player, \
          unique_cards, default_card, default_option)
    # Discard Pile
    if default_card == '':
        default_option = 'Discard Pile'
    if default_card == '' and len(teams) == 2:
        if utils.team(player, teams) == 0:
            opp_team = 1
        else:
            opp_team = 0
        if 'RW' in board[opp_team][3] and 'S ' in unique_cards:
            default_card = 'S '
        elif 'RW' in board[opp_team][3] and 'SL' in unique_cards:
            default_card = 'SL'
        elif 'ET' in board[opp_team][3] and 'OG' in unique_cards:
            default_card = 'OG'
        elif 'PP' in board[opp_team][3] and 'FT' in unique_cards:
            default_card = 'FT'
        elif 'DA' in board[opp_team][3] and 'A ' in unique_cards:
            default_card = 'A '
    if default_card == '' and ('RW' in hands[player] or 'RW' in board[utils.team(player, teams)][3]):
        if 'R ' in unique_cards:
            default_card = 'R '
        elif 'EL' in unique_cards:
            default_card = 'EL'
    if default_card == '' and ('ET' in hands[player] or 'ET' in board[utils.team(player, teams)][3]) \
      and 'G ' in unique_cards:
        default_card = 'G '
    if default_card == '' and ('PP' in hands[player] or 'PP' in board[utils.team(player, teams)][3]) \
      and 'ST' in unique_cards:
        default_card = 'ST'
    if default_card == '' and ('DA' in hands[player] or 'DA' in board[utils.team(player, teams)][3]) \
      and 'RP' in unique_cards:
        default_card = 'RP'
    if default_card == '' and board[utils.team(player, teams)][2].count('2%') + hands[player].count('2%') > 2:
        default_card = '2%'
    if default_card == '' and ('S ' in hands[player] or 'FT' in hands[player] or 'OG' in hands[player] \
      or 'A ' in hands[player] or 'SL' in hands[player]):
        dupes = {}
        for card in unique_cards:
            if card in ['S ', 'FT', 'OG', 'A ', 'SL']:
                dupes[card] = hands[player].count(card)
        dupe_max = max(dupes.values())
        if dupe_max > 1:
            choices = []
            for k in dupes.iterkeys():
                if hands[player].count(k) == dupe_max:
                    choices.append(k)
            default_card = choices[0]
    if default_card == '' and ('R ' in hands[player] or 'ST' in hands[player] or 'G ' in hands[player] \
      or 'RP' in hands[player] or 'EL' in hands[player]):
        dupes = {}
        for card in unique_cards:
            if card in ['R ', 'ST', 'G ', 'RP', 'EL']:
                dupes[card] = hands[player].count(card)
        dupe_max = max(dupes.values())
        if dupe_max > 1:
            choices = []
            for k in dupes.iterkeys():
                if hands[player].count(k) == dupe_max:
                    choices.append(k)
            default_card = choices[0]
    if default_card == '': 
        if 'RW' in board[utils.team(player, teams)][3] and 'R ' in unique_cards:
            default_card = 'R '
        elif 'RW' in board[utils.team(player, teams)][3] and 'EL' in unique_cards:
            default_card = 'EL'
        elif 'ET' in board[utils.team(player, teams)][3] and 'G ' in unique_cards:
            default_card = 'G '
        elif 'PP' in board[utils.team(player, teams)][3] and 'ST' in unique_cards:
            default_card = 'ST'
        elif 'DA' in board[utils.team(player, teams)][3] and 'RP' in unique_cards:
            default_card = 'RP'
    dist_values = []
    for card in hands[player]:
        if card in ['2%', '1%', '75', '50', '25']:
            dist_values.append(score.score_card(card))
    if default_card == '' and len(dist_values) > 0:
        miles = min(dist_values)
        if miles == 25:
            default_card = '25'
        elif miles == 50:
            default_card = '50'
        elif miles == 75:
            default_card = '75'
        elif miles == 100:
            default_card = '1%'
        elif miles == 200:
            default_card = '2%'
    if default_card == '':
        default_card = hands[player][len(hands[player])-1]
    return default_card, default_option

def discard(board, trip_length, teams, hand_scores, label, player, hands, delayed_action):
    unique_cards = []
    for card in hands[player]:
        if card in unique_cards:
            pass
        else:
            unique_cards.append(card)
    default_card, default_option = defaults(hands, board, trip_length, teams, hand_scores, label, player, \
      unique_cards, delayed_action)
    if len(unique_cards) == 1:
        play_card = unique_cards[0]
        hands[player].remove(play_card)
        print "Player %s, your selection is" % str(player+1),
        raw_input(utils.colorize(play_card) + ". Press any key to continue. ")
    else:
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
    return hands, play_card, default_option
