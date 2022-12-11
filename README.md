# Examination of Health Data Breaches Study

### Group 5: Ivory Chorng, Noel Thomas

---

We looked at a study on data breaches in the United States [[Link]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4272442/) and 
wanted to improve it. The author’s data was acquired from the U.S. Department of Health and Human Service, Office for 
Civil Rights [[Link]](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf). The page includes 
breaches reported within the last 24 months (when the study was done, which is 2013) that are currently under 
investigation by the Office for Civil Rights.

We plan to improve the work done in this study and look at aspects of data breaches that they couldn't. Some of our 
ideas include: using the date of breach to understand trends in data breaches and aggregating by more than one level
(state, location and type of breach) to understand more about the nature of data breaches in this country.

**Note**: Location of breach is the source of the data breach, for example: laptops, email, etc.

We have three hypotheses that we want to verify:

**Hypothesis 1**: Data breaches increase during the holiday season.

**Hypothesis 2**: Hacking is the most common type of breach and email is the most common location of breach across all 
the states in the US.

**Hypothesis 3**: States with higher population have more data breaches.



First, replicating the study. To do this, we had to first process the dataframe. The first two functions, **read_file()** 
and **adjust_time_limits()** help us read in the data and slice it to retrieve the data from the desired timeframe 
respectively.

Then we have three functions that help us with the processing of the dataframe. __cleanup()__ removes columns 
with null values. It first shows us the percentage of null values in each column, so we can make a decision to not 
remove a column if it has a large percentage of null values, since it may skew the analysis. This function then calls 
the other two functions in question: __fix_columns()__ and __change_to_binary()__. The former works on two specific columns 
with overlapping unique values in each cell and creates a new column containing one of those unique values in each 
cell. It is used to 'fix' the 'Types of Breach' and 'Location of Breached Information' columns this way. The latter is 
also meant to work on two specific columns: 'Business Associate Present' and 'Covered Entities Involved'. Both these 
columns are used in the study, however they contain string values. This function essentially converts these string 
values to binary. 'Business Associate Present' contains 'Yes' and 'No', and so these are overwritten as 1s and 0s, and 
'Covered Entities Involved' contains the type of covered entity involved, so a new column is created with a 1 if a 
covered entity exists for the data breach or a 0 if it doesn't.

We were able to recreate the analysis with the help of the function __analyze_column()__. This contains commands to look at 
the aggregated metrics by certain columns (like the type of breach, or the location of the breach). It also shows us 
the breakdown by percentage, and even plots the percentage values. This function recreates all the tables and 
visualizations from the study.

The next two functions, __plot_seasonal()__ and __check_trends()__ use the date of the data breaches and shows us 
visuals related to it. plot_seasonal() shows us the annual trend of data breaches. This gives us an insight into the 
time of year when we could see a potentially higher number of data breaches. The second function, check_trends() shows 
us the general trend of data breaches since the earliest date available in the dataset (2009).

Looking at the trend of data breaches in the United States, we can see an increase from the first date (October 2009), 
until the start of 2014, and then a sharp decrease until the last available date in the dataset (July 2016):

![alt text](https://github.com/noelthomas28/2022Fall_projects/blob/main/Trend.png "Number of data breaches in the US")


We also used the __analyze_multi_column()__ function to aggregate by more than one category and analyze the results. 
Essentially, this function helps us study the highest contributing type or location of breach in this country for each 
state, and thereby show us which is the most common across all states.


### Hypothesis 1

We expected data breaches to increase during the holiday season, which we subjectively defined as the last six weeks of 
the year, from mid-November to the end of December. When we plotted the count of data breaches each year until the 
latest available date (2016), using the plot_seasonal() function, we found that this really isn't true. They remain 
consistent all year round.

![alt text](https://github.com/noelthomas28/2022Fall_projects/blob/main/Seasonal.png "Count of data breaches each year")

### Hypothesis 2

We looked at the type and location of data breaches for all the states in the country. We expected hacking to be the 
most common type of breach and email the most common location of breach. However, when we looked at the data (until 
the latest date), we found that both assumptions were wrong.

This was the plot for the highest contributing location of breach in the US. We can see that 'Paper' is the highest.

![alt text](https://github.com/noelthomas28/2022Fall_projects/blob/main/Location%20of%20Breach.png "Highest contributing location of breach")


And this was the plot for the highest contributing type of breach in the US. 'Unauthorized Access/Disclosure' is 
the highest.

![alt text](https://github.com/noelthomas28/2022Fall_projects/blob/main/Type%20of%20Breach.png "Highest contributing type of breach")
