from bagpy import bagreader
import pandas as pd
import sys
import os
import ast
from graphviz import Digraph
from rosbag import ROSBagException
import json
from src.extractor import functions


def get_file_name(folder):
    return folder + '/' + folder.split('/')[-1] + ".bag"


def generate_topics(bag, graph, all_topics, metric):
    sub_topics = []
    for topic in all_topics:
        sub_topics += topic.split('/')[1:]
        if topic not in graph:
            tmp = pd.read_csv(functions.get_file_path(bag, topic))
            stamps = tmp['Stamps'].tolist()
            period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
            med_period = functions._median(period)
            med_freq = round((1.0 / med_period), 2)
            if str(med_freq) != 'nan':
                graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq) + 'Hz'))
            else:
                graph.node(topic, topic, {'shape': 'rectangle'})
            data = {topic: {'name': topic,
                            'start': stamps[1],
                            'end': stamps[-1],
                            'frequency': med_freq
                            }}
            metric["Topics"].update(data)

    for sub_topic in sub_topics:
        if sub_topics.count(sub_topic) > 1:
            substring = '/' + sub_topic
            # create clusters
            with graph.subgraph(name='cluster_' + sub_topic) as sub_topic:
                for topic in all_topics:
                    if substring in topic:
                        tmp = pd.read_csv(functions.get_file_path(bag, topic))
                        stamps = tmp['Stamps'].tolist()
                        period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
                        med_period = functions._median(period)
                        med_freq = round((1.0 / med_period), 2)
                        if str(med_freq) != 'nan':
                            sub_topic.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq) + 'Hz'))
                        else:
                            sub_topic.node(topic, topic, {'shape': 'rectangle'})
                        data = {topic: {'name': topic,
                                        'start': stamps[1],
                                        'end': stamps[-1],
                                        'frequency': med_freq
                                        }}
                        metric["Topics"].update(data)
                sub_topic.attr(label=substring)


def generate_edges(graph, rosout_info, topics, nodes, metric):
    # merge subscribers for each node
    edge_info = pd.DataFrame(data={'name': nodes}, columns=['name', 'topics'])
    for i in range(len(nodes)):
        list_of_topics = []
        for j in range(len(rosout_info)):
            # merge topics with the same node name
            # print(rosout_info['name'][j])
            if rosout_info['name'][j] == nodes[i]:
                # evaluate string as list and merge them into one list
                list_of_topics += ast.literal_eval(rosout_info['topics'][j])
        # keep the unique value in the list of topics
        edge_info['topics'][i] = list(set(list_of_topics))

    # relationship contained in 'topics'
    for i in range(len(nodes)):
        publisher = nodes[i]
        for j in range(len(edge_info['topics'][i])):
            subscriber = edge_info['topics'][i][j]
            if subscriber in topics:
                graph.edge(publisher, subscriber)
                metric['Nodes'][publisher]['#subscriber'] += 1
                metric['Nodes'][publisher]['avg_pub_freq'] = functions.update_avg_freq(metric, publisher, subscriber)

    # relationship contained in 'msg'
    substring = "Subscribing to "
    valid_msg = rosout_info['msg'].dropna()
    for i in range(len(valid_msg)):
        if substring in valid_msg.iloc[i]:
            publisher = valid_msg.iloc[i].split(substring)[1]
            subscriber = rosout_info['name'].iloc[i]
            graph.edge(publisher, subscriber)
            metric['Nodes'][subscriber]['#publisher'] += 1


def extract_graph(bag, topics, rosout_info, metric):
    graph = Digraph(name=bag)

    # initialize the metric
    metric['Topics'] = {}
    metric['Nodes'] = {}

    # add fixed node
    graph.node("/fixed node", "/rosout", {'shape': 'oval'})
    metric['Nodes'].update({'/rosout': {'name': '/rosout',
                                        'source': 'fixed node',
                                        '#publisher': 0,
                                        '#subscriber': 0,
                                        'avg_pub_freq': 0}})

    # topics
    generate_topics(bag, graph, topics, metric)

    # add fixed edges
    graph.edge("/rosout", "/fixed node")
    metric['Nodes']['/rosout']['#subscriber'] += 1
    metric['Nodes']['/rosout']['avg_pub_freq'] = functions.update_avg_freq(metric, '/rosout', '/rosout')
    graph.edge("/fixed node", "/rosout_agg")
    metric['Nodes']['/rosout']['#publisher'] += 1
    metric['Nodes']['/rosout']['avg_pub_freq'] = functions.update_avg_freq(metric, '/rosout', '/rosout_agg')

    # nodes
    nodes = rosout_info['name'].unique()
    for node in nodes:
        graph.node(node, node, {'shape': 'oval'})
        metric['Nodes'].update({node: {'name': node,
                                       'source': 'bagfile',
                                       '#publisher': 0,
                                       '#subscriber': 0,
                                       'avg_pub_freq': 0}})

    # edges
    generate_edges(graph, rosout_info, topics, nodes, metric)

    # save graph
    bagname = bag.split('/')[-1]
    graph.render(filename=bag.split('/')[-1],
                 directory="graphs/ros1/"+bagname)

    dot_file = "graphs/ros1/" + bagname + '/' + bagname + '.dot'
    with open(dot_file, 'w') as dot_file:
        dot_file.write(graph.source)

    # view graph
    graph.unflatten(stagger=3, fanout=True).view()


def main(bagfolder, start_t, end_t):
    bagfile = get_file_name(bagfolder)
    bag = bagfile.replace('.bag', '')

    while True:
        try:
            b = bagreader(bagfile)
            break
        except ROSBagException as err:
            print(err)
            sys.exit()

    if '/rosout' in b.topics:
        rosout = pd.read_csv(b.message_by_topic('/rosout'))
        rosout_info = rosout[(rosout['Time'] >= start_t) & (rosout['Time'] <= end_t)][['name', 'msg', 'topics']]
        rosout_info = rosout_info.reset_index(drop=True)
        rosout_info.to_csv(bagfolder + '/' + 'rosout_info.csv')

        all_info = pd.DataFrame()
        for topic in b.topics:
            stamps = pd.read_csv(b.message_by_topic(topic))['Time']
            topic_info = pd.DataFrame({'Stamps': stamps})

            file_path = functions.get_file_path(bag, topic)
            if os.path.exists(file_path):
                os.remove(file_path)
            topic_info.to_csv(file_path)

            all_info = functions.update_all_info(topic, topic_info, all_info)

        all_info.to_csv(bagfolder + '/' + 'all_info.csv')

        # topics within the time range
        topics = []
        for topic in list(b.topics):
            topic_data = all_info.loc[all_info['topics'] == topic]
            if not topic_data.empty:
                if topic_data['start-time'].values[0] < end_t or topic_data['start-time'].values[0] == end_t:
                    if topic_data['end-time'].values[0] > start_t:
                        topics.append(topic)

    else:
        print("No architectural information can be extracted because the topic '/rosout' is not recorded")
        sys.exit()

    metric = dict()
    metric['Filepath'] = bagfolder
    metric['Start'] = start_t
    metric['End'] = end_t

    extract_graph(bag, topics, rosout_info, metric)

    # save metric
    directory = 'metrics/'
    metric_path = 'metrics/' + bagfolder.split('/')[-1] + '.json'
    os.makedirs(directory, exist_ok=True)
    with open(metric_path, 'w') as json_file:
        json.dump(metric, json_file, indent=4)

# if __name__ == "__main__":
#     main()
