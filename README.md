# Group 5: Examination of Health Data Breaches Study

### Ivory Chorng, Noel Thomas

We looked at a study on data breaches in the United States [[Link]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4272442/) and 
wanted to improve it. The author’s data was acquired from the U.S. Department of Health and Human Service, Office for 
Civil Rights [[Link]](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf). The page includes 
breaches reported within the last 24 months (when the study was done, which is 2013) that are currently under 
investigation by the Office for Civil Rights.

We plan to improve the work done in this study and look at aspects of data breaches that they couldn't. Some of our 
ideas include: using the date of breach to understand trends in data breaches and aggregating by more than one level
(state, location and type of breach) to understand more about the nature of data breaches in this country.

We have two hypotheses that we want to verify:

**Hypothesis 1**: Data breaches increase during the holiday season.

**Hypothesis 2**: States with higher population have more data breaches.


First, replicating the study. To do this, we had to first process the dataframe. The first two functions, read_file() 
and adjust_time_limits() help us read in the data and slice it to retrieve the data from the desired timeframe 
respectively.

Then we have three functions that help us with the processing of the dataframe. cleanup() removes columns 
with null values. It first shows us the percentage of null values in each column, so we can make a decision to not 
remove a column if it has a large percentage of null values, since it may skew the analysis. This function then calls 
the other two functions in question: fix_columns() and change_to_binary(). The former works on two specific columns 
with overlapping unique values in each cell and creates a new column containing one of those unique values in each 
cell. It is used to 'fix' the 'Types of Breach' and 'Location of Breached Information' columns this way. The latter is 
also meant to work on two specific columns: 'Business Associate Present' and 'Covered Entities Involved'. Both these 
columns are used in the study, however they contain string values. This function essentially converts these string 
values to binary. 'Business Associate Present' contains 'Yes' and 'No', and so these are overwritten as 1s and 0s, and 
'Covered Entities Involved' contains the type of covered entity involved, so a new column is created with a 1 if a 
covered entity exists for the data breach or a 0 if it doesn't.


