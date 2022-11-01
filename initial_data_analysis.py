import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_json("bbc_weather_cb25.json")
df = df.transpose()
df = df.dropna(axis=0)
# print(df)

one_date = df.iloc[[0]]


# Analyse a single date
# Eventually repeat for all dates to build more data points for comparison
over_time = {"2022-07-29": {
    "06": [], "07": [], "08": [], "09": [], "10": [], "11": [], "12": [], "13": [], "14": [], "15": [], "16": [], "17": [], "18": [], "19": [], "20": [], "21": [], "22": [], "23": [], "00": [], "01": [], "02": [], "03": [], "04": [], "05": []
    }
}
hour_sequence = ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "00", "01", "02", "03", "04", "05"]

for day in range(len(df.columns)):
    a_date = pd.DataFrame({"hour": one_date[day + 1].values[0].keys(), "speed": one_date[day + 1].values[0].values()})
    speed = a_date.speed.values.tolist()
    # print("Day: {}".format(day))
    # for count, speeds in enumerate(speed):
    #     print("Speed: {}".format(count))
    #     # print(speed[count])

    for index, hour in enumerate(over_time["2022-07-29"].keys()):
        over_time["2022-07-29"][hour].append(speed[index])


# print(over_time)


fig, axs = plt.subplots(nrows=8, ncols=3, figsize=(20, 20))
plt.subplots_adjust(hspace=1)
for hour_sing, ax in zip(hour_sequence, axs.ravel()):
    x_values = range(len(over_time["2022-07-29"][hour_sing]))
    y_values = over_time["2022-07-29"][hour_sing]

    # Calculate polynomial for trend line https://stackoverflow.com/questions/61011711/add-trendline-for-timeseries-graph-in-python
    z = np.polyfit(x_values, y_values, 1)
    p = np.poly1d(z)

    ax.plot(x_values, y_values, marker="o")
    ax.invert_xaxis()
    ax.set_title(hour_sing)
    ax.set_xticks(x_values)
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])
    ax.grid(visible=True)
    ax.set_yticks(range(3, 13))
    plt.xlabel("Days from date")
    plt.ylabel("Wind speed (mph)")

    ax.plot(x_values, p(x_values), "r--")

# ax06 = plt.subplot(1, 1, 1)
# plt.title("6AM")
# x_values = range(len(over_time["2022-07-29"]["06"]))
# plt.plot(x_values, over_time["2022-07-29"]["06"], marker="o")
# ax06.invert_xaxis()
# plt.xlabel("Days from date")
# plt.ylabel("Wind Speed (mph)")
# ax06.set_xticks(x_values)
# ax06.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"])


plt.show(aspect="auto")
plt.savefig("2022-07-29.png")
# line graph with hue as upper/lower bounds

