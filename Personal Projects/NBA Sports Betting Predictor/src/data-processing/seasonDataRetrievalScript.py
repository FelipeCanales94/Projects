import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv, os, time

class SeasonDataRetrievalScript:

    # Scrape odds starting from 2013 season forward

    def __init__(self):
        return None
    
    def retrieveOldOdds(self):

        #season start date = oct 30-31st, end date = april 16th
        
        date = datetime.date(2014,10,28) # first day of 07 season

        while date != datetime.date(2014,10,29):
            
            # skip months may-september
            if date.month == 5:
                date = datetime.date(date.year,10,25)

            url = 'https://www.sportsbookreview.com/betting-odds/nba-basketball/money-line/full-game/?date={}'.format(date)
            bsoup = soup(uReq(url), 'html.parser')
            # directory_name = pjoin(player_team + '/individual_stats', str(getPlayerNumber(player_name) + '.csv'))  # puts csv in team directory
            # csv_writer = csv.writer(open(directory_name, 'w'))


            tables = bsoup.findAll('div', {'class':'GameRows_threeColumns__O43n1'})  # get information on table
            #num_rows = len(tables.findAll('tr'))  # find number of rows
            # get table header and write to csv
            header = [th.getText() for th in bsoup.findAll('span', {'class':'GameRows_participantBox__0WCRz'})]


            print(header)
            
            date = date + datetime.timedelta(days=1)


    
    def createExcel():
        return None

sr = SeasonDataRetrievalScript()
sr.retrieveOldOdds()