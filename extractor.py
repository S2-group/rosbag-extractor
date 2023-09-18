import os, sys
import argparse
from src.extractor import main


def check_files_extension(folder_path, extension):
    for filename in os.listdir(folder_path):
        if filename.endswith(extension):
            return True
    return False


def run_extractor(ros_version, start_time, end_time, file_path, filetype, input, time_space):
    print(">>>> Bag File Extractor <<<<")

    if start_time is None:
        start_time = 'start'
    if end_time is None:
        end_time = 'end'

    if ros_version == 'ros1':
        if filetype == 'bag':
            main.extractor(start_time, end_time, file_path, filetype, input, time_space)
        else:
            print("ROS1 only has filetype `bag`")
            sys.exit()
    elif ros_version == 'ros2':
        if filetype == 'db3':
            if check_files_extension(file_path, '.db3'):
                main.extractor(start_time, end_time, file_path, filetype, input, time_space)
            else:
                print("Cannot find the correct file with the input filetype: " + filetype)
        elif filetype == 'mcap':
            if check_files_extension(file_path, '.mcap'):
                main.extractor(start_time, end_time, file_path, filetype, input, time_space)
            else:
                print("Cannot find the correct file with the input filetype: " + filetype)
        else:
            print("Input the correct filetype. Valid filetypes in ROS2 are 'db3' and 'mcap'.")
    else:
        print("ROS version is unknown")

    print(">>>>>>>>>>>>>><<<<<<<<<<<<<<<")


def run():
    # Arguments definition and management
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--ros_version', help='ROS Version: ros1 or ros2', required=True, type=str)
    parser.add_argument('-s', '--start_time', help='User-defined start time (in seconds)', required=False, type=str)
    parser.add_argument('-e', '--end_time', help='User-defined end time (in seconds)', required=False, type=str)
    parser.add_argument('-f', '--file_path', help='Path to FOLDER containing the ros bagfile.', required=True, type=str)
    parser.add_argument('-ft', '--file_type', help='Bag file type: bag, db3 or mcap', required=True, type=str)
    parser.add_argument('-i', '--input', help='Path to file containing nodes information', required=False, type=str)
    parser.add_argument('-ts', '--time_space', help='Time in second to generate a series of interconnected graphs', required=False, type=str)
    options = parser.parse_args()

    run_extractor(options.ros_version,
                  options.start_time,
                  options.end_time,
                  options.file_path,
                  options.file_type,
                  options.input,
                  options.time_space)


if __name__ == "__main__":
    run()