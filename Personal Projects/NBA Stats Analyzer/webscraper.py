from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv, os
from os.path import join as pjoin

# TODO:!!!! IMPORTANT !!!! Account for all edge cases
# TODO: Separate away games from home games.
# TODO: Clean up data. No need for Date, Age, ...etc
# TODO: Figure out a way to organize by creating a new Folder labeled with the Team's Name. Within that folder,
#       have team stats, individual stats
# TODO: Organize organize organize! Still have a long way to go
# TODO: create function that grabs all team stats
# TODO: find a way to get all shots taken by a player/team


# global #
# team abbreviations to get game longs
team_abbreviations = {'Atlanta Hawks': 'ATL',
                     'Brooklyn Nets': 'BRK',
                     'Boston Celtics': 'BOS',
                     'Charlotte Hornets': 'CHA',
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
                     'Phoenix Suns': 'PHX',
                     'Portland Trail Blazers': 'POR',
                     'Sacramento Kings': 'SAC',
                     'San Antonio Spurs': 'SAS',
                     'Toronto Raptors': 'TOR',
                     'Utah Jazz': 'UTA',
                     'Washington Wizards': 'WAS'}

# web scraping function get team stats for all 82 regular season games and write to a csv file
def getTeamStats(team_name):
    placeholder = ''


# web scraping function to get an individual player's stats for all 82 regular season games and write to a csv file
def individualStats(player_name):


    player_abb = getNameAbb(player_name)    # must get abbreviation used by basketball-reference
    url = 'https://www.basketball-reference.com/players/{}/{}/gamelog/2019'.format(player_abb[0], player_abb)
    bsoup = soup(uReq(url), 'html.parser')  # use BeautifulSoup in order to parse through site

    # Get player's team name and store their data in their respective folder #
    player_team = getPlayerTeam(bsoup)
    createFolder(player_team + '/individual_stats')   # creates new directory using team's name if it doesn't exist
    directory_name = pjoin(player_team + '/individual_stats', str(getPlayerNumber(player_name) + '.csv')) # puts csv in team directory
    csv_writer = csv.writer(open(directory_name, 'w'))  # opens stream to write into csv

    # Find and iterate through player's data #

    table = bsoup.find("tbody")     # get information on table
    num_rows = len(table.findAll('tr'))     # find number of rows

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
            if(x.get('First') == player_name.split(' ')[0] and x.get('Last') == player_name.split(' ')[1]):
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


# test
individualStats('D\'Angelo Russell')
individualStats('Joe Harris')
individualStats('Caris Levert')









