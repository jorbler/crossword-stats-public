from src.getNYTdata import get_data
import pandas as pd
import json
from datetime import date, timedelta
import src.get_all_data as get_all_data
import os

# def get_info():
#     today_date = str(date.today() - timedelta(days=1))
#     today_date_list = str(today_date).split("-")

#     with open("data/user_data.json", 'r') as file:
#         data = json.load(file)
        
#     cookies = {"NYT-S": data["cookie"]}

#     puzzle_types = ["daily", "mini", "bonus"]
#     return today_date, today_date_list, cookies, puzzle_types

def get_last_date() -> str:
    '''Returns the date of the last refresh from the user_data.json file.'''
    with open("data/user_data.json", 'r') as file:
        data = json.load(file)
    last_date = data["last_refresh_date"]
    return last_date

def get_today(puzzle_type: str, start_date: str, end_date: str) -> pd.DataFrame:
    '''Retreives data from last_refresh_date to day before current day and formats it into a DataFrame'''
    with open("data/user_data.json", 'r') as file:
        my_data = json.load(file)
    cookies = {"NYT-S": my_data["cookie"]}

    url = f"https://www.nytimes.com/svc/crosswords/v3//puzzles.json?publish_type={puzzle_type}&sort_order=asc&sort_by=print_date&date_start={start_date}&date_end={end_date}"
    data = json.loads(get_data(url = url, cookies = cookies))["results"]
    metadata = pd.DataFrame(data, dtype = str)
   
    my_stats = {}

    for i in range(len(metadata)):
        this_puzzle_id = metadata["puzzle_id"].values[i]
        url = "https://www.nytimes.com/svc/crosswords/v6/game/" + this_puzzle_id + ".json"
        
        my_stats[this_puzzle_id] = json.loads(get_data(url, cookies))["calcs"]    
        metadata_dedup = metadata.drop_duplicates()
        metadata_dedup = metadata_dedup.reset_index(drop = True).astype("string")

    stats_frame = get_all_data.create_stats_frame(my_stats)
    todays_data = get_all_data.merge_frames(stats_frame, metadata_dedup)
    todays_data = get_all_data.add_days(todays_data)

    return todays_data

def add_todays_data(curr_file_path: str, puzzle_type: str) -> None:
    '''Concatinates the new data to the existing data and saves it. Renames the file to reflect the new last_refresh_date.'''
    today_date = str(date.today() - timedelta(days=1))
    current = pd.read_csv("data/" + curr_file_path)
    start_date = get_last_date(curr_file_path)
    todays_data = get_today(puzzle_type, start_date, today_date)
    new = pd.concat([current, todays_data])
    new = new.drop_duplicates(subset = ["print_date"])
    new.to_csv("data/" + curr_file_path, index = False)
    os.rename(("data/" + curr_file_path), ("data/" + "_".join(curr_file_path.split("_")[:2] + ["".join(today_date.split("-"))]) + ".csv"))

def main() -> None:
    '''Runs full data refresh process, changing the last_refresh_date in data/user_data.json after all data loading is complete.'''
    cur_files = os.listdir("data/")
    
    mini_file = [file for file in cur_files if file.startswith("mini")][0]
    add_todays_data(mini_file, "mini")

    daily_file = [file for file in cur_files if file.startswith("daily")][0]
    add_todays_data(daily_file, "daily")
    
    today_date = str(date.today() - timedelta(days=1))
    if today_date.endswith("01"):
        bonus_file = [file for file in cur_files if file.startswith("bonus")][0]
        add_todays_data(bonus_file, "bonus")

    with open("data/user_data.json", 'r') as file:
        user_data = json.load(file)
    
    user_data["last_refresh_date"] = str(date.today() - timedelta(days=1))
    
    with open('data/user_data.json', 'w') as f:
        json.dump(user_data, f)

if __name__ == "__main__":
    main()
