from rosbags.rosbag2 import Reader
from graphviz import Digraph
import pandas as pd
import os
from src.extractor import functions


def main(bagfolder, start_t, end_t, input_file, graph_n):
    graph = Digraph(name=bagfolder+graph_n)
    graph.graph_attr["rankdir"] = "LR"

    with Reader(bagfolder) as reader:
        all_info = pd.DataFrame()
        for topic in list(reader.topics):
            connections = [x for x in reader.connections if x.topic == topic]
            topic_info = functions.get_msg_and_info_db3(reader, connections)

            file_path = functions.get_file_path(bagfolder, topic)

            if os.path.exists(file_path):
                os.remove(file_path)
            topic_info.to_csv(file_path)

            all_info = functions.update_all_info(topic, topic_info, all_info)
        all_info.to_csv(bagfolder + '/' + 'all_info.csv')

        # topics within the time range
        topics = []
        for topic in list(reader.topics):
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

        metric = dict()
        metric['Filepath'] = bagfolder
        metric['Start'] = start_t
        metric['End'] = end_t

        functions.create_graph(bagfolder, graph, topics, nodes, graph_n, metric)

        # save graph
        functions.save_graph(bagfolder, graph, graph_n, "ros2")

        # view graph
        graph.unflatten(stagger=5, fanout=True).view()

# if __name__ == '__main__':
#     main(bagfolder, file, start, end, input)
