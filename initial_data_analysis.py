import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Load Weather JSON into DataFrame
df = pd.read_json("bbc_weather_cb25.json")
df = df.transpose()
df = df.dropna(axis=0)

# Set date to analyse here:
analysis_date = "2022-08-14"
one_date = df.loc[analysis_date]
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


fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
plt.subplots_adjust(hspace=1)
for hour_sing, ax in zip(hour_sequence, axs.ravel()):
    x_values = range(len(over_time[analysis_date][hour_sing]))
    y_values = over_time[analysis_date][hour_sing]

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


plt.show(aspect="auto")
fig.savefig(f"{analysis_date}.png")
# line graph with hue as upper/lower bounds

