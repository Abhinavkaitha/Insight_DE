import unittest
from data_processor import DataProcessor


class DataProcessorUnitTests(unittest.TestCase):

    def test_read_file_valid_file(self):
        file_path = "../input/Border_Crossing_Entry_Data.csv"
        dp = DataProcessor(input_file_name=file_path)
        self.assertIsNotNone(dp.data)

    def test_read_file_invalid_file(self):
        file_path = "invalid_path"
        dp = DataProcessor(input_file_name=file_path)
        self.assertIsNone(dp.data)

    def test_valid_fn(self):
        dp = DataProcessor()
        valid_row = ["Derby Line","Vermont","209","US-Canada Border","03/01/2019 12:00:00 AM","Truck Containers Full","6483","POINT (-72.09944 45.005)"]
        self.assertTrue(dp.valid(valid_row))

        invalid_rows = [["Derby Line","Vermont","209","US-Canada Border","","Truck Containers Full","6483","POINT (-72.09944 45.005)"],
                        ["Derby Line", "Vermont", "209", "US-Canada Border", "03/01/2019 12:00:00 AM", "Truck Containers Full", "",
                         "POINT (-72.09944 45.005)"],
                        ["Derby Line", "Vermont", "209", "US-Canada Border", "03/01/2019 12:00:00 AM",
                         "", "6483",
                         "POINT (-72.09944 45.005)"],
                        ["Derby Line", "Vermont", "209", "", "03/01/2019 12:00:00 AM",
                         "Truck Containers Full", "6483",
                         "POINT (-72.09944 45.005)"]]

        for row in invalid_rows:
            self.assertFalse(dp.valid(row))


if __name__ == '__main__':
    unittest.main()
