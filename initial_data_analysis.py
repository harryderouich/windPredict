import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def load_df():
    # Load Weather JSON into DataFrame
    df = pd.read_json("bbc_weather_cb25.json")
    df = df.transpose()
    df = df.dropna(axis=0)
    print("Type")
    print(type(df))
    return df


def template_creation(df, analysis_date):
    one_date = df.loc[[analysis_date]]

    # Create "Single Date" Dictionary with lists for each hour
    over_time = {analysis_date: {
        "06": [], "07": [], "08": [], "09": [], "10": [], "11": [], "12": [], "13": [], "14": [], "15": [], "16": [], "17": [], "18": [], "19": [], "20": [], "21": [], "22": [], "23": [], "00": [], "01": [], "02": [], "03": [], "04": [], "05": []
        }
    }

    # Hour sequence for data values to be paired with
    hour_sequence = ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00", "01", "02", "03", "04", "05"]

    for day in range(len(df.columns)):
        a_date = pd.DataFrame({"hour": one_date[day + 1].values[0].keys(), "speed": one_date[day + 1].values[0].values()})
        speed = a_date.speed.values.tolist()

        for index, hour in enumerate(over_time[analysis_date].keys()):
            over_time[analysis_date][hour].append(speed[index])

    return over_time, hour_sequence


def template_creation_multi_date(df, analysis_date, num_days):
    starting_index = df.index.get_loc(analysis_date)
    full_dates = df.axes[0].tolist()[starting_index:starting_index+num_days]
    month_object = []
    for a_date in full_dates:
        over_time_item, hour_sequence = template_creation(df, a_date)
        month_object.append(over_time_item)
    return month_object


def single_day_line_graphs(hours_list, time_dict, analysis_date):
    fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
    plt.subplots_adjust(hspace=1)
    for hour_sing, ax in zip(hours_list, axs.ravel()):
        x_values = range(len(time_dict[analysis_date][hour_sing]))
        y_values = time_dict[analysis_date][hour_sing]

        # Calculate polynomial for trend line
        z = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(z)

        # Plot Graph and set Labels etc.
        ax.plot(x_values, y_values, marker="o")
        ax.invert_xaxis()
        ax.set_title(hour_sing)
        ax.set_xticks(x_values)
        ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])
        ax.grid(visible=True)
        ax.set_yticks(range(3, 13))
        ax.set(xlabel='Days from date', ylabel='Wind speed (mph)')
        ax.plot(x_values, p(x_values), "r--")

    fig.suptitle(f"Trends in Wind Forecast Speed (hourly)\n{analysis_date}\nCB25 0 Area", va="baseline", fontsize="30", y=0.9)
    plt.show()


def line_graph(time_dict, analysis_date, hour_sequence):
    final_speed = []
    lower_bound = []
    upper_bound = []

    for hour in time_dict[analysis_date]:
        # print(time_dict[analysis_date][hour])
        final_speed.append(time_dict[analysis_date][hour][-1])
        lower_bound.append(min((time_dict[analysis_date][hour])))
        upper_bound.append(max((time_dict[analysis_date][hour])))

    plt.figure(figsize=(15, 5))
    plt.plot(hour_sequence, final_speed)

    plt.fill_between(hour_sequence, lower_bound, upper_bound, alpha=0.2)

    # Labels
    plt.suptitle("Wind Speed for {}\nCB25 0".format(analysis_date))
    plt.legend(["Wind Speed T-minus 1 Day", "Variance Min/Max"])

    plt.show(aspect="auto")


def scatter_graph(hours_list, multi_day_dict):
    fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
    plt.subplots_adjust(hspace=1)

    for hour_sing, ax in zip(hours_list, axs.ravel()):
        for day in multi_day_dict:
            entire_hours = [*day.values()]
            print(entire_hours)
            # Calculate difference to end speed
            end_speed = entire_hours[0][hour_sing][-1]
            speed_diff = []
            for each in entire_hours[0][hour_sing]:
                speed_diff.append(end_speed - each)
            x_values = range(len(entire_hours[0][hour_sing]))
            y_values = speed_diff

            # Plot Graph
            ax.scatter(x_values, y_values, 10)

        # Set 0 Line
        ax.axhline(0)

        # Set Ticks
        ax.set_yticks(range(-5, 5))
        # ax.set_xticks(x_values)
        # ax.set_xticklabels(["13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])

        # Set Labels
        ax.set_title(hour_sing)
        ax.set(xlabel='Days from date', ylabel='Wind speed (mph)')

        ax.grid(visible=True)

    fig.suptitle(f"Trends in Wind Forecast Speed (hourly)\nMulti Day View\nCB25 0 Area", va="baseline", fontsize="30",
                 y=0.9)

    plt.show()


# Set date to analyse here:
date = "2022-08-19"
wind_df = load_df()

over_time, hours = template_creation(wind_df, date)
multi_day = template_creation_multi_date(wind_df, date, 30)

# Graphs
# line_graph(over_time, date, hours)
# single_day_line_graphs(hours, over_time, date)
scatter_graph(hours, multi_day)

