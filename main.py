import json
from time import sleep

import pandas as pd
import requests
from tqdm import tqdm

start_season = 1996
end_season = 2022

seasons = [
    f"{season}-{str(season + 1)[-2:]}" for season in range(start_season, end_season + 1)]

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nba.com/",
    "Connection": "keep-alive",
}

all_seasons_data = pd.DataFrame()

base_url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={season}&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision="

for season in tqdm(seasons):
    url = base_url.format(season=season)
    response = requests.get(url, headers=request_headers)
    data = json.loads(response.text)
    headers = data["resultSets"][0]["headers"]
    rows = data["resultSets"][0]["rowSet"]
    df = pd.DataFrame(rows, columns=headers)
    df["SEASON"] = season
    all_seasons_data = pd.concat([all_seasons_data, df], ignore_index=True)
    sleep(2)

all_seasons_data.to_csv("data/team_stats_defense_po.csv", index=False)
