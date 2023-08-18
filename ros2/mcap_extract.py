from mcap_ros2.reader import read_ros2_messages
import pandas as pd
import os
from graphviz import Digraph
import functions
import yml_to_csv


def main(folder, file, start_t, end_t):
    graph = Digraph(name=folder, strict=True)
    graph.graph_attr["rankdir"] = "LR"
    # add fixed nodes
    graph.node('/_ros2cli_rosbag2', '/_ros2cli_rosbag2')

    # get all topics
    all_topics = []
    for msg in read_ros2_messages(file):
        if msg.channel.topic not in all_topics:
            all_topics.append(msg.channel.topic)

    all_info = pd.DataFrame()

    for topic in all_topics:
        connections = read_ros2_messages(file, topics=topic)

        topic_info = functions.get_msg_and_info_mcap(connections)

        file_path = functions.get_file_path(folder, topic)

        if os.path.exists(file_path):
            os.remove(file_path)
        topic_info.to_csv(file_path)

        if len(topic_info['Stamps'].head(1).values) != 0 and len(topic_info['Stamps'].tail(1).values) != 0:
            new_data = pd.DataFrame({'topics': topic,
                                     'start-time': topic_info['Stamps'].head(1).values,
                                     'end-time': topic_info['Stamps'].tail(1).values,
                                     'med-frequency': functions.get_freq(topic_info['Stamps'].tolist()),
                                     'mean-frequency': functions.get_mean_freq(topic_info['Stamps'].tolist())
                                     })
            all_info = pd.concat([all_info, new_data], ignore_index=True)

    all_info.to_csv(folder + '/' + 'all_info.csv')

    # topics within the time range
    topics = []
    for topic in list(all_topics):
        topic_data = all_info.loc[all_info['topics'] == topic]
        if not topic_data.empty:
            if topic_data['start-time'].values[0] < end_t or topic_data['start-time'].values[0] == end_t:
                if topic_data['end-time'].values[0] > start_t:
                    topics.append(topic)


    functions.create_graph(folder, graph, topics)

    functions.add_metrics(graph)

    # save graph
    graph.render(filename=folder.split('/')[-1],
                 directory="graphs/ros2/" + folder.split('/')[-1])
    # view graph
    graph.unflatten(stagger=5, fanout=True).view()

# if __name__ == '__main__':
#     file = "/Users/berry.c/Desktop/rosbag/bagfiles/ros2/iron_mcap/rosbag2_2023_07_24-15_37_31/rosbag2_2023_07_24-15_37_31_0.mcap"
#     folder = "/Users/berry.c/Desktop/rosbag/bagfiles/ros2/iron_mcap/rosbag2_2023_07_24-15_37_31"
#
#     reader = make_reader(open(file, "rb"), decoder_factories=[DecoderFactory()])
#
#     start = reader.get_summary().statistics.message_start_time / 1000000000
#     end = reader.get_summary().statistics.message_end_time / 1000000000
#
#     main(folder, file, start, end)
