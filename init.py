#!/usr/bin/env python

import random

def initialize_game(num_players):
    hand_count = 0
    if num_players == 2 or num_players == 4:
        num_teams = 2
    else:
        num_teams = 3
    teams = []
    for team in range(num_teams):
        teams.append([])
    t = 0
    for plr in range(num_players):
        teams[t].append(plr)
        if t == num_teams-1:
            t = 0
        else:
            t += 1 
    if len(teams[0]) > 1:
        label = "Team"
    else:
        label = "Player"
    game_scores = []
    for i in range(len(teams)):
        game_scores.append(0)
    player = -1
    goes_first = random.randint(0,num_players-1)
    if num_players == 4:
        deck = {0:"ET",
                1:"PP",
                2:"DA",
                3:"RW",
                4:"G ", 5:"G ", 6:"G ", 7:"G ", 8:"G ", 9:"G ",
                10:"ST", 11:"ST", 12:"ST", 13:"ST", 14:"ST", 15:"ST",
                16:"RP", 17:"RP", 18:"RP", 19:"RP", 20:"RP", 21:"RP",
                22:"EL", 23:"EL", 24:"EL", 25:"EL", 26:"EL", 27:"EL",
                28:"R ", 29:"R ", 30:"R ", 31:"R ", 32:"R ", 33:"R ", 34:"R ",
                35:"R ", 36:"R ", 37:"R ", 38:"R ", 39:"R ", 40:"R ", 41:"R ",
                42:"OG", 43:"OG", 44:"OG",
                45:"FT", 46:"FT", 47:"FT",
                48:"A ", 49:"A ", 50:"A ",
                51:"SL", 52:"SL", 53:"SL", 54:"SL",
                55:"S ", 56:"S ", 57:"S ", 58:"S ", 59:"S ",
                60:"2%", 61:"2%", 62:"2%", 63:"2%",
                64:"1%", 65:"1%", 66:"1%", 67:"1%", 68:"1%", 69:"1%",
                70:"1%", 71:"1%", 72:"1%", 73:"1%", 74:"1%", 75:"1%",
                76:"75", 77:"75", 78:"75", 79:"75", 80:"75", 81:"75", 82:"75", 83:"75", 84:"75", 85:"75",
                86:"50", 87:"50", 88:"50", 89:"50", 90:"50", 91:"50", 92:"50", 93:"50", 94:"50", 95:"50",
                96:"25", 97:"25", 98:"25", 99:"25", 100:"25", 101:"25", 102:"25", 103:"25", 104:"25", 105:"25"}
    else:
        deck = {0:"ET",
                1:"PP",
                2:"DA",
                3:"RW",
                4:"G ", 5:"G ", 6:"G ", 7:"G ", 8:"G ", 9:"G ",
                10:"ST", 11:"ST", 12:"ST", 13:"ST", 14:"ST", 15:"ST",
                16:"RP", 17:"RP", 18:"RP", 19:"RP", 20:"RP", 21:"RP",
                22:"EL", 23:"EL", 24:"EL", 25:"EL", 26:"EL", 27:"EL",
                28:"R ", 29:"R ", 30:"R ", 31:"R ", 32:"R ", 33:"R ", 34:"R ",
                35:"R ", 36:"R ", 37:"R ", 38:"R ", 39:"R ", 40:"R ", 41:"R ",
                42:"OG", 43:"OG",
                44:"FT", 45:"FT",
                46:"A ", 47:"A ",
                48:"SL", 49:"SL", 50:"SL",
                51:"S ", 52:"S ", 53:"S ", 54:"S ",
                55:"2%", 56:"2%", 57:"2%", 58:"2%",
                59:"1%", 60:"1%", 61:"1%", 62:"1%", 63:"1%", 64:"1%",
                65:"1%", 66:"1%", 67:"1%", 68:"1%", 69:"1%", 70:"1%",
                71:"75", 72:"75", 73:"75", 74:"75", 75:"75", 76:"75", 77:"75", 78:"75", 79:"75", 80:"75",
                81:"50", 82:"50", 83:"50", 84:"50", 85:"50", 86:"50", 87:"50", 88:"50", 89:"50", 90:"50",
                91:"25", 92:"25", 93:"25", 94:"25", 95:"25", 96:"25", 97:"25", 98:"25", 99:"25", 100:"25"}
    return hand_count, game_scores, teams, deck, label, player, goes_first

def initialize_hand(num_players, teams, deck, label, player, hand_count, goes_first):
    play_count = 0
    hand_count += 1
    draw_pile = deck.values()
    random.shuffle(draw_pile)
    discard_pile = []
    hand_scores = []
    board = []
    trip_completed = []
    cf_count = []
    for i in range(len(teams)):
        hand_scores.append(0)
        board.append(['','',[],[]])
        trip_completed.append(False)
        cf_count.append(0)
    if num_players == 4: 
        trip_length = 1000
    else:
        trip_length = 700
    extension = False
    delayed_action = False
    draw_again = False
    play_possible = True
    cf = False
    if player == -1:
        player = goes_first
    elif player == num_players - 1:
        player = 0
    else:
        player += 1
    return play_count, hand_count, hand_scores, board, draw_pile, discard_pile, trip_length, \
      extension, delayed_action, trip_completed, player, draw_again, cf_count, cf, play_possible
