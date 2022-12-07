import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# Done
def load_df() -> pd.DataFrame:
    # Load Weather JSON into DataFrame
    df = pd.read_json("bbc_weather_cb25.json")
    # Reflect DataFrame by writing rows as columns and vice versa
    df = df.transpose()
    # Remove rows containing any missing values
    df = df.dropna(axis=0)
    return df


# Done
def template_creation(df: pd.DataFrame, analysis_date: str) -> tuple[dict, list[str]]:
    # Target row in DataFrame that matches the intended date
    one_date = df.loc[[analysis_date]]

    # Create "Single Date" Dictionary with empty lists for each hour
    per_hour_dict = {analysis_date: {
        "06": [], "07": [], "08": [], "09": [], "10": [], "11": [], "12": [], "13": [], "14": [], "15": [], "16": [],
        "17": [], "18": [], "19": [], "20": [], "21": [], "22": [], "23": [], "00": [], "01": [], "02": [], "03": [],
        "04": [], "05": []
    }
    }

    # Ordered hour sequence for data values to be paired with
    hour_sequence = ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
                     "22", "23", "00", "01", "02", "03", "04", "05"]

    # Loop each column (days) and build structure
    for day in range(len(df.columns)):
        a_date = pd.DataFrame(
            {"hour": one_date[day + 1].values[0].keys(), "speed": one_date[day + 1].values[0].values()})
        speed = a_date.speed.values.tolist()
        for index, hour in enumerate(per_hour_dict[analysis_date].keys()):
            per_hour_dict[analysis_date][hour].append(speed[index])

    return per_hour_dict, hour_sequence


# Done
def template_creation_multi_date(df: pd.DataFrame, analysis_date: str, num_days: int) -> list:
    # Get index of provided analysis date (forms the start of the range)
    starting_index = df.index.get_loc(analysis_date)

    # Select range containing start date plus specified number of subsequent dates
    full_dates = df.axes[0].tolist()[starting_index:starting_index + num_days]

    # Empty list to add each single date dict in to
    month_list = []

    # Loop each date and append to month list
    for a_date in full_dates:
        over_time_item, hour_sequence = template_creation(df, a_date)
        month_list.append(over_time_item)

    return month_list


# Done
def single_day_line_graphs(hours_list: list[str], time_dict: dict, analysis_date: str):
    # Create subplots and adjust space
    fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
    plt.subplots_adjust(hspace=1)

    # Iterate through each hour and subplot
    for hour_sing, ax in zip(hours_list, axs.ravel()):
        # Gather x and y values
        x_values = range(len(time_dict[analysis_date][hour_sing]))
        y_values = time_dict[analysis_date][hour_sing]

        # Calculate polynomial for trend line
        z = np.polyfit(x_values, y_values, 1)
        poly = np.poly1d(z)

        # Plot Graph and set Labels
        ax.plot(x_values, y_values, marker="o")  # Plot main x/y data
        ax.invert_xaxis()  # Change order of data on x_axis
        ax.set_title(hour_sing)  # Title each subplot with the hour
        ax.set_xticks(x_values)  # Set x ticks to equal the x values (to be labelled below)
        ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])
        ax.grid(visible=True)  # Enable grid
        ax.set_yticks(range(3, 13))  # Hard coded y_ticks so graphs can be compared
        ax.set(xlabel='Days from date', ylabel='Wind speed (mph)')  # Add axis labels to each subplot
        ax.plot(x_values, poly(x_values), "r--")  # Plot trend line

    # Add main title and show graph
    fig.suptitle(f"Trends in Wind Forecast Speed (hourly)\n{analysis_date}\nCB25 0 Area", va="baseline", fontsize="30",
                 y=0.9)
    plt.show()


# Done
def line_graph(time_dict: dict, analysis_date: str, hour_sequence: list[str]):
    # Create empty lists for upcoming values to be appended to
    final_speed = []
    lower_bound = []
    upper_bound = []

    # Iterate each hour in time dictionary, then calculate and append the final, min and max speeds for the given hour
    for hour in time_dict[analysis_date]:
        final_speed.append(time_dict[analysis_date][hour][-1])
        lower_bound.append(min((time_dict[analysis_date][hour])))
        upper_bound.append(max((time_dict[analysis_date][hour])))

    # Create and plot data
    plt.figure(figsize=(15, 5))
    plt.plot(hour_sequence, final_speed)

    # Add shaded area
    plt.fill_between(hour_sequence, lower_bound, upper_bound, alpha=0.2)

    # Labels
    plt.suptitle("Wind Speed for {}\nCB25 0".format(analysis_date))
    plt.legend(["Wind Speed T-minus 1 Day", "Variance Min/Max"])

    plt.show(aspect="auto")


# Done
def scatter_graph(hours_list: list[str], multi_date_dict: list):
    # Create subplots
    fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
    plt.subplots_adjust(hspace=1)

    # Iterate through hours/subplots
    for hour_sing, ax in zip(hours_list, axs.ravel()):
        # Iterate through each date (plotting once for every date on each subplot)
        for date in multi_date_dict:

            # Unpack each hour iterable
            entire_hours = [*date.values()]

            # Extract end speed
            end_speed = entire_hours[0][hour_sing][-1]

            # Calculate and store difference to end speed
            speed_diff = []
            for each in entire_hours[0][hour_sing]:
                speed_diff.append(end_speed - each)

            # Set x and y
            x_values = range(len(entire_hours[0][hour_sing]))
            y_values = speed_diff

            # Plot Graph
            ax.scatter(x_values, y_values, 10)

        # Set 0 Line
        ax.axhline(0)

        # Set Ticks
        ax.set_yticks(np.arange(-10, 10, 1))
        ax.set_yticklabels([])
        ax.set_xticks(range(13))
        ax.set_xticklabels(["13", "12", "11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])

        # Set Labels and show grid
        ax.set_title(hour_sing)
        ax.set(xlabel='Days from date', ylabel='+/- Deviation')
        ax.grid(visible=True)

    # Add main figure title
    fig.suptitle(f"Trends in Wind Forecast Speed (hourly)\nMulti Day View\nCB25 0 Area", va="baseline", fontsize="30",
                 y=0.9)

    plt.show()


def histo_chart(hours_list: list[str], multi_date_dict: list, start_date: str):
    # Empty list to store each date's average variance
    avg_of_dates = []

    # Iterate through each date
    for date in multi_date_dict:

        # Unpack each hour iterable
        entire_hours = [*date.values()]

        # Empty list for each hour's average
        day_hour_avg = []

        # Loop each hour
        for hour in hours_list:
            # Calculate difference to end speed
            end_speed = entire_hours[0][hour][-1]

            # Empty list to store each hour's difference to end speed
            speed_diff = []
            for each in entire_hours[0][hour]:
                speed_diff.append(end_speed - each)

            # Average the variance for the given hour
            hour_avg = sum(speed_diff) / len(speed_diff)
            day_hour_avg.append(hour_avg)

        # Average of all hours and store resulting date's average
        date_avg = sum(day_hour_avg) / len(day_hour_avg)
        avg_of_dates.append(date_avg)

    # Histogram
    # Create figure
    plt.figure(figsize=(15, 15))

    # Plot histogram with symmetrical bins
    plt.hist(avg_of_dates, bins=np.arange(-4, 5, step=1))

    # Set x ticks and labels
    plt.xticks(np.arange(-4, 4.5, step=1))
    plt.xlabel(
        "Average Wind Speed Variation +/– mph\nAbove 0 - Date was over-predicted\nBelow 0 - Date was under-predicted",
        fontsize=20)
    plt.ylabel("Number of dates", fontsize=20)
    plt.suptitle(f"Average Wind Speed Variation - {start_date} + {len(multi_date_dict)} Days\nCB25 0 Area",
                 va="baseline", fontsize="30",
                 y=0.9)

    # Set divider line at 0
    plt.axvline(0, linewidth=3, color="red", linestyle="dashed")
    plt.grid(visible=True)

    plt.show()


def multi_histo_chart(hours_list: list[str], multi_date_dict: list):
    # Create subplots
    fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
    plt.subplots_adjust(hspace=1)

    # Iterate through hours/subplots
    for hour_sing, ax in zip(hours_list, axs.ravel()):
        avg_of_dates = []

        # Iterate through each date (plotting once for every date on each subplot)
        for date in multi_date_dict:

            # Unpack each hour iterable
            entire_hours = [*date.values()]

            # Empty list for each hour's average
            day_hour_avg = []

            # Loop each hour
            for hour in hours_list:
                # Calculate difference to end speed
                end_speed = entire_hours[0][hour][-1]

                # Empty list to store each hour's difference to end speed
                speed_diff = []
                for each in entire_hours[0][hour]:
                    speed_diff.append(end_speed - each)

                # Average the variance for the given hour
                hour_avg = sum(speed_diff) / len(speed_diff)
                day_hour_avg.append(hour_avg)

            # Average of all hours and store resulting date's average
            date_avg = sum(day_hour_avg) / len(day_hour_avg)
            avg_of_dates.append(date_avg)

        # Histogram
        # Plot histogram with symmetrical bins
        ax.hist(avg_of_dates, bins=np.arange(-4, 5, step=1))

        # Set x ticks and labels
        ax.set_xticks(np.arange(-4, 4.5, step=1))
        ax.set(
            xlabel="Average Wind Speed Variation +/– mph",
            ylabel="Number of dates"
            )

        # Line of symmetry & grid
        ax.axvline(0, linewidth=3, color="red", linestyle="dashed")
        ax.grid(visible=True)

    # Add main figure title
    fig.suptitle(f"Trends in Wind Forecast Speed (hourly)\nCB25 0 Area\nAbove 0 - Date was over-predicted\nBelow 0 - Date was under-predicted", va="baseline", fontsize="30",
                 y=0.9)

    plt.show()


# Set date to analyse here:
date_to_analyse = '2022-07-29'
wind_df = load_df()

# Creating Assets
over_time, hours = template_creation(wind_df, date_to_analyse)
multi_day = template_creation_multi_date(wind_df, date_to_analyse, 100)

# Creating Graphs
# line_graph(over_time, date_to_analyse, hours)
# single_day_line_graphs(hours, over_time, date_to_analyse)
# scatter_graph(hours, multi_day)
# histo_chart(hours, multi_day, date_to_analyse)
multi_histo_chart(hours, multi_day)
