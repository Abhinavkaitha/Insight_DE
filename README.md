# Insight Data Engineering coding challenge
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

int is used as a placeholder for the average value in the code. If it remains as int by the end of calculations, then int is replaced with 0. This function will check the type of the element at that index and if it is not an integer, it will replace it with zero.

Input: Any datatype

Output: If the input is integer, it will return the same integer, otherwise, it will return zero.

### is_date:

Is_date is used to check whether the time stamp is according to the format or not.

Input: Any string

Output: If the input time stamp has this '03/01/2019 12:00:00 AM' format, then True, otherwise false.

### is_int:

Is_int is used to check whether the `Value` is an integer or not.

Input: Any string.

Output: If the string is integer, then True, otherwise, False.

### valid:

Checks if there are any missing values in any column and also checks if there are any elements `Value` and `Date` columns with invalid datatype.

Input: complete row in the csv file

Output: If there are any missing values in the required columns (`Border`,`Measure`,`Value`,`Date`) or if the `Date` is not according to the format or if there are values other than integers in the column `Value`, then the output is False.

### read_files: 

This will change the given input file to a nested list. Each line is validated and stored as a list with each column as an element. `cursor` is used to keep track of the number of valid rows and we can limit the maximum number of rows appended into the list with the help of `max_num_rows`.

Input: csv file

Output: Nestes list with structure
```
[['Derby Line',
  'Vermont',
  '209',
  'US-Canada Border',
  '03/01/2019 12:00:00 AM',
  'Truck Containers Full',
  '6483',
  'POINT (-72.09944 45.005)'],
 ['Norton',
  'Vermont',
  '211',
  'US-Canada Border',
  '03/01/2019 12:00:00 AM',
  'Trains',
  '19',
  'POINT (-71.79528000000002 45.01)']]
```

## process_data:

The input of this function is the nested list obtained from the previous function. This is changed to a nested dictionary.
with different borders as keys.
The values are again dictionaries.

   These dictinaries has measure as keys. 
   The values are tuples with two elements. 
   
The first one is a dictionary with time stamp as keys and the second element gives the sum of total crossings for that combination of border and measure. 
The dictionary in the first element of this tuple has values as tuples: the first one is the number of people crossed that border with that measure duirng that time stamp. This will add the crossings across different ports as well 

For example consider
```
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
```

The second element will give us the cumulative average of crossings rounded to the nearest whole number, for that combination of Border and Measure, or means of crossing.

Input: Nested list obtained from read function.

Output: Nested dictionary with structure
```
            {'US-Canada Border': 
                         {'Trains': ({'03/01/2019 12:00:00 AM': (19, int)},
                           19),
                          'Truck Containers Empty': ({'02/01/2019 12:00:00 AM': (1319,
                             int)},
                           1319),
                          'Truck Containers Full': ({'03/01/2019 12:00:00 AM': (6483,
                             int)},
                           6483)}),
             'US-Mexico Border': 
                         {'Pedestrians': ({'01/01/2019 12:00:00 AM': (56810,
                             int),
                            '02/01/2019 12:00:00 AM': (172163, 56810),
                            '03/01/2019 12:00:00 AM': (346158, 114487)},
                           575131)})})
```
## generate_report:

The nested dictionary obtained from the above function is used to create a list of dictionaries with the required parameters in output as keys and the corresponding data as values. This list is sorted based on `Date`, `Value`, `Measure` and `Border`. This list is then written into a csv file. 

Structure of the sorted list of dictionaries:

```
[{'Average': 0,
  'Border': 'US-Canada Border',
  'Date': '03/01/2019 12:00:00 AM',
  'Measure': 'Truck Containers Full',
  'Value': 6483},
 {'Average': 0,
  'Border': 'US-Canada Border',
  'Date': '03/01/2019 12:00:00 AM',
  'Measure': 'Trains',
  'Value': 19},
 {'Average': 114487,
  'Border': 'US-Mexico Border',
  'Date': '03/01/2019 12:00:00 AM',
  'Measure': 'Pedestrians',
  'Value': 346158},
 {'Average': 0,
  'Border': 'US-Canada Border',
  'Date': '02/01/2019 12:00:00 AM',
  'Measure': 'Truck Containers Empty',
  'Value': 1319},
 {'Average': 56810,
  'Border': 'US-Mexico Border',
  'Date': '02/01/2019 12:00:00 AM',
  'Measure': 'Pedestrians',
  'Value': 172163},
 {'Average': 0,
  'Border': 'US-Mexico Border',
  'Date': '01/01/2019 12:00:00 AM',
  'Measure': 'Pedestrians',
  'Value': 56810}]

```

Input: Nested dictionary from data structure function.

Output: csv file.

## Test Cases

### test_1: 
provided by the insight team

### test_2:
If there are any missing values in `Border` or `Measure` or `Value` or `Date`, then the entire row must be skipped. This test case checks this condition.For ex:

```
Norton,Vermont,211,US-Canada Border,,Trains,19,POINT (-71.79528000000002 45.01)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,,15272,POINT (-104.37167 29.56056)

```
Since the `Date` is missing in the first row and `Measure` is missing in the second row, these two rows will be skipped.

### test_3:
If the elements in `Value` or `Date` are not according to the format, then those rows must be skipped. This test case checks this. 

```
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00xyz,Truck Containers Full,6483,POINT (-72.09944 45.005)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346Ft,POINT (-115.49806000000001 32.67889)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,152x,POINT (-104.37167 29.56056)

```
The first row has the wrong `Date` format. The second and third has `Value` in thw wrong format. So, these rows will be skipped.

## Unit Tests

The file unit_tests.py has functions to test the `read files` and `valid` functions.
![Output of Unit tests](https://github.com/Abhinavkaitha/Insight_DE/blob/master/output/unit_test_output.png)

To run the unit_tests file use the command

```
python ./src/unit_tests.py
```

## Summary
The `main.py` script reads the input file line by line and creates a dictionary `report_dict` (i.e, `{'US-Canada Border': 
                         {'Trains': ({'03/01/2019 12:00:00 AM': (19, int)},
                           19),
                          'Truck Containers Empty': ({'02/01/2019 12:00:00 AM': (1319,
                             int)},
                           1319),
                          'Truck Containers Full': ({'03/01/2019 12:00:00 AM': (6483,
                             int)},
                           6483)}),
             'US-Mexico Border': 
                         {'Pedestrians': ({'01/01/2019 12:00:00 AM': (56810,
                             int),
                            '02/01/2019 12:00:00 AM': (172163, 56810),
                            '03/01/2019 12:00:00 AM': (346158, 114487)},
                           575131)})})`) to keep track of the number of crossings in each month and also the running monthly average of total number of crossings for that type of crossing and border. Consequently, the required data is appended into a  list of dictionaries (i.e, `[{'Average': 0,
  'Border': 'US-Canada Border',
  'Date': '03/01/2019 12:00:00 AM',
  'Measure': 'Truck Containers Full',
  'Value': 6483},
 {'Average': 0,
  'Border': 'US-Canada Border',
  'Date': '03/01/2019 12:00:00 AM',
  'Measure': 'Trains',
  'Value': 19}]`)and sorted based on `Border`, `Date`, `Measure` and `Value`. Finally this list is written in the desired comma separated output format. 

## Instructions
To execute the script move to the main directory of the project and run the following in the terminal:

```
python ./src/main.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv
```

Alternatively, you can execute `./run.sh` script to run the code, move to the insight_testsuite and execute `./run_tests.sh` script to run all the test cases.
