import sys
from rosbags.rosbag2 import Reader
import ros2_extract


def main():
    path_to_file = sys.argv[1]

    # time parsed as in second (str)
    start = sys.argv[2]
    end = sys.argv[3]

    with Reader(path_to_file) as reader:
        # time in second
        bag_start = reader.start_time / 1000000000
        bag_end = reader.end_time / 1000000000

        # bag_duration = reader.duration / 1000000000

    if start == 'start':
        start_t = bag_start
    else:
        try:
            if float(start) < bag_start or float(start) > bag_end:
                print("Please input a valid start time.")
                print("Current start_time: ", start)
                print("Bag file start_time: ", bag_start)
                print("Bag file end_time: ", bag_end)
                sys.exit()
            else:
                start_t = float(start)
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()

    if end == 'end':
        end_t = bag_end
    else:
        try:
            if float(end) > bag_end or float(end) < bag_start:
                print("Please input a valid end time.")
                sys.exit()
            else:
                end_t = float(end)
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()

    print("The extraction STARTS at", start_t, "and ENDS at", end_t)
    ros2_extract.main(path_to_file, start_t, end_t)


if __name__ == '__main__':
    main()