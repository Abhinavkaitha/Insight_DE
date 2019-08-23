import csv
import collections
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

def round_fun(number):
    number_dec = int(str(number-int(number))[2:3])
    if number_dec < 5:
        return int(number)
    return int(number) + 1

def type_check(x):
    if type(x) is int:
        return x
    return 0

def is_date(string):

    try:
        parse(string, fuzzy=False)
        return True

    except ValueError:
        return False


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def validate(Border, Date, Measure, Value):
    if Border == "" or Date == "" or Measure == "" or Value == "":
        return False

    if not is_date(Date) or not is_int(Value):
        return False

    return True

def read(file):
    nested_list = []
    with open(file, newline='') as csvfile:
        border_file = csv.reader(csvfile, delimiter = ',')
        _ = next(border_file)
        for row in border_file:
            nested_list.append(row)
    return nested_list

def data_structure(data_nested_list):

    data_dict = collections.defaultdict(lambda: collections.defaultdict(
        lambda: (collections.defaultdict(lambda: (int, int)), 0)))

    data_nested_list = sorted(data_nested_list, key=lambda x: x[4])
    report = []

    # 0 Port Name, 1 State, 2 Port Code, 3 Border, 4 Date, 5 Measure, 6 Value, 7 Location

    tuple_first_element = 0

    tuple_second_element = 1

    for row in data_nested_list:

        Border = row[3]

        Date = row[4]

        Measure = row[5]

        Value = row[6]

        try:
            new_value = int(Value) + data_dict[Border][Measure][tuple_first_element][Date][tuple_first_element]
        except:
            new_value = int(Value)
        if Date not in data_dict[Border][Measure][tuple_first_element]:
            try:
                new_value_dict = {Date: (new_value, round_fun(data_dict[Border][Measure][tuple_second_element] / len(
                    data_dict[Border][Measure][tuple_first_element])))}
            except:
                new_value_dict = {Date: (new_value, 0)}
        else:
            new_value_dict = {
                Date: (new_value, data_dict[Border][Measure][tuple_first_element][Date][tuple_second_element])}
        new_dict = dict(data_dict[Border][Measure][tuple_first_element], **new_value_dict)
        data_dict[Border][Measure] = (new_dict, data_dict[Border][Measure][tuple_second_element] + int(Value))
    return data_dict



def write(data_dict):

    rows = []
    for border, val in data_dict.items():
        row1 = {'Border': border}
        for measure, vals in val.items():
            row2 = dict({'Measure': measure}, **row1)
            for dat, vals2 in vals[0].items():
                row3 = dict({'Date': dat, 'Value': vals2[0], 'Average': type_check(vals2[1])}, **row2)
                rows.append(row3)
    rows = sorted(rows, key=lambda i: (i['Date'], i['Value'],i['Measure'], i['Border']),reverse=True)
    try:
        with open(output_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Border', 'Date', 'Measure', 'Value', 'Average'])
            writer.writeheader()
            for data in rows:
                writer.writerow(data)
    except IOError:
        print("I/O error")


if __name__ == "__main__":

    data_nested_list = read(input_file)

    data_dict = data_structure(data_nested_list)

    write(data_dict)
