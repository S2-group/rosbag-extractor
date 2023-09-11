# python3 bag_extract.py bagfile

from bagpy import bagreader
import pandas as pd
import sys
import ast
from graphviz import Digraph
from rosbag import ROSBagException


def read_rosout(b, bagname):
    csvfiles = []
    data = b.message_by_topic('/rosout')
    csvfiles.append(data)

    rosout = pd.read_csv(bagname + '/rosout.csv')
    all_info = rosout[['name', 'msg', 'topics']]
    return all_info

def generate_topics(graph, all_topics):
    sub_topics = []
    for topic in all_topics:
        sub_topics += topic.split('/')[1:]
        if topic not in graph:
            graph.node(topic, topic, {'shape': 'rectangle'})

    for sub_topic in sub_topics:
        if sub_topics.count(sub_topic) > 1:
            substring = '/' + sub_topic
            # create clusters
            with graph.subgraph(name='cluster_'+ sub_topic) as sub_topic:
                for topic in all_topics:
                    if substring in topic:
                        sub_topic.node(topic, topic, {'shape' : 'rectangle'})
                sub_topic.attr (label=substring)

def generate_edges(graph, all_info, nodes):
    # merge subscribers for each node
    edge_info = pd.DataFrame(data={'name': nodes}, columns=['name', 'topics'])
    for i in range(len(nodes)):
        list_of_topics = []
        for j in range(len(all_info)):
            # merge topics with the same node name
            # print(all_info['name'][j])
            if all_info['name'][j] == nodes[i]:
                # evaluate string as list and merge them into one list
                list_of_topics += ast.literal_eval(all_info['topics'][j])
        # keep the unique value in the list of topics
        edge_info['topics'][i] = list(set(list_of_topics))

    # relationship contained in 'topics'
    for i in range(len(nodes)):
        publisher = nodes[i]
        for j in range(len(edge_info['topics'][i])):
            subscriber = edge_info['topics'][i][j]
            graph.edge(publisher, subscriber)

    # relationship contained in 'msg'
    substring = "Subscribing to "
    valid_msg = all_info['msg'].dropna()
    for i in range(len(valid_msg)):
        if substring in valid_msg.iloc[i]:
            publisher = valid_msg.iloc[i].split(substring)[1]
            subscriber = all_info['name'].iloc[i]
            graph.edge(publisher, subscriber)


def extract_graph(bag, topics, all_info):
    graph = Digraph(name=bag)

    generate_topics(graph, topics)

    # if no '/rosout' topic in the bag file
    if len(all_info) == 0:
        # print("FALSE")
        # nodes
        graph.node("/rosbag_record", "/rosbag_record", {'shape': 'oval'})
        graph.node("/rosout", "/rosout", {'shape': 'rectangle'})

        # edges
        graph.edge("/rosbag_record", "/rosout")
        for topic in topics:
            graph.edge(topic, "/rosbag_record")
    else:
        # print("TRUE")
        # nodes
        nodes = all_info['name'].unique()
        for node in nodes:
            graph.node(node, node, {'shape': 'oval'})

        # edges
        generate_edges(graph, all_info, nodes)

    # add fixed node and edges
    graph.node("/fixed node", "/rosout", {'shape': 'oval'})
    graph.edge("/rosout", "/fixed node")
    graph.edge("/fixed node", "/rosout_agg")

    # save graph
<<<<<<< HEAD:src/extractor/ros1/extract_graph.py
    graph.render(filename=bagname.split('/')[-1],
                 directory="graphs/ros1/"+bagname.split('/')[-1])
=======
    bagname = bag.split('/')[-1]
    graph.render(filename=bag.split('/')[-1],
                 directory="graphs/ros1/"+bagname)

    dot_file = "graphs/ros1/"+ bagname + '/' + bagname + '.dot'
    with open(dot_file, 'w') as dot_file:
        dot_file.write(graph.source)
>>>>>>> 6e6001b6a833874f359c0f430ea2da9796b05d4c:src/extractor/bag_extract.py

    # view graph
    graph.unflatten(stagger=3, fanout=True).view()


def get_file_name(folder):
    return folder + '/' + folder.split('/')[-1] + ".bag"


def main(bagfolder):
    # bagfile = sys.argv[1]
    bagfile = get_file_name(bagfolder)
    bag = bagfile.replace('.bag', '')

    while(True):
        try:
            b = bagreader(bagfile)
            break
        except ROSBagException as err:
            print(err)
            sys.exit()

    if '/rosout' in b.topics:
        # print("TRUE")
        all_info = read_rosout(b, bag)
    else:
        # print("FALSE")
        # print(b.topics)
        sys.exit()

    extract_graph(bag, b.topics, all_info)


# if __name__ == "__main__":
#     main()
