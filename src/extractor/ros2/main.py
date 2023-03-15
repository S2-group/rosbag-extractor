
import ros1_extract
import ros2_extract
import sys
from datetime import datetime
from rosbags.rosbag2 import Reader


def date_to_datetime(time):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")


def main():
    path_to_file = sys.argv[1]

    start = sys.argv[2]
    end = sys.argv[3]

    with Reader(path_to_file) as reader:
        bag_start = datetime.fromtimestamp(reader.start_time // 1000000000)
        bag_end = datetime.fromtimestamp(reader.end_time // 1000000000)
        # print("The bagfile STARTS at：", bag_start, " and ENDS at: ", bag_end)

    if start == 'start':
        start_t = bag_start
    else:
        try:
            if date_to_datetime(start) < bag_start or date_to_datetime(start) > bag_end:
                print("Please input a valid start time.")
                sys.exit()
            else:
                start_t = date_to_datetime(start)
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()

    if end == 'end':
        end_t = bag_end
    else:
        try:
            if date_to_datetime(end) > bag_end or date_to_datetime(end) < bag_start:
                print("Please input a valid end time.")
                sys.exit()
            else:
                end_t = date_to_datetime(end)
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()

    ros2_extract.main(path_to_file, start_t, end_t)


if __name__ == '__main__':
    main()
