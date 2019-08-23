# Scripts for Insight Data Engineering coding challenge
This GitHub repository contains my solution to the [coding challenge](https://github.com/InsightDataScience/border-crossing-analysis) for the [Insight Data Engineering Fellows Program](https://www.insightdataengineering.com/).

Given a comma separated input file with 8 columns, e.g.,

```
iPort Name,State,Port Code,Border,Date,Measure,Value,Location
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,POINT (-72.09944 45.005)
Norton,Vermont,211,US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,POINT (-71.79528000000002 45.01)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,POINT (-115.49806000000001 32.67889)
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Frontier,Washington,3020,US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,POINT (-117.78134000000001 48.910160000000005)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
Eagle Pass,Texas,2303,US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)
```
the script generates a comma separated output file with sum of total number of crossings (`Value`) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used and the running monthly average of total crossings, rounded to the nearest whole number, for that combination of `Border` and `Measure`, or means of crossing.For example, the output will be the following for the above file.
```
Border,Date,Measure,Value,Average
US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0
```
## Assumptions

* The time is assumed to be 12:00:00 AM on all the dates, i.e if the border crossing is recorded at two different times on the same day, then they are not treated as same dates.

* The format of the time stamp is assumed to be remained same throught the data. If the format is changed, the program will skip that row.

* Even if these are some missing values in the csv file, it is assumed that those missing values will be in the form of empty strings.

* The values in each line are expected to be in the same order.

## Different functions in the code

### round_fun:

The default rounding function was rounding the number 114486.5 to 114486. But, we want the function to round it to 114487. This function will take care of that.

Input: Any real number

Output: Nearest integer to the input real number

### type_check:

I used int as a placeholder for the average value in the code. If it remains as int by the end of calculations, then I'm replacing it with 0. This function will check the type of the element at that index and if it is not an integer, it will replace it with zero.

Input: Any datatype

Output: If the input is integer, it will return the same integer, otherwise, it will return zero.

### is_date:

Is date is used to check whether the time stamp is according to the format or not.

Input: Any string

Output: 

### is_int:

Is_int is used to check whether the Value is an integer or not.

## Summary
The `border_analytics.py` script reads the input file line by line and creates two dictionaries `Dic` (i.e, `{drug_name:total_cost, }`) to keep track of drug costs and `doctor_names` (i.e., `{drug_name:unique_doctor_names}`) to keep track of unique doctor names for each drug. Consequently, the dictionary `drug_cost` is sorted by the value (and key if there is a tie) and written in the desired comma separated output format. 

## Instructions
To execute the script move to the main directory of the project and run the following in the terminal:

```
python ./src/border_analytics.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv
```

Alternatively, you can execute `./run.sh` script to run the codes for a sample file and perform a unit test.
