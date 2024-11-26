import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.data_prep_plot import *

week_xlabels = ["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]

# Graphs for daily CW
def create_hist(day: str):

    day_frame = get_day_frame(day)

    plt.figure(figsize=(8, 6))
    plt.hist((day_frame["seconds_spent_solving"]/60), bins = 20, color = "lightgrey") 

    plt.title(f'{day} Crossword Solve Times', fontdict={"size":"xx-large"})
    plt.xlabel('Time (minutes)')
    plt.ylabel('Count')

    ave_time = np.mean(day_frame["seconds_spent_solving"])
    best_time = np.min(day_frame["seconds_spent_solving"])
    recent_time = day_frame.iloc[-1, 0]

    plt.axvline(ave_time/60, color='dodgerblue', linestyle='--', linewidth=2, label=f'Average: {int(ave_time//60)}:{(str(round(ave_time%60))).zfill(2)}')
    plt.axvline(best_time/60, color='gold', linestyle='--', linewidth=2, label=f'Best: {int(best_time//60)}:{(str(round(best_time%60))).zfill(2)}')
    plt.axvline(recent_time/60, color = 'deeppink', linestyle='--', linewidth=2, label=f'Most Recent: {int(recent_time//60)}:{(str(round(recent_time%60))).zfill(2)}')
    
    plt.legend(loc='upper right', fontsize='x-large')

def create_compare_ave_times():
    all_days = prep_bar_chart_all_days()
    all_days_min = all_days/60

    plt.figure(figsize=(8, 6))

    plt.bar(all_days_min.index, all_days_min.values, color = "dodgerblue")
    plt.title("Average Crossword Times by Day", fontdict= {"size":"xx-large"})

    plt.xticks(range(0,7),week_xlabels, fontsize = 14)

    plt.yticks(range(0, round(max(all_days_min)) + 10,5),  fontsize = 14)
    plt.ylabel("Average Time (in Minutes)", fontdict= {"size":"x-large"})

    for i in range(len(all_days)):
        plt.text(i - .35, 
                all_days_min.values[i] + .75,
                f'{round(all_days.values[i]//60)}:{str(round(all_days.values[i]%60)).zfill(2)}',
                fontdict= {"size":"x-large"})

def create_mini_hist_box(num_days:int = 100):
    mini_hist_box_data = prep_mini_hist_box(num_days)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(mini_hist_box_data, bins=30, color='gold', edgecolor='black')

    ax_box = ax.twinx()
    ax_box.boxplot(mini_hist_box_data, vert=False, widths=0.1, patch_artist=True,
                boxprops=dict(facecolor='dodgerblue', color='black'),
                medianprops=dict(color='black'), 
                flierprops={"markerfacecolor":'red', 
                            "marker":"o"})
    ax_box.set_yticks([])

    labels = [np.min(mini_hist_box_data)] + list(np.percentile(mini_hist_box_data, [25, 50, 75])) + [np.max(mini_hist_box_data)]

    for i in range(len(labels)):
        ax_box.text(labels[i] - 2 , 1.07, f'{round(labels[i])}s', 
                    fontdict={"style":"normal", 
                            "size":"medium"},
                            fontweight = "bold",
                            bbox={"facecolor":"white", 
                                    "boxstyle":'round,pad=0.25'})

    plt.xticks(range(0, round(labels[4]),20), labels = [f'{num}s' for num in range(0, round(labels[4]),20)])
