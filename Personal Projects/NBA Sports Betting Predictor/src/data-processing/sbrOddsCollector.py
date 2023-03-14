from sbrscrape import Scoreboard

class SbrOddsCollector:

    # json reference: https://pypi.org/project/sbrscrape/0.0.6/

    def __init__(self) -> None:
        sbr = Scoreboard(sport='NBA')
        self.sportsbook = 'fanduel' # fanduel as an example, will rotate between other sportsbooks in future
        self.games = sbr.games
    
    # function to get odds from scraper
    def getData(self):

        res = {}

        for game in self.games:
            money_line_home = money_line_away = None

            if self.sportsbook in game['home_ml']:
                money_line_home = game['home_ml'][self.sportsbook]
            
            if self.sportsbook in game['away_ml']:
                money_line_away = game['away_ml'][self.sportsbook]

            home_team = game['home_team_abbr']
            away_team = game['away_team_abbr']

            res[home_team+'_'+away_team] = [money_line_home, money_line_away]

        return res