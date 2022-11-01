import json

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta


def get_html(url):
    query = requests.get(url)
    html_object = BeautifulSoup(query.content, 'html.parser')
    return html_object


def save_html(page_object):  # Saves HTML to local storage
    with open("bbc_weather_cb25_day4.html", "w", encoding="utf-8") as file_to_write:
        file_to_write.write(page_object.prettify())


def open_html(file_path):
    with open(file_path, encoding="utf-8") as local_file:
        html_file_object = BeautifulSoup(local_file, 'html.parser')
    return html_file_object


def parse_html(page, date, distance_from_date):
    date_label = str(date)
    # Create Hour By Hour Object
    hour_by_hour = page.find(class_="wr-time-slot-list__time-slots")
    time_slots = hour_by_hour.find_all(class_="wr-js-time-slot")
    wind_dictionary_day = {}
    for time_slot in time_slots:
        time_string = time_slot.find(class_="wr-time-slot-primary__time").get_text().strip()[:2]
        wind_speed_mph = time_slot.find(class_="wr-value--windspeed--mph").get_text().split()[0]
        wind_dictionary_day[time_string] = int(wind_speed_mph)
        # print("Time: {}:00 / {}mph".format(time_string, wind_speed_mph))
    print(wind_dictionary_day)
    return wind_dictionary_day


def ordinal(n):
    return str(n)+("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def each_page(base_url):
    with open("bbc_weather_cb25.json") as existing_data:
        wind_dictionary_all_days = json.load(existing_data)
    today = datetime.now()
    # print(today.date())
    list_of_links = []
    for count in range(13):
        list_of_links.append(base_url + "day{}".format(count+1))
    # print(list_of_links)
    for day_diff, link in enumerate(list_of_links):
        this_datetime = today + timedelta(days=(day_diff + 1))
        this_date = this_datetime.date()
        # print(str(day_diff + 1), this_date, link)
        html_file = get_html(link)
        wind_dictionary_single_day = parse_html(html_file, this_date, day_diff+1)
        try:
            wind_dictionary_all_days[str(this_date)][day_diff+1] = wind_dictionary_single_day
        except KeyError:
            wind_dictionary_all_days[str(this_date)] = {}
            wind_dictionary_all_days[str(this_date)][day_diff + 1] = wind_dictionary_single_day

    with open("bbc_weather_cb25.json", "w") as weather_dump:
        json.dump(wind_dictionary_all_days, weather_dump)


# Get and save HTML page to local storage
# html_link = get_html("https://www.bbc.com/weather/cb25/day4")
# save_html(html_link)

# Open local HTML file and make object ready for parsing:
# html_file = open_html("bbc_weather_cb25_day4.html")
# parse_html(html_file)

# IMPORTANT - Can only run 1 time per day
each_page("https://www.bbc.com/weather/cb25/")
