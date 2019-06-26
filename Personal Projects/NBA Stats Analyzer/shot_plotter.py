import requests
import urllib.request

import socket
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


#   TODO: Find way to separate made and missed shots in shot types/shot zones, shot areas
#   TODO: Check if there is an easier way to check certain conditions (ex. Shot type = layup && ShotMade = False)
#   TODO: Check how to make missed shots Xs
#   TODO: Edge cases for layups and dunks
#   TODO: Clean up Clean up 

# Maybe make the table a global variable? ----> Weigh out pros and cons
# Scatter plots for now


#Constants

# Needed in order to make requests to stats.nba.com
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),  # noqa: E501
    'Dnt': ('1'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'origin': ('http://stats.nba.com')
    }

#def getPlayerID(player_name):


def getTable():

    # James Harden info parameters test
    playerInfo = {
        'PlayerID': '2544',
        'Season': '2018-19',
        'SeasonType': 'Regular+Season',
        'ContextMeasure': 'FGA',
        'LastNGames': '0',
        'LeagueID': '00',
        'Month': '0',
        'OpponentTeamID': '0',
        'Period': '0',
        'TeamID': '0',
    }

    # URL to be used
    buckets_url = 'http://stats.nba.com/stats/shotchartdetail?PlayerID={}&Season={}&SeasonType={}&PlayerPosition=&' \
                  'ContextMeasure={}&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames={}&LeagueID={}&Location=&Month={}' \
                  '&OpponentTeamID={}&Outcome=&Period={}&Position=&RookieYear=&SeasonSegment=&TeamID={}&VsConference=' \
                  '&VsDivision='.format(playerInfo.get('PlayerID'), playerInfo.get('Season'), playerInfo.get('SeasonType'),
                                        playerInfo.get('ContextMeasure'), playerInfo.get('LastNGames'), playerInfo.get('LeagueID'),
                                        playerInfo.get('Month'), playerInfo.get('OpponentTeamID'), playerInfo.get('Period'), playerInfo.get('TeamID'))

    # Information needed
    response = requests.get(buckets_url, headers=HEADERS)   # Request player info from api
    headers = response.json()['resultSets'][0]['headers']   # Gets headers
    shots = response.json()['resultSets'][0]['rowSet']      # Gets all player info in regards to their shot
    tables = pd.DataFrame(shots, columns=headers)          # Table of shots and headers

    return tables


# Plots all missed shots
def plotMissedShots(table):
    missed_shots = table[table.EVENT_TYPE == "Missed Shot"]
    plt.figure(figsize=(12, 11))
    plt.scatter(missed_shots.LOC_X, missed_shots.LOC_Y, color='red', facecolors='none')
    plt.show()

# Plots all made shots
def plotMadeShots(table):

    made_shots = table[table.EVENT_TYPE == "Made Shot"]
    plt.figure(figsize=(12, 11))
    plt.scatter(made_shots.LOC_X, made_shots.LOC_Y, color='blue')
    plt.show()


#Plots all shots Made or Missed
def plotAll(table):
    made_shots = table[table.EVENT_TYPE == 'Made Shot']
    missed_shots = table[table.EVENT_TYPE == 'Missed Shot']

    plt.scatter(made_shots.LOC_X, made_shots.LOC_Y, color='green')
    plt.scatter(missed_shots.LOC_X, missed_shots.LOC_Y, color='red')
    plt.figure(figsize=(12, 11))
    plt.show()


# only plot 3 point shots
def plotThreePointers(table):

    threePointShots = table[table.SHOT_TYPE == '3PT Field Goal']
    plt.scatter(threePointShots.LOC_X, threePointShots.LOC_Y)
    plt.figure(figsize=(12, 11))
    plt.show()


# only plot 2 point shots
def plotTwoPointers(table):
    twoPointShots = table[table.SHOT_TYPE == '2PT Field Goal']

    plt.scatter(twoPointShots.LOC_X, twoPointShots.LOC_Y)
    plt.figure(figsize=(12, 11))
    plt.show()

# only plot layups
def plotLayups(table):

    # So many different types of layups. Figure out an easier way to check conditions
    layups = table[table.ACTION_TYPE == 'Layup Shot']
    driving_layups = table[table.ACTION_TYPE == 'Driving Layup Shot']
    cutting_layups = table[table.ACTION_TYPE == 'Cutting Layup Shot']
    running_layups = table[table.ACTION_TYPE == 'Running Layup Shot']
    putback_layups = table[table.ACTION_TYPE == 'Putback Layup Shot']
    alley_layups = table[table.ACTION_TYPE == 'Alley Oop Layup shot']
    driving_finger_rolll = table[table.ACTION_TYPE == 'Driving Finger Roll Layup Shot']
    finger_roll = table[table.ACTION_TYPE == 'Finger Roll Layup Shot']
    tip_layup = table[table.ACTION_TYPE == 'Tip Layup Shot']  # Tip in layups should count as putbacks -_-
    reverse_layup = table[table.ACTION_TYPE == 'Reverse Layup Shot']

    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()

# only plot dunks
def plotDunks(table):
    dunks = table[table.ACTION_TYPE == 'Dunk Shot']
    driving_dunks = table[table.ACTION_TYPE == 'Driving Dunk Shot']
    cutting_dunks = table[table.ACTION_TYPE == 'Cutting Dunk Shot']
    running_dunks = table[table.ACTION_TYPE == 'Running Dunk Shot']
    alley_dunk = table[table.ACTION_TYPE == 'Alley Oop Dunk Shot']
    running_alley = table[table.ACTION_TYPE == 'Running Alley Oop Dunk Shot']
    putback_dunk = table[table.ACTION_TYPE == 'Putback Dunk Shot']
    reverse_dunk = table[table.ACTION_TYPE == 'Running Reverse Dunk Shot']


    plt.scatter(dunks.LOC_X, dunks.LOC_Y)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()

# Shots taken less than 8 foot from the basket
def lessThanEight(table):
    less_eight = table[table.SHOT_ZONE_RANGE == 'Less Than 8 ft.']

    plt.scatter(less_eight.LOC_X, less_eight.LOC_Y)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()

# Shots taken 8-16 foot from the basket
def eightSixteen(table):
    eight_sixteen = table[table.SHOT_ZONE_RANGE == '8-16 ft.']

    plt.scatter(eight_sixteen.LOC_X, eight_sixteen.LOC_Y)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()

# Shots taken 16-24 foot from the basket
def sixTeenTwoFour(table):
    sixteen_twentyfour = table[table.SHOT_ZONE_RANGE == '16-24 ft.']

    plt.scatter(sixteen_twentyfour.LOC_X, sixteen_twentyfour.LOC_Y)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()

# Shots taken 24+ feet from basket
def TwoFourPlus(table):
    twentyfour_up = table[table.SHOT_ZONE_RANGE == '24+ ft.']

    plt.scatter(twentyfour_up.LOC_X, twentyfour_up.LOC_Y)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    plt.figure(figsize=(12, 11))
    plt.show()


# Tests
table = getTable()
lessThanEight(table)
TwoFourPlus(table)

