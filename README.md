# Mille Bornes

## Games
### 1 Player (mb1p.py)
* for one player against the computer (2, 3, 4, or 6 player game)
* 4 and 6 player games are 2 and 3 team games respectively
* each player is dealt 6 cards
* each hand is to 1000 miles (4 players) or 700 miles (2, 3, or 6 players)
* hands can be extended from 700 miles to 1000 miles (2, 3, or 6 players)
* each game is to 5000 points
* a shutout is scored when you complete a trip and your opponents have 0 milestones
* mb1p.py optionally takes one argument:
  * number of players (2, 3, 4, or 6)

### Auto (mb_auto.py)
* automated game computer vs computer (2, 3, 4, or 6 player game)
* 4 and 6 player games are 2 and 3 team games respectively
* each player is dealt 6 cards
* each hand is to 1000 miles (4 players) or 700 miles (2, 3, or 6 players)
* hands can be extended from 700 miles to 1000 miles (2, 3, or 6 players)
* each game is to 5000 points
* a shutout is scored when you complete a trip and your opponents have 0 milestones
* mb1p.py optionally takes one argument:
* mb_auto.py optionally takes three arguments:
  * number of players (2, 3, 4, or 6)
  * number of games (integer greater than zero)
  * pause between hands flag (Y/N)

## Cards
### Safeties
* [ET] Extra Tank, 1
* [PP] Puncture-proof, 1
* [DA] Driving Ace, 1
* [RW] Right-of-Way, 1

### Remedies
* [G ] Gasoline, 6
* [ST] Spare tire, 6
* [RP] Repairs, 6
* [EL] End of Limit, 6
* [R ] Roll, 14

### Hazards
* [OG] Out of gas, 3
* [FT] Flat tire, 3
* [A ] Accident, 3
* [SL] Speed limit, 4
* [S ] Stop, 5

### Distance
* [2%] 200, 4
* [1%] 100, 12
* [75] 75, 10
* [50] 50, 10
* [25] 25, 10

## Round Scoring
* Milestones played
* Each safety card played, 100
* All 4 safties played, 300
* Each "coup fourre", 300
* Trip completed, 400
* Delayed action, 300
* Safe trip (no 200's), 300
* Extension, 200
* Shut-out, 500