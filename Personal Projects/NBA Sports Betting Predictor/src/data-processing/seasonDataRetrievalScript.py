import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv, os, time
from os.path import join as pjoin
from pathlib import Path

class SeasonDataRetrievalScript:
    # Scrape odds starting from 2013 season forward

    #TODO: Finish this webscraper -> get all archived data -> check for more features

    def __init__(self):
        self.csv_headers = ['Date', 'ROT' 'Winning Team', '1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter', 'Final', 'ML']
    
    def retrieveOldOdds(self):

        #season start date = oct 30-31st, end date = april 16th
        
        date = datetime.date(2014,10,28) # first day of '14 season
        path = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent) + '/data/seasonOddsDatasets/'
        
        while date != datetime.date(2014,10,29):
            odds_year = str(date.year) + '-' + str(date.year + 1)
            directory_name = pjoin(path,  odds_year + '.csv')  # puts csv in team directory
            csv_writer = csv.writer(open(directory_name, 'w'))
            
            # skip months may-september
            if date.month == 5:
                date = datetime.date(date.year,10,25)

            url = 'https://www.sportsbookreview.com/betting-odds/nba-basketball/money-line/full-game/?date={}'.format(date)
            bsoup = soup(uReq(url), 'html.parser')
                        
            # get table header and write to csv
            team_names = [th.getText() for th in bsoup.findAll('span', {'class':'GameRows_participantBox__0WCRz'})]
            team_final_scores = [th.getText() for th in bsoup.findAll('div', {'class':'GameRows_scores__YkN24'})]
            team_rot = [th.getText() for th in bsoup.findAll('span', {'class':'GameRows_smallNumber__q50_o'})]
            team_scoreboards = [th.getText() for th in bsoup.findAll('div', {'class':'BoxScore_scoreboardColumn__x0cEb'}) if len(th.getText()) > 6] 
            quarter_scores_processed = []
            away_scores = []
            home_scores = []


            for i in range(len(team_scoreboards)):
                if i % 4 == 0 and i != 0: # skip totals
                    quarter_scores_processed.append(away_scores)
                    quarter_scores_processed.append(home_scores)
                    away_scores = []
                    home_scores = []
                    
                unprocessed_score = team_scoreboards[i]
                away_score = unprocessed_score[:2]
                home_score = unprocessed_score[-2:]
                away_scores.append(away_score)
                home_scores.append(home_score)

            quarter_scores_processed.append(away_scores)
            quarter_scores_processed.append(home_scores)
           

            for i in range(len(team_names)):
                csv_writer.writerow([team_names[i], team_rot[i], quarter_scores_processed[i][0], quarter_scores_processed[i][1], quarter_scores_processed[i][2], quarter_scores_processed[i][3], team_final_scores[i]])
            
            date = date + datetime.timedelta(days=1)


    
    def createExcel():
        return None

sr = SeasonDataRetrievalScript()
sr.retrieveOldOdds()