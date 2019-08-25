import os
import csv
import collections
from utils import round_fun, is_date, is_int, type_check
import sys


class DataProcessor:
    def __init__(self, num_rows=-1, input_dir_path="../input/", required_column_indices=[3, 4, 5, 6]):
        self.num_rows = num_rows
        self.input_dir_path = input_dir_path.split("/")[0]+"/"+input_dir_path.split("/")[1]
        self.required_column_indices = required_column_indices
        self.report_dict = collections.defaultdict(lambda: collections.defaultdict(
            lambda: (collections.defaultdict(lambda: (int, int)), 0)))
        self.data = self.read_files()

    def valid(self, data_row):
        for ind in self.required_column_indices:
            if data_row[ind] == "":
                return False
        if not is_date(data_row[4]) or not is_int(data_row[6]):
            return False
        return True

    def read_files(self):
        data = []
        cursor = 0
        for input_file in os.listdir(self.input_dir_path):
            with open(self.input_dir_path + input_file) as csv_file:
                border_file = csv.reader(csv_file, delimiter=',')
                _ = next(border_file)
                for row in border_file:
                    if self.valid(row) and (self.num_rows < 0 or cursor < self.num_rows):
                        data.append(row)
                        cursor += 1
        return data

    def process_data(self):
        self.data = sorted(self.data, key=lambda x: x[4])
        report = []

        # 0 Port Name, 1 State, 2 Port Code, 3 Border, 4 Date, 5 Measure, 6 Value, 7 Location
        tuple_first_element = 0
        tuple_second_element = 1

        for row in self.data:
            border = row[3]
            date = row[4]
            measure = row[5]
            value = row[6]
            try:
                new_value = int(value) + self.report_dict[border][measure][tuple_first_element][date][tuple_first_element]
            except:
                new_value = int(value)
            if date not in self.report_dict[border][measure][tuple_first_element]:
                try:
                    new_value_dict = {
                        date: (new_value, round_fun(self.report_dict[border][measure][tuple_second_element] / len(
                            self.report_dict[border][measure][tuple_first_element])))}
                except:
                    new_value_dict = {date: (new_value, 0)}
            else:
                new_value_dict = {
                    date: (new_value, self.report_dict[border][measure][tuple_first_element][date][tuple_second_element])}
            new_dict = dict(self.report_dict[border][measure][tuple_first_element], **new_value_dict)
            self.report_dict[border][measure] = (new_dict, self.report_dict[border][measure][tuple_second_element] + int(value))

    def generate_report(self, output_file):
        self.process_data()
        rows = []
        for border, val in self.report_dict.items():
            row1 = {'Border': border}
            for measure, vals in val.items():
                row2 = dict({'Measure': measure}, **row1)
                for dat, vals2 in vals[0].items():
                    row3 = dict({'Date': dat, 'Value': vals2[0], 'Average': type_check(vals2[1])}, **row2)
                    rows.append(row3)
        rows = sorted(rows, key=lambda i: (i['Date'], i['Value'], i['Measure'], i['Border']), reverse=True)
        try:
            with open(output_file, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=['Border', 'Date', 'Measure', 'Value', 'Average'])
                writer.writeheader()
                for data in rows:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
