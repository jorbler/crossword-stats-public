import pandas as pd
from getNYTdata import get_data
import json
from datetime import datetime
from tqdm import tqdm

puzzle_types = ["daily", "mini", "bonus"]

def retrieve_data(puzzle_type, start_date, cookies):
    if puzzle_type == "mini":
        first_days = list(pd.date_range(start = start_date, end = pd.Timestamp("today"), freq = "MS").astype(str))
        first_days = [i.split("-") for i in first_days]
    else:
        first_days = list(pd.date_range(start = start_date, end = pd.Timestamp("today"), freq = "MS").astype(str))
        first_days = [i.split("-") for i in first_days]
    
    metadata = pd.DataFrame(columns = ['author', 'editor', 'format_type', 'print_date', 'publish_type','puzzle_id', 'title', 'version', 'percent_filled', 'solved', 'star'])
    
    a = "https://www.nytimes.com/svc/crosswords/v3//puzzles.json?publish_type=" + puzzle_type + "&sort_order=asc&sort_by=print_date&date_start="
    i = 0
    while (i + 2) <= len(first_days):
        start_year = first_days[i][0]
        start_month = first_days[i][1]
        start_day = first_days[i][2]

        end_year = first_days[i + 1][0]
        end_month = first_days[i + 1][1]
        end_day = first_days[i + 1][2]

        url = f'{a}{start_year}-{start_month}-{start_day}&date_end={end_year}-{end_month}-{end_day}'
        data = json.loads(get_data(url = url, cookies = cookies))["results"]
        metadata = pd.concat((metadata, pd.DataFrame(data)))

        i += 1
    
    today_date = datetime.now().date()
    today_date = str(today_date).split("-")

    start_year = first_days[-1][0]
    start_month = first_days[-1][1]
    start_day = first_days[-1][2]

    end_year = today_date[0]
    end_month = today_date[1]
    end_day = today_date[2]

    url = f'{a}{start_year}-{start_month}-{start_day}&date_end={end_year}-{end_month}-{end_day}'
    data = json.loads(get_data(url = url, cookies = cookies))["results"]
    metadata = pd.concat((metadata, pd.DataFrame(data)))
    

    my_stats = {}
    for id in tqdm(metadata["puzzle_id"]):
        url = "https://www.nytimes.com/svc/crosswords/v6/game/" + str(id) + ".json"
        my_stats[str(id)] = json.loads(get_data(url, cookies))["calcs"]
    metadata_dedup = metadata.drop_duplicates()
    metadata_dedup = metadata_dedup.reset_index(drop = True).astype("string")

    return my_stats, metadata_dedup


def create_stats_frame(my_stats):
    stats_frame = pd.DataFrame(my_stats)
    stats_frame = stats_frame.T.reset_index()
    stats_frame = stats_frame[["index", "secondsSpentSolving"]].astype({"index": 'string', "secondsSpentSolving": float})
    stats_frame.columns = ["puzzle_id", "seconds_spent_solving"]
    return stats_frame


def merge_frames(stats_frame, metadata):
    crosswords = pd.merge(stats_frame, metadata, how = "outer", on = "puzzle_id")
    return crosswords


def add_days(crosswords):
    days_of_week = {"0": "Monday",
                    "1": "Tuesday",
                    "2": "Wednesday",
                    "3": "Thursday",
                    "4": "Friday",
                    "5": "Saturday",
                    "6": "Sunday"}

    for i in range(len(crosswords)):
        print_date_list = crosswords.loc[i,"print_date"].split("-")
        crosswords.loc[i, "day"] = days_of_week[str(datetime(int(print_date_list[0]), int(print_date_list[1]), int(print_date_list[2])).weekday())]

    return crosswords
    

def save_crosswords(crosswords, puzzle_type, start_date):    
    crosswords.to_csv(f'data/{puzzle_type}_{"".join(start_date.split("-"))}_{str(datetime.now().date())}.csv', index = False)


def get_all_data():
    my_cookie = input("Enter your cookie:")
    cookies = {"NYT-S": my_cookie}
    puzzle_type = input("Enter puzzle type: ")
    start_date = input("What is the start date for the data you want to retrieve? Use the format 'YYYY-MM-DD': ")
    print("Retrieving puzzle IDs...")
    my_stats, metadata = retrieve_data(puzzle_type, start_date, cookies)
    print("Getting your stats...")
    stats_frame = create_stats_frame(my_stats)
    print("Merging stats with metadata...")
    crosswords = merge_frames(stats_frame, metadata)
    crosswords = add_days(crosswords)
    save_crosswords(crosswords, puzzle_type, start_date)
    print("Crossword stats saved!")

def main():
    get_all_data()

if __name__ == "__main__":
    get_all_data()