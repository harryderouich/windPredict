# BBC Weather Wind Predictor

## Background
As a keen weekend-warrior-cyclist residing in one of the flattest areas of the UK, I religiously study the weather forecast for the upcoming weekend's wind speed.

My go-to source for this is BBC Weather which allows you to view the hour-by-hour forecast up to 14 days in advance. 

Anecdotally, I sometimes notice a trend that the wind speed can fluctuate by a considerable margin, especially when viewing very far in advance.

I am looking to achieve 2 things with this project:

- Perform a data experiment to confirm or deny my hypothesis.
- Assuming the hypothesis to be true, develop a method to more accurately predict the wind speed (taking the parameters of wind speed (in mph) and how far away the date is (in days))

With possible future improvements including:
- Developing a user-friendly interface that allows users to enter any location and have the modified wind speed returned.
- Bundling the above into a browser extension that operates on top of the BBC Weather website.

## Stage 1: Data Collection
### Planning
The logical first step was to build a web scraping script that could start building a dataset in the background. After the analysis stage I will be looking to create the prediction using some kind of machine learning technique, so the more data I have available for this stage, the better. 

The pieces of data I am collecting are:
- Date of forecast
- Distance from the date (in days)
- Hour of the forecast (BBC Weather runs from 6am to 5am)
- Wind speed (in MPH)

Some possible limitations I have identified so far are:
- The weather forecast is updated multiple times a day, but I believe that capturing each day's data at the same time will negate most of this.
- The wind speed is reported as a whole number, which may lack the detail to spot small deviations or nuances.

My current aim is to capture around 4 weeks of data (with a full 14-day history of how each day is reported) to be able to conclude if there is a significant deviation. My next goal will be to collect at least 3 months of data to feed into my machine learning model. I will continue to collect data until the model is stable.

### Creating the web scraper
I had used Python and the BeautifulSoup library for a few mini projects in the past so knew it would be the smoothest route to creating this. 

The first step was identifying that BBC Weather uses JavaScript to display subsequent days' data. Therefore, it could not be scraped in the usual method of parsing an HTML document after being initialised using the Requests library.

Luckily, each day's pane in the forecast viewer had its own direct link, by appending /day2, /day3 and so on to the URL. This meant I could easily iterate through each page (up til /day13) for the furthest away data.

So, it was just a process of identifying the HTML structure of the forecast pane, which contained a 2 digit string representing the hours (e.g. "06" indicates 06:00am) and buried a bit deeper was the speed itself. I iterate through each of the 13 days available and then the 24 hours available, storing the wind speed for each. A set of nested dictionary made the most sense to transfer in and out of a JSON file so each day's data could be appended. The format for which was:

```
{ 
date(string) : { 
    days_away_from_date(int) : {
        "06" : wind_speed_mph(int), 
         ** Repeat for the 6am - 5am **
    }, 
    ** Repeat for each day until date is reached **
}, 
** Repeat for each new date **
```

For example, the full dataset for a given day looks like:
```
{
"2022-07-23" : {
    13: {
        "06": 5,
        "07": 6,
        "08": 6
        (...and so on)
        }
    12: {
        "06": 6,
        "07": 6,
        "08": 8
        (...and so on)
        }
    11: {
        "06": 4,
        "07": 5,
        "08": 6
        (...and so on)
        }
    (...and so on)
    }
}
```
This will allow later inspection of how the reported wind speed changed during the 2 weeks each date is forecasted.

After running this a few times to verify the code was robust, I took advantage of a QNAP NAS I have that is always on and internet connected. The operating system is Linux based which wasn't something I was experienced with. Also lacking was prior use of SSH and the command line which made it a good challenge. I settled on installing Python3 from the built-in App Store and then using SSH to set up a Python3 environment for my shell. 

To configure the Python3 environment:
```. /etc/profile.d/python3.bash```

To execute the script once:
```python3 /[PATH-TO-FILE]/bbc_weather_scraper.py```

After a few hiccups relating to full file paths, I had this running on demand on the NAS.

To save having to run it myself on a daily basis, I looked into setting up a Cronjob which would run it every day at the same time. To do this on my QNAP NAS:

Open the Crontab using vi: ```vi /etc/config/crontab```

Inserting the following entry to the list of tasks: ```0 8 * * * . /etc/profile.d/python3.bash; python3 /[PATH-TO-FILE]/bbc_weather_scraper.py``` This runs the sets up the Python3 environment and runs the script at 8am every day.

Saving the crontab and restarting the cron service: ```crontab /etc/config/crontab && /etc/init.d/crond.sh restart```

For possible bug fixing I also proactively create a log file when the script runs with the current date and time.

## Stage 2: Data Analysis

My web scraper continues to run and build up data. As of 1st November 2022 I have built up 3 months of full (13-day forecast) data. 

### Single Day and Testing of Hypothesis

The first step was to look at an individual dimension. Take a single date and explore how the wind speed trended, if at all, in the fortnightly forecast.

Choosing an arbitrary date, 30th July 2022, I began work writing `initial_data_analysis.py` to explore my findings. It was my first time using the `numpy`, `pandas` and `matplotlib` libraries in a real world scenario.

The program begins by loading the scraped JSON data into a DataFrame and does some minor cleanup work. 

Then, after the constant of the date to be analysed is set, some structure related elements are built; a dictionary to take the single date's data, and a list of hours for mapping later.

We then iterate through the DataFrame and populate the empty Dictionary template, so it's in a more familiar format to work with.

Next, we start to build our figure and subplots for each hour's trend to be laid out on. During this loop, the `x` and `y` values are plotted, axis labels set and a polynomial calculated for the trend line.

### Results
<img src="https://i.imgur.com/mjOnJw4.png" width="800" alt="graph of wind speed for 2022-07-30, CB25 area"><br />
*Figure 1: Graph of Wind Forecast Speed for 30th July 2022* [Full Size](https://i.imgur.com/mjOnJw4.png)

A conclusion made ever more clear by the trend line is that, universally, the wind speed trended downwards in the time leading up to the chosen date.

To rule out a coincidence, I repeated this for the dates around 1 and 2 weeks ahead of the first date.

<img src="https://i.imgur.com/BPKum5Q.png" width="800" alt="graph of wind speed for 2022-08-07, CB25 area"><br />
*Figure 2: Graph of Wind Forecast Speed for 7th August 2022* [Full Size](https://i.imgur.com/BPKum5Q.png)

<img src="https://i.imgur.com/0ZjuKqF.png" width="800" alt="graph of wind speed for 2022-08-07, CB25 area"><br />
*Figure 3: Graph of Wind Forecast Speed for 14th August 2022* [Full Size](https://i.imgur.com/0ZjuKqF.png)

The same trend appeared. This validated me continuing the investigation. I'd now test for my theory against a larger portion of the dataset, or the entire thing if possible. 

My first intuition was to calculate a numerical representation of the trend line, to either:
- Average out over the whole day to test overall daily variance. For example, to broadly predict how much an entire day's wind speed will likely vary.
- Stored the numerical variance of how each hour trended, essentially averaging out the 13 days of captured speed for a given hour on a single day, to compare average variance for a given hour across the entire data set. For example, to look at how the 6AM wind forecast varies compared to the 6PM wind forecast.

I wasn't sure at this stage what format I'd be needing this value to turn it into a prediction model. Storing absolute values, such as the minimum, maximum or range, or a percentage change over time initially seemed the most intuitive way to look at the trend. But at the same time I was considering something more algebraic to enable a more usable input in calculating the rate of change.

### Multi Day Analysis
To improve the robustness of any future readings I decided to look at analysing a larger portion of the data available, which had now exceeded 100 dates.

I had decided on a set of scatter graphs (one for each hour) similar to the per hour line graphs at the previous stage. Functioning similar to a line graph (visually; allowing for a trend line to indicate a rough "direction"), but allowing me to hopefully spot correlation (i.e. the same pattern) over an array of dates.

I refactored the code in `initial_data_analysis.py` into functions so that I could reuse elements to serve multiple purposes. At the same time ensuring the functions had been type hinted, so I could keep track of their parameters and what they returned.

For instance, the `template_creation()` function came in use when creating all current and future graphs, as well as being used within `template_creation_multi_date()`.

Although at this point there became a need for a comparative value that would allow for evaluation of wind speed _deviation_, not just wind speed. Otherwise, it would result in analysis of the wind speed itself, rather than the accuracy of future forecasts. 

To quickly recap on the data hierarchy, we had:
```angular2html
1. Date (yyyy-mm-dd)
    2. Day from date (13 to 1)
        3. Hour (06 to 05)
            4. Wind speed (integer, mph)
```

For my scatter graph, I had a subplot for each Hour. So we started by iterating over the list of hours (06 to 05) so that each one could be computed and plotted, before moving on to the next one. 

Having then targeted an hour (e.g. 06/6am), we iterated over the `multi_day_dict` to single out one Date (e.g 2022-07-29).

Each hour (06) had an array of 13 values to average out. So we took the speed from day 1, as this was the closest, and therefore most accurate, reading to the actual date, letting it be the `end_speed`. Then for each of the 13 values we calculated the difference to `end_speed`.

For example, if `end_speed` is `10 (mph)` and `Day: 13, Hour: 06` is `8`, the difference stored would be `2`. By plotting each date's difference, for day 13-1, for each hour, we'd hopefully be able to spot a trend.

An initial run of the data with 3 consequent dates was promising. Line at +/- 0 for clarity.

<img src="https://i.imgur.com/aVzYdxh.png" width="800" alt="graph of wind speed for 2022-07-29 + 2 days, CB25 area"><br />
*Figure 4: Graph of Wind Forecast Speed for 29th July 2022 + 2 Days* [Full Size](https://i.imgur.com/0ZjuKqF.png)

Although, when running with more data (100 days), we hit our first hurdle.

<img src="https://i.imgur.com/0i4CLvS.png" width="800" alt="graph of wind speed for 2022-07-29 + 99 days, CB25 area"><br />
*Figure 5: Graph of Wind Forecast Speed for 29th July 2022 + 99 Days* [Full Size](https://i.imgur.com/0i4CLvS.png)

No correlation at all. Which, whilst validating the lack of robustness on the initial model, made our task of finding a conclusion a bit more tricky. The sheer volume of data, both sides of our +/- 0 line made it impossible to visually determine a trend. Potentially paving the way for project to become inconclusive.

### Taking a step back

So it was back to the drawing board. I decided to lean into what was the shortfall of the previous evaluation (volume of data) and play into its strengths: analyse density and frequency.

To avoid getting carried away, I retracted from looking at each hour individually and instead looking at entire days. My thought process being that any slight nuance spotted hour-to-hour could be looked at in a second phase, after we are put on the right tracks by a more broad trend. 

I settled on creating a histogram, due to its ability to show frequency distribution. `histo_chart()` performed similar computations to `scatter_graph()`, with the difference to actual wind speed being calculated, but with averages being taken at the hour, day and date stages. The resulting date average being what summarised the overall distribution for a given day.

For instance, the 6am data points (days 13 to 1) could be `[1, 2, -2, 1...]`, averaging to say, `0.5`. 

Then the average of all hours (06 to 05), e.g. `[0.5, 1, -0.75...]`, could average to say, `0.63`, forming the average for that date.

The resulting array could then be plotted into a histogram, in this case for 100 days. Importing the `scipy` library allowed for plotting of line of best fit. Divider at +/- 0 for clarity.

<img src="https://i.imgur.com/guP9n8L.png" width="800" alt="graph of wind speed for 2022-07-29 + 100 days, CB25 area"><br />
*Figure 6: Graph of Wind Forecast Speed for 29th July 2022 + 100 Days* [Full Size]()

Note, that I took an average of the 100 date averages, which was `0.019`, in other words, each day fluctuated approx. 0.02mph from what was initially predicted vs. what actually happened. Likening to our lack of overall trend or correlation seen before. 

But as shown by the histogram in Figure 6 above, instead looking at the distribution of date averages, we can begin to draw some more conclusions. 

- The modal class can be seen as `0 < x < 1`, indicating that on average, the wind speed is over-predicted on a given day.
- We can also see a wider range for the values <0, extending to as much as -4. This suggests that under-predictions typically a higher margin of error than over-predictions.

As we have now seen that the shape of the data gives us opportunities to spot a pattern, I will look to create a histogram for the average of each hour (06-05). This will perhaps allow me to spot a pattern that a number of hours have in common, or how some hours lead on to other hours. Remembering the purpose of the project, being to analyse wind speed for cycling, a conclusion on a more practical set of hours (e.g. daylight hours) would be an acceptable and successful outcome. 

After the creation of two new histogram related functions, we were presented with the graphs below, grid purposely omitted: 

<img src="https://i.imgur.com/BbEpFaJ.png" width="800" alt="100 day single-hour histogram summary, CB25 area"><br />
*Figure 7: Per-hour histograms summarising 100 days of variance* [Full Size](https://i.imgur.com/BbEpFaJ.png)

I opted against showing a grid, so I could better evaluate the *shape* of the data, as it was the first time looking at data in this dimension and I wanted to be able to make a general conclusion at this stage. I was grateful to see that there was a noticeable difference between at least a few of the hours. This indicated that there would be more to investigate here, but that I had perhaps reached the limit of evaluating just the shape of the data. 

Being that we were now looking for slight nuance in the results, rather than sweeping assumptions, a mathematical representation of the hours and their relationship to one another would likely be required. 

But at the same time, I thought it would be a good idea to wait for more data to be collected, on the chance it made the differences between the hours more drastic (and noticeable visually). 

*To be continued*