import pandas as pd
import yml_to_csv
import transform_csv

def main(yml_file_path):
    csv_file = yml_to_csv.main(yml_file_path)
    transformed_csv = transform_csv.main(csv_file)



if __name__ == '__main__':
    main()
