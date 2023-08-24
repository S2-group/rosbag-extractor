from mcap_ros2.reader import read_ros2_messages
import pandas as pd
import os
from graphviz import Digraph
from src.extractor import functions


def main(bagfolder, file, start_t, end_t, input_file):
    graph = Digraph(name=bagfolder, strict=True)
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

        file_path = functions.get_file_path(bagfolder, topic)

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

    all_info.to_csv(bagfolder + '/' + 'all_info.csv')

    # topics within the time range
    topics = []
    for topic in list(all_topics):
        topic_data = all_info.loc[all_info['topics'] == topic]
        if not topic_data.empty:
            if topic_data['start-time'].values[0] < end_t or topic_data['start-time'].values[0] == end_t:
                if topic_data['end-time'].values[0] > start_t:
                    topics.append(topic)

    if input_file is not None:  # with external file
        functions.read_csvs(bagfolder, input_file)
        nodes = functions.get_all_nodes(input_file)
    else:
        nodes = []

    functions.create_graph(bagfolder, graph, topics, nodes)

    functions.add_metrics(graph)

    # save graph
    graph.render(filename=bagfolder.split('/')[-1],
                 directory="graphs/ros2/" + bagfolder.split('/')[-1])
    # view graph
    graph.unflatten(stagger=5, fanout=True).view()

# if __name__ == '__main__':
#     main(bagfolder, file, start, end, input)
