import sys
from rosbags.rosbag2 import Reader
from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import db3_extract
import mcap_extract
# from mcap_ros2.reader import read_ros2_messages
# import mcap
# from mcap.mcap0.stream_reader import StreamReader


def get_mcap_file_name(path_to_file):
    folder = path_to_file.split('/')[-1]
    return path_to_file + "/" + folder + "_0.mcap"


def check_time_range(start, bag_start, end, bag_end):
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
    return start_t, end_t


def main():
    # time parsed as in second (str)
    start = sys.argv[1]
    end = sys.argv[2]
    path_to_file = sys.argv[3]
    filetype = sys.argv[4]

    if filetype == 'db3':
        with Reader(path_to_file) as reader:
            bag_start = reader.start_time / 1000000000
            bag_end = reader.end_time / 1000000000

        start_t, end_t = check_time_range(start, bag_start, end, bag_end)
        print("The extraction STARTS at", start_t, "and ENDS at", end_t)
        db3_extract.main(path_to_file, start_t, end_t)
    else:
        file_mcap = get_mcap_file_name(path_to_file)
        reader = make_reader(open(file_mcap, "rb"), decoder_factories=[DecoderFactory()])

        # connections = read_ros2_messages(file_mcap)

        # Reference: https://pypi.org/project/mcap/0.0.4/ -> version 0.0.14
        # stream = open(file_mcap, "rb")
        # reader = StreamReader(stream)
        # file_path = 'test.txt'
        # with open(file_path, 'w') as file:
        #     for record in reader.records:
        #         file.write(str(record) + '\n')
                    # print(record)

        # print("THIS IS READER:", reader.records)

        bag_start = reader.get_summary().statistics.message_start_time / 1000000000
        bag_end = reader.get_summary().statistics.message_end_time / 1000000000

        start_t, end_t = check_time_range(start, bag_start, end, bag_end)
        print("The extraction STARTS at", start_t, "and ENDS at", end_t)
        mcap_extract.main(path_to_file, file_mcap, start_t, end_t)


if __name__ == '__main__':
    main()
