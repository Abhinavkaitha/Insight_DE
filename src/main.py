import sys
from data_processor import DataProcessor

if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    dp = DataProcessor(input_file_name=input_dir)
    dp.generate_report(sys.argv[2])
