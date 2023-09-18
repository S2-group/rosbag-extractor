import sys
from bagpy import bagreader
from rosbags.rosbag2 import Reader
from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
from src.extractor import bag_extract as bag
from src.extractor import db3_extract as db3
from src.extractor import mcap_extract as mcap


def get_mcap_file_name(path_to_file):
    folder = path_to_file.split('/')[-1]
    return path_to_file + "/" + folder + "_0.mcap"


def check_time_range(start, bag_start, end, bag_end):
    if start == 'start':
        start_t = bag_start
    else:
        try:
            if float(start) + bag_start > bag_end:
                print("Please input a valid start time. The bag has duration of", str(bag_end-bag_start), 'seconds')
                # print("Current start_time: ", start)
                # print("Bag file start_time: ", bag_start)
                # print("Bag file end_time: ", bag_end)
                sys.exit()
            else:
                start_t = float(start) + bag_start
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()

    if end == 'end':
        end_t = bag_end
    else:
        try:
            if float(end) < 0 or float(end) + bag_start > bag_end:
                print("Please input a valid end time. The bag has duration of", str(bag_end-bag_start), 'seconds')
                sys.exit()
            else:
                end_t = float(end) + bag_start
        except ValueError as err:
            print("ValueError: ", err)
            sys.exit()
    return start_t, end_t


def extractor(start, end, path_to_file, filetype, input_file, time_space):
    if filetype == 'bag':
        bagfile = path_to_file + '/' + path_to_file.split('/')[-1] + ".bag"

        b = bagreader(bagfile)
        # bag_start = b.start_time
        # bag_end = b.end_time
        # start_t, end_t = check_time_range(start, bag_start, end, bag_end)
        # bag.main(path_to_file, start_t, end_t, input_file)
        bag.main(path_to_file)
    elif filetype == 'db3':
        with Reader(path_to_file) as reader:
            bag_start = reader.start_time / 1000000000
            bag_end = reader.end_time / 1000000000

        start_t, end_t = check_time_range(start, bag_start, end, bag_end)

        if time_space is not None:
            start_t_spaced = start_t
            graph_n = 0
            time_space = float(time_space)
            while start_t_spaced+time_space < bag_end:
                print("The extraction of graph " + str(graph_n) + " STARTS at", start_t_spaced, "and ENDS at",
                      start_t_spaced+time_space, "\nThe duration of bag is: " + str(time_space), 'seconds')
                db3.main(path_to_file, start_t_spaced, start_t_spaced+time_space, input_file, str(graph_n))
                start_t_spaced += time_space
                graph_n += 1

            # last graph
            print("The extraction of graph " + str(graph_n) + " STARTS at", start_t_spaced, "and ENDS at",
                  end_t, "\nThe duration of bag is: " + str(end_t-start_t_spaced), 'seconds')
            db3.main(path_to_file, start_t_spaced, end_t, input_file, str(graph_n))
        else:
            graph_n = 0
            print("The extraction STARTS at", start_t, "and ENDS at", end_t, "\nThe duration of bag is: " + str(end_t-start_t), 'seconds')
            db3.main(path_to_file, start_t, end_t, input_file, str(graph_n))

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

        if time_space is not None:
            start_t_spaced = start_t
            graph_n = 0
            time_space = float(time_space)
            while start_t_spaced+time_space < bag_end:
                print("The extraction of graph " + str(graph_n) + " STARTS at", start_t_spaced, "and ENDS at",
                      start_t_spaced+time_space, "\nThe duration of bag is: " + str(time_space), 'seconds')
                mcap.main(path_to_file, file_mcap, start_t_spaced, start_t_spaced+time_space, input_file, str(graph_n))
                start_t_spaced += time_space
                graph_n += 1

            # last graph
            print("The extraction of graph " + str(graph_n) + " STARTS at", start_t_spaced, "and ENDS at",
                  end_t, "\nThe duration of bag is: " + str(end_t-start_t_spaced), 'seconds')
            mcap.main(path_to_file, file_mcap, start_t_spaced, end_t, input_file, str(graph_n))
        else:
            graph_n = 0
            print("The extraction STARTS at", start_t, "and ENDS at", end_t, "\nThe duration of bag is: " + str(end_t-start_t), 'seconds')
            mcap.main(path_to_file, file_mcap, start_t, end_t, input_file, str(graph_n))


# if __name__ == '__main__':
#     extractor()
