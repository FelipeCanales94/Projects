from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv, os, time
from os.path import join as pjoin

# TODO:!!!! IMPORTANT !!!! Account for all edge cases
# TODO: Separate away games from home games.
# TODO: Clean up data. No need for Date, Age, ...etc
# TODO: Organize organize organize! Still have a long way to go
# TODO: Find a way to get all shot coords taken by a player/team and what type of shot they took


# global #
# team abbreviations to get game longs
team_abbreviations = {'Atlanta Hawks': 'ATL',
                      'Brooklyn Nets': 'BRK',
                      'Boston Celtics': 'BOS',
                      'Charlotte Hornets': 'CHO',
                      'Chicago Bulls': 'CHI',
                      'Cleveland Cavaliers': 'CLE',
                      'Dallas Mavericks': 'DAL',
                      'Denver Nuggets': 'DEN',
                      'Detroit Pistons': 'DET',
                      'Golden State Warriors': 'GSW',
                      'Houston Rockets': 'HOU',
                      'Indiana Pacers': 'IND',
                      'Los Angeles Clippers': 'LAC',
                      'Los Angeles Lakers': 'LAL',
                      'Memphis Grizzlies': 'MEM',
                      'Miami Heat': 'MIA',
                      'Milwaukee Bucks': 'MIL',
                      'Minnesota Timberwolves': 'MIN',
                      'New Orleans Pelicans': 'NOP',
                      'New York Knicks': 'NYK',
                      'Oklahoma City Thunder': 'OKC',
                      'Orlando Magic': 'ORL',
                      'Philadelphia 76ers': 'PHI',
                      'Phoenix Suns': 'PHO',
                      'Portland Trail Blazers': 'POR',
                      'Sacramento Kings': 'SAC',
                      'San Antonio Spurs': 'SAS',
                      'Toronto Raptors': 'TOR',
                      'Utah Jazz': 'UTA',
                      'Washington Wizards': 'WAS'}


# web scraping function get team stats for all 82 regular season games and write to a csv file
def getTeamStats(team_name):
    url = 'https://www.basketball-reference.com/boxscores/201810170DET.html'    # url for boxscores
    url2 = 'https://www.basketball-reference.com/teams/BRK/2019_games.html'     # url for schedule
    # 1: Have to separate 'opp' and date from team schedule
    # 2: format it such that it's yyyymmdd0TEAM_Abbreviation
    # 3: webscrape Team Totals
    # 4: find a way to get shot attempt coords from the game
    # 4: save game id and team totals to one csv and shot attempt coords to another csv



# web scraping function to get an individual player's stats for all 82 regular season games and write to a csv file
def individualStats(player_name):
    player_abb = getNameAbb(player_name)  # must get abbreviation used by basketball-reference
    url = 'https://www.basketball-reference.com/players/{}/{}/gamelog/2019'.format(player_abb[0], player_abb)
    bsoup = soup(uReq(url), 'html.parser')  # use BeautifulSoup in order to parse through site

    # Get player's team name and store their data in their respective folder #
    player_team = getPlayerTeam(bsoup)
    createFolder(player_team + '/individual_stats')  # creates new directory using team's name if it doesn't exist
    directory_name = pjoin(player_team + '/individual_stats', str(getPlayerNumber(player_name) + '.csv'))  # puts csv in team directory
    csv_writer = csv.writer(open(directory_name, 'w'))  # opens stream to write into csv

    # Find and iterate through player's data #

    table = bsoup.find("tbody")  # get information on table
    num_rows = len(table.findAll('tr'))  # find number of rows

    # get table header and write to csv
    header = [th.getText() for th in bsoup.find('thead').findAll('tr', limit=2)[0].findAll('th')][1:]
    csv_writer.writerow(header)

    # get all player stats and write to a csv file
    for row in range(num_rows):
        player_stats = [td.getText() for td in table.findAll('tr')[row].findAll('td')]
        csv_writer.writerow(player_stats)


# gets player abbreviation used by basketball-reference
def getNameAbb(player_name):
    return player_name.split(' ')[1].lower().replace("'", "")[0:5] + player_name.split(' ')[0].lower().replace("'", "")[0:2] + '01'


# since no two players can have the same number on a team, we will use their number to name the csv
def getPlayerNumber(player_name):
    with open('Brooklyn_Nets/nets_players.csv', mode='r') as file:
        read_csv = csv.DictReader(file)
        for x in read_csv:
            if x.get('First') == player_name.split(' ')[0] and x.get('Last') == player_name.split(' ')[1]:
                return x.get('\ufeffNum')


# creates folder with team name
def createFolder(player_team):
    newpath = player_team
    if not os.path.exists(newpath):
        os.makedirs(newpath)


# gets player's team
def getPlayerTeam(bsoup):
    for team in bsoup.findAll('p'):
        if 'Team' in team.getText():
            player_team = team.getText()[6:].replace(" ", "_")
    return player_team


# Creates player database for every NBA team.
def getTeamRoster(team_name):
    if team_name in team_abbreviations:  # Make sure it's a valid NBA team
        team_name_fixed = team_name.replace(' ', '_')  # Replace spaces with underscores
        createFolder(team_name_fixed)  # creates team folder if it isn't there already
        directory = team_name_fixed + '/' + team_name_fixed + '_roster.csv'  # directory to write csv

        # start web scraping
        url = 'https://www.basketball-reference.com/teams/{}/2019.html'.format(team_abbreviations.get(team_name))
        bsoup = soup(uReq(url), 'html.parser')

        header = ['Num', 'First', 'Last', 'Pos']  # only need this info from players

        table = bsoup.find('tbody')  # get table info
        num_rows = len(table.findAll('tr'))  # find number of rows

        csv_writer = csv.writer(open(directory, 'w'))  # opens stream to write into csv
        csv_writer.writerow(header)  # write header into

        # get all players's info and write into a csv
        for row in range(num_rows):
            player_num = [th.getText() for th in table.findAll('tr')[row].findAll('th')]  # gets player's number
            players = player_num + [th.getText() for th in table.findAll('tr')[row].findAll('td')][0:3]  # everything else

            # Must check whether or not a player has a first and last name (ex. Nene from the Rockets only has 1 name)
            if ' ' not in players[1]:
                players[3] = players[2]
                players[2] = ''
            else:
                name = players[1].split()  # player name must be split into two parts - First and Last
                players[3] = players[2]  # shift info one index to the right
                players[1] = name[0]
                players[2] = name[1]
                csv_writer.writerow(players)  # write info onto a csv

    else:
        raise TypeError('Not an NBA team!')


# testing
individualStats('D\'Angelo Russell')
individualStats('Joe Harris')
individualStats('Caris Levert')

for x in team_abbreviations.keys():
    getTeamRoster(x)









