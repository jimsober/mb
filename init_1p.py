#!/usr/bin/env python

import random

def initialize_game(num_players):
    hand_count = 0
    if num_players == 2:
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
