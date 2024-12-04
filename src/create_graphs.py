import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.data_prep import *

week_xlabels = ["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]

def create_hist(day: str, ax: plt.Axes) -> None:
    '''Draws daily histogram graph.'''
    day_frame = get_day_frame(day)

    ax.hist((day_frame["seconds_spent_solving"]/60), bins = 20, color = "lightgrey") 

    ax.set_title(f'{day} Crossword Solve Times', fontdict={"size":"xx-large"})
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Count')

    ave_time = np.mean(day_frame["seconds_spent_solving"])
    best_time = np.min(day_frame["seconds_spent_solving"])
    recent_time = day_frame.iloc[-1, 0]

    ax.axvline(ave_time/60, color='dodgerblue', linestyle='--', linewidth=2, label=f'Average: {int(ave_time//60)}:{(str(round(ave_time%60))).zfill(2)}')
    ax.axvline(best_time/60, color='gold', linestyle='--', linewidth=2, label=f'Best: {int(best_time//60)}:{(str(round(best_time%60))).zfill(2)}')
    ax.axvline(recent_time/60, color = 'deeppink', linestyle='--', linewidth=2, label=f'Most Recent: {int(recent_time//60)}:{(str(round(recent_time%60))).zfill(2)}')
    
    ax.legend(loc='upper right', fontsize='x-large')

def create_compare_ave_times() -> None:
    '''Draws average time by day bar chart.'''
    all_days = prep_bar_chart_all_days()
    all_days_min = all_days/60

    for i in range(len(all_days)):
        if all_days[i] == 0:
            all_days[i] = ""
            
    plt.figure(figsize=(8, 6))

    plt.bar(all_days_min.index, all_days_min.values, color = "dodgerblue")
    plt.title("Average Crossword Times by Day", fontdict= {"size":"xx-large"})

    plt.xticks(range(0,7),week_xlabels, fontsize = 14)

    plt.yticks(range(0, round(max(all_days_min)) + 10,5),  fontsize = 14)
    plt.ylabel("Average Time (in Minutes)", fontdict= {"size":"x-large"})

    for i in range(len(all_days)):
        try:
            plt.text(i - .35, 
                    all_days_min.values[i] + .75,
                    f'{round(all_days.values[i]//60)}:{str(round(all_days.values[i]%60)).zfill(2)}',
                    fontdict= {"size":"x-large"})
        except Exception as e:
            plt.text(i - .35, 
                    all_days_min.values[i] + .75,
                    f'',
                    fontdict= {"size":"x-large"})

def create_mini_hist_box(num_days: int, ax: plt.Axes, ax_box: plt.Axes) -> None:
    '''Draws histogram/boxplot graph for mini crosswords.'''
    mini_hist_box_data = prep_mini_hist_box(num_days)

    ax.hist(mini_hist_box_data, bins=30, color='gold', edgecolor='black')

    ax_box.boxplot(mini_hist_box_data, vert=False, widths=0.1, patch_artist=True,
                boxprops=dict(facecolor='dodgerblue', color='black'),
                medianprops=dict(color='black'), 
                flierprops={"markerfacecolor":'deeppink', 
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
        
    ax.set_xticks(range(0, round(labels[4]), 20))
    ax.set_xticklabels([f'{num}s' for num in range(0, round(labels[4]),20)])
    ax.set_title(f"Last {num_days} Mini Puzzles (Excluding Saturdays)", fontdict={"size":"xx-large"})