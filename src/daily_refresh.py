from getNYTdata import get_data
import pandas as pd
import json
from datetime import date, timedelta
import get_all_data as get_all_data
import os

today_date = str(date.today() - timedelta(days=1))
today_date_list = str(today_date).split("-")

my_cookie = input("Enter your cookie:")
cookies = {"NYT-S": my_cookie}

puzzle_types = ["daily", "mini", "bonus"]

def get_today(puzzle_type, date):
    url = f"https://www.nytimes.com/svc/crosswords/v3//puzzles.json?publish_type={puzzle_type}&sort_order=asc&sort_by=print_date&date_start={date}&date_end={date}"
    data = json.loads(get_data(url = url, cookies = cookies))["results"]
    metadata = pd.DataFrame(data, dtype = str)

    this_puzzle_id = metadata["puzzle_id"].values[0]
    url = "https://www.nytimes.com/svc/crosswords/v6/game/" + this_puzzle_id + ".json"
    
    my_stats = {}
    my_stats[this_puzzle_id] = json.loads(get_data(url, cookies))["calcs"]    
    metadata_dedup = metadata.drop_duplicates()
    metadata_dedup = metadata_dedup.reset_index(drop = True).astype("string")

    stats_frame = get_all_data.create_stats_frame(my_stats)
    todays_data = get_all_data.merge_frames(stats_frame, metadata_dedup)
    todays_data = get_all_data.add_days(todays_data)
    
    return todays_data

def add_todays_data(curr_file_path, puzzle_type):
    current = pd.read_csv("data/" + curr_file_path)
    todays_data = get_today(puzzle_type, today_date)
    new = pd.concat([current, todays_data])
    new = new.drop_duplicates(subset = ["print_date"])
    new.to_csv("data/" + curr_file_path, index = False)
    os.rename(("data/" + curr_file_path), ("data/" + "_".join(curr_file_path.split("_")[:2] + ["".join(today_date.split("-"))]) + ".csv"))

if __name__ == "__main__":
    os.chdir("/Users/jordanlerner/crossword-stats/")
    cur_files = os.listdir("data/")
    
    mini_file = [file for file in cur_files if file.startswith("mini")][0]
    add_todays_data(mini_file, "mini")

    daily_file = [file for file in cur_files if file.startswith("daily")][0]
    add_todays_data(daily_file, "daily")

    if today_date.endswith("01"):
        bonus_file = [file for file in cur_files if file.startswith("bonus")][0]
        add_todays_data(bonus_file, "bonus")