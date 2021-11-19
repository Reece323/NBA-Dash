import os
import re
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguestandings


def get_colors(teamname):
    if teamname == 'New Orleans Pelicans':
        teamname = 'New Orleans Pelicans Team'
    URL = f"https://teamcolorcodes.com/{teamname.replace(' ', '-').lower()}-color-codes/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    colors = []
    for i in soup.find_all(class_='colorblock'):
        hex = re.compile(r'#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})(?=;|[^(]*\))').findall(i.text)
        if len(hex) > 0:
            colors.append(hex[0])

    if teamname == 'San Antonio Spurs':
        colors[0] = '#000000'
        colors[1] = '#C4CED4'
    return colors

team_colors = {
    "Atlanta Hawks": ["#e03a3e", "#C1D32F", "#26282A", "#C8102E", "#FFCD00", "#87674F", "#000000"], 
    "Boston Celtics": ["#007A33", "#BA9653", "#963821", "#E59E6D", "#000000"], 
    "Brooklyn Nets": ["#000000", "#FFFFFF", "#002A60", "#CD1041", "#777D84", "#C6CFD4", "#FFFFFF"], 
    "Charlotte Bobcats": ["#2e5a8b", "#f26432", "#959da0", "#232020"],  
    "Charlotte Hornets": ["#1d1160", "#00788C", "#A1A1A4", "#00778B", "#280071", "#F9423A"], 
    "Chicago Bulls": ["#CE1141", "#000000"], 
    "Cleveland Cavaliers": ["#860038", "#041E42", "#FDBB30", "#000000", "#E35205", "#5C88DA", "#27251F", "#DC3B34", "#04225C", "#FFFFFF"], 
    "Dallas Mavericks": ["#00538C", "#B8C4CA", "#002B5E", "#000000", "#002855", "#00843D"], 
    "Denver Nuggets": ["#0E2240", "#FEC524", "#8B2131", "#1D428A", "#00285E", "#418FDE", "#FDB927", "#041E42", "#9D2235", "#8B6F4E"], 
    "Detroit Pistons": ["#C8102E", "#1d42ba", "#bec0c2", "#002D62", "#ED174C", "#006BB6", "#bec0c2", "#002D62", "#D50032", "#003DA5", "#041E42", "#9D2235", "#FFA300", "#006272", "#8A8D8F", "#000000"], 
    "Golden State Warriors": ["#1D428A", "#ffc72c", "#006BB6", "#FDB927", "#26282A", "#041E42", "#BE3A34", "#FFA300", "#00A9E0", "#FFCD00"], 
    "Houston Rockets": ["#CE1141", "#000000", "#C4CED4", "#041E42", "#2C7AA1", "#BA0C2F", "#8A8D8F", "#BA0C2F", "#000000", "#FFC72C"], 
    "Indiana Pacers": ["#002D62", "#FDBB30", "#BEC0C2"], 
    "Los Angeles Clippers": ["#c8102E", "#1d428a", "#BEC0C2", "#000000"], 
    "Los Angeles Lakers": ["#552583", "#FDB927", "#000000"], 
    "Memphis Grizzlies": ["#5D76A9", "#12173F", "#F5B112", "#707271", "#6189B9", "#00285E", "#FDB927", "#BED4E9", "#00B2A9", "#E43C40", "#BC7844", "#040204", "#FFFFFF"], 
    "Miami Heat": ["#98002E", "#F9A01B", "#000000", "#41B6E6", "#db3eb1", "#000000", "#FFFFFF", "#BA0C2F", "#FEDD00", "#000000"], 
    "Milwaukee Bucks": ["#00471B", "#D5C8AD", "#0077c0", "#000000", "#AC1a2f", "#274e37", "#95999d", "#FFFFFF", "#702F8A", "#2C5234", "#8A8D8F", "#009429", "#f7a500", "#FFFFFF", "#000000"], 
    "Minnesota Timberwolves": ["#0C2340", "#236192", "#9ea2a2", "#78BE20", "#221C35", "#981D97", "#FFFFFF", "#236192", "#00843D", "#8A8D8F", "#000000", "#FFD700", "#C8102E", "#24429C", "#1CA64C", "#848A8C", "#FFFFFF"], 
    "New Orleans Pelicans": ["#0C2340", "#C8102E", "#85714D"], 
    "New York Knicks": ["#006BB6", "#F58426", "#BEC0C2", "#000000", "#0072CE", "#FE5000", "#8A8D8F", "#000000"], 
    "Oklahoma City Thunder": ["#007ac1", "#ef3b24", "#002D62", "#fdbb30"], 
    "Orlando Magic": ["#0077c0", "#C4ced4", "#000000"], 
    "Philadelphia 76ers": ["#006bb6", "#ed174c", "#002B5C", "#c4ced4", "#006bb6", "#D50032", "#BB9754", "#040204", "#002F6C", "#D50032"], 
    "Phoenix Suns": ["#1d1160", "#e56020", "#000000", "#63727A", "#F9AD1B", "#B95915", "#Bec0c2", "#FF6900", "#FE5000", "#EF3340", "#5F259F", "#000000"], 
    "Portland Trail Blazers": ["#E03A3E", "#000000"], 
    "Sacramento Kings": ["#5a2d81", "#63727A", "#000000", "#542e91", "#c4ced4", "#000000"], 
    "San Antonio Spurs": ["#000000", "#C4CED4", "#8a8d8f", "#000000", "#EF426F", "#00B2A9", "#FF8200"], 
    "Toronto Raptors": ["#ce1141", "#000000", "#A1A1A4", "#B4975A", "#753BBD", "#BA0C2F", "#8A8D8F", "#000000"], 
    "Utah Jazz": ["#002B5C", "#F9A01B", "#F9A01B", "#00471B", "#3E2680", "#6CAEDF", "#753BBD", "#00A9E0", "#006272", "#954E4C"], 
    "Washington Wizards": ["#002B5C", "#e31837", "#C4CED4"]
    }
