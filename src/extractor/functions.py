import numpy as np
import pandas as pd
from src.extractor import group_topic
import os
import ast

def get_file_path(bagfolder, topic):
    return bagfolder + "/" + topic.replace("/", "-")[1:] + ".csv"


def get_msg_and_info_db3(reader, connections):
    stamps = []
    df = pd.DataFrame()
    for conn, timestamp, rawdata in reader.messages(list(connections)):
        stamps.append(timestamp * (10 ** -9))
    data = pd.DataFrame({'Stamps': stamps})
    df = pd.concat([df, data], ignore_index=True)
    return df


def get_msg_and_info_mcap(connections):
    stamps = []
    df = pd.DataFrame()
    for conn in connections:
        timestamp = conn.log_time_ns
        stamps.append(timestamp * (10 ** -9))
    data = pd.DataFrame({'Stamps': stamps})
    df = pd.concat([df, data], ignore_index=True)
    return df


def _median(values):
    values_len = len(values)
    if values_len == 0:
        return float('nan')
    sorted_values = sorted(values)
    if values_len % 2 == 1:
        return sorted_values[int(values_len / 2)]

    lower = sorted_values[int(values_len / 2) - 1]
    upper = sorted_values[int(values_len / 2)]
    return float(lower+upper) / 2


def get_freq(stamps):
    period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
    med_period = _median(period)
    med_freq = round((1.0 / med_period), 2)
    return med_freq


def get_mean_freq(stamps):
    n_messages = len(stamps)
    total_time = stamps[len(stamps)-1] - stamps[0]
    if total_time == 0.0:
        mean_freq = float('nan')
    else:
        mean_freq = round((float(n_messages) / total_time), 2)
    return mean_freq


def get_all_nodes(input_file):
    df = pd.read_csv(input_file)
    return df['Name']


def read_csvs(bagfolder, input_file):
    df = pd.read_csv(input_file)
    node_pubs = ['Name', 'Publish']
    node_subs = ['Name', 'Subscribe']

    df_pubs = df[node_pubs]
    df_subs = df[node_subs]

    df_pubs.to_csv(os.path.join(bagfolder, 'pubs.csv'), index=False)
    df_subs.to_csv(os.path.join(bagfolder, 'subs.csv'), index=False)


def generate_topics(bagfolder, graph, topics):
    for topic in topics:
        if topic not in graph:
            tmp = pd.read_csv(get_file_path(bagfolder, topic))
            stamps = tmp['Stamps'].tolist()
            period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
            med_period = _median(period)
            med_freq = round((1.0 / med_period), 2)
            if str(med_freq) != 'nan':
                graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq)+'Hz'))
            else:
                graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq)))
            # graph.node(topic, topic, {'shape': 'rectangle'})
    group_topic.main(graph, topics)


def generate_nodes(graph, nodes):
    if len(nodes) > 0:
        for node in nodes:
            if node not in graph:
                graph.node(node, node, {'shape': 'ellipse'}, color='blue')


def generate_edges(bagfolder, graph, topics, nodes):
    for topic in topics:
        if topic == '/parameter_events':
            graph.edge('/parameter_events', '/_ros2cli_rosbag2')
        graph.edge('/_ros2cli_rosbag2', topic)

    if len(nodes) > 0:
        df_pubs = pd.read_csv(bagfolder+'/pubs.csv')
        df_subs = pd.read_csv(bagfolder+'/subs.csv')

        for node in nodes:
            pub_to_topics = ast.literal_eval(df_pubs[df_pubs['Name'] == node]['Publish'].values[0])
            sub_to_topics = ast.literal_eval(df_subs[df_subs['Name'] == node]['Subscribe'].values[0])

            if len(pub_to_topics) != 0:
                # pubs
                for topic_name in pub_to_topics:
                    if topic_name in graph:
                        graph.edge(node, topic_name, color='blue')
                    else:
                        graph.node(topic_name, topic_name, {'shape': 'rectangle'}, color='blue')
                        graph.edge(node, topic_name, color='blue')

            if len(sub_to_topics) != 0:
                # subs
                for topic_name in sub_to_topics:
                    if topic_name in graph:
                        graph.edge(topic_name, node, color='blue')
                    else:
                        graph.node(topic_name, topic_name, {'shape': 'rectangle'}, color='blue')
                        graph.edge(topic_name, node, color='blue')

            # remove the node if the node has no publisher or subscriber
            if len(pub_to_topics) == 0 and len(sub_to_topics) == 0:
                graph.body[:] = [item for item in graph.body if node not in item]


def create_graph(bagfolder, graph, topics, nodes):
    generate_topics(bagfolder, graph, topics)
    generate_nodes(graph, nodes)
    generate_edges(bagfolder, graph, topics, nodes)


def save_graph(bagfolder, graph):
    bagname = bagfolder.split('/')[-1]
    graph.render(filename=bagfolder.split('/')[-1],
                 directory="graphs/ros2/" + bagname)

    dot_file = "graphs/ros2/" + bagname + '/' + bagname + '.dot'
    with open(dot_file, 'w') as dot_file:
        dot_file.write(graph.source)