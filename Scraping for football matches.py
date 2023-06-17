"""This is a scraping code on football gambling. 
Match day, home team, away team, number of corner kicks and odds will be scraped."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

"""Making empty lists"""
#Using at No.1
list_url_today = []
list_url_tomorrow = []
#Using at No.2
list_corner = []


"""No.1 Going to the homepage and getting URLs of every match"""
url_home = "https://www.betfair.com/sport/football"
r = requests.get(url_home)
soup = BeautifulSoup(r.text,'html.parser')

#Getting in-play's game block, today's game block and tomorrow's game block.
inplay_today_tomorrow = soup.find_all("ul",class_="event-list")
make_sure_three = len(inplay_today_tomorrow)

"""No.2 Getting the URL where is the information we need"""
#for today
if len(inplay_today_tomorrow) > 1:
    #Getting the block of today's games 
    today_match = inplay_today_tomorrow[1]
    #Getting a tag
    list_url_today = [a['href'] for a in today_match.select('a.ui-nav.event-team-container.ui-top.event-link.ui-gtm-click')]
    #Deleting Duplicate data
    list_url_today = list(set(list_url_today))
    #Adding http~
    list_url_today  = ["https://www.betfair.com" + url for url in list_url_today]

else:
    print("There are no values for today's match.")
    
#for tomorrow
if len(inplay_today_tomorrow) > 2:
    #Getting the block of tomorrow's games
    tomorrow_match = inplay_today_tomorrow[2]
    #Getting a tag
    list_url_tomorrow = [a['href'] for a in tomorrow_match.select('a.ui-nav.event-team-container.ui-top.event-link.ui-gtm-click')]
    #Deleting Duplicate data
    list_url_tomorrow = list(set(list_url_tomorrow))
    #Adding http~
    list_url_tomorrow = ["https://www.betfair.com" + url for url in list_url_tomorrow]
else:
    print("There are no values for tomorrow's match.")


"""No.2 Getting home_team, away_team, num_corners and odds"""
#for today
for n in np.arange(len(list_url_today)):
    url_home = list_url_today[n]
    r = requests.get(url_home)
    soup = BeautifulSoup(r.text,'html.parser')

    corner = soup.find("a", title="Cards & Corners")
    href = corner["href"]
    href = "https://www.betfair.com" + href

    url_corner = href
    r = requests.get(url_corner)
    soup = BeautifulSoup(r.text,'html.parser')
    
    """Make sure home team and Away team"""
    home_team = soup.find("td", class_="home-runner").text 
    away_team = soup.find("td", class_="away-runner").text 
    
    corners = soup.find_all("span", class_="runner-name", title=re.compile(r"(?:Under|Over)"))
    
    for corner in corners:
        num_corner = corner.text
        print(num_corner)
        parent_tag = corner.parent
        odds = parent_tag.find("span", class_="ui-runner-price").text
        print(odds)
        
        dicts = {"date": "today",
                 "home_team": home_team,
                 "away_team": away_team,
                 "num_corner": num_corner,
                 "odds": odds}
        list_corner.append(dicts)
    
#for tomorrow
for n in np.arange(len(list_url_tomorrow)):
    url_home = list_url_tomorrow[n]
    r = requests.get(url_home)
    soup = BeautifulSoup(r.text,'html.parser')

    corner = soup.find("a", title="Cards & Corners")
    href = corner["href"]
    href = "https://www.betfair.com" + href

    url_corner = href
    r = requests.get(url_corner)
    soup = BeautifulSoup(r.text,'html.parser')
    
    """Make sure home team and Away team"""
    home_team = soup.find("td", class_="home-runner").text 
    away_team = soup.find("td", class_="away-runner").text 
    
    corners = soup.find_all("span", class_="runner-name", title=re.compile(r"(?:Under|Over)"))
    
    for corner in corners:
        num_corner = corner.text
        print(num_corner)
        parent_tag = corner.parent
        odds = parent_tag.find("span", class_="ui-runner-price").text
        print(odds)
        
        dicts = {"date": "tomorrow",
                "home_team": home_team,
                 "away_team": away_team,
                 "num_corner": num_corner,
                 "odds": odds}
        list_corner.append(dicts)


dataframe_match = pd.DataFrame(list_corner)

dataframe_match.to_excel('output.xlsx', index=False)