#!/usr/bin/env python
# coding: utf-8

# https://sportsreference.readthedocs.io/en/stable/
# pip install sportsipy
# Out-dated, no longer works :(
# https://stackoverflow.com/questions/70519889/when-i-run-the-sportsipy-nba-teams-teams-function-i-am-getting-notified-that-the


# https://pypi.org/project/sports.py/
# pip install sports.py


# https://stackoverflow.com/questions/21332597/how-can-i-get-the-scores-and-schedules-using-espn-api

import argparse
import sys
import os
import shutil
import requests
import pandas as pd
from bs4 import BeautifulSoup
#https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/
import re

__author__ = "Ike Starnes"
__copyright__ = "Copyright (c) 2024 Ike Starnes, all rights reserved."

def get_nba_boxscore():
    url = 'https://www.cbssports.com/nba/gametracker/boxscore/NBA_20240530_DAL@MIN/'
    # url = 'https://www.bing.com/sportsdetails?q=Mavericks%20vs%20Timberwolves&gameid=SportRadar_Basketball_NBA_2023_Game_d8fee11e-c90d-4d0e-9f9d-2ae27e6c0348&league=Basketball_NBA&scenario=GameCenter&intent=Game&iscelebratedgame=True&TimezoneId=Eastern%20Standard%20Time&sport=Basketball&seasonyear=2023&team=SportRadar_Basketball_NBA_2023_Team_583eca2f-fb46-11e1-82cb-f4ce4684ea4c&team2=SportRadar_Basketball_NBA_2023_Team_583ecf50-fb46-11e1-82cb-f4ce4684ea4c&venueid={%22id%22:%22SportRadar_Basketball_NBA_2023_Venue_7aed802e-3562-5b73-af1b-3859529f9b95%22}:version-1&segment=sports&isl2=true&IsAutoRefreshEnabled=true&'
    # url = 'https://www.livesport.com/game/2V13yfaE/#/game-summary/player-statistics/0'
    # url = 'https://www.espn.com/nba/boxscore/_/gameId/401672980'
    # url = 'https://www.nba.com/game/dal-vs-min-0042300315/box-score#box-score'
    # url = 'https://www.aiscore.com/basketball/match-minnesota-timberwolves-dallas-mavericks/o07dzsmv6nmcmkn/boxscore'
    html = requests.get(url).text.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find_all('table', class_='stats-table')
    boxscoretable = pd.read_html(str(table))
    print('---------------------------------------------------------------------------')
    bsa1 = boxscoretable[0]
    bsa2 = boxscoretable[2]
    bsh1 = boxscoretable[3]
    bsh2 = boxscoretable[5]
    away = pd.concat([bsa1, bsa2], ignore_index=True, sort=False)
    home = pd.concat([bsh1, bsh2], ignore_index=True, sort=False)
    boxscore = pd.concat([home, away], ignore_index=True, sort=False)
    print(boxscore)
    print('---------------------------------------------------------------------------')
    boxscore.to_excel('C:/Temp/TTT/ttt.xlsx')

def get_draftkings_data():
    from draft_kings import Sport, Client
    mlb_games = Client().contests(sport=Sport.MLB)
   
    for game in mlb_games.draft_groups:
        #print(game)
        players = Client().available_players(draft_group_id=game.draft_group_id)
        print(players.team_series)

def main():
    """Main Function"""

    print ('hello foo bar')

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in-value', dest='input_value', required=True, help='Enter a value')
    args = parser.parse_args()

    print(f'Hello Python in VS Code: {args.input_value}')

    import sys
    a_list = []
    a_tuple = ()
    a_list = ["Geeks", "For", "Geeks"]
    a_tuple = ("Geeks", "For", "Geeks")
    print(sys.getsizeof(a_list))
    print(sys.getsizeof(a_tuple))


if __name__ == "__main__":
    main()
    print('Done.')
