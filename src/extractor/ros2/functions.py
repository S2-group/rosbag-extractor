import pandas as pd
import group_topic


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



def generate_edges(graph, topics):
    for topic in topics:
        if topic == '/parameter_events':
            graph.edge('/parameter_events', '/_ros2cli_rosbag2')
        graph.edge('/_ros2cli_rosbag2', topic)


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


def create_graph(bagfolder, graph, topics):
    generate_topics(bagfolder, graph, topics)
    # generate_nodes(graph, all_info)
    generate_edges(graph, topics)
