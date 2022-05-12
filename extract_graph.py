# python3 extract_graph.py bagfile

from bagpy import bagreader
import pandas as pd
import sys
import ast
from graphviz import Digraph
import os.path


bagfile = sys.argv[1]
bagname = bagfile.replace('.bag', '')
b = bagreader(bagfile)

# topics into dataFrame for extraction to generate graph
topics = pd.DataFrame(b.topics, columns=['Topics'])
# print(topics)

# list of csv files based on the topics
csvfiles = []
topiclist = ['/rosout', '/rosout_agg']
for t in topiclist:
    data = b.message_by_topic(t)
    csvfiles.append(data)

print("Finished extracting csv files")

# # if no rosout file is present
# if not os.path.exists(bagname + '/rosout.csv'):
# merge files and only keep needed columns
rosout = pd.read_csv(bagname + '/rosout.csv')
rosout_agg = pd.read_csv(bagname + '/rosout_agg.csv')
rosout = pd.concat([rosout, rosout_agg]).reset_index()
all_info = rosout[['name', 'msg', 'topics']]


graph = Digraph(name=bagname, strict=True)

all_topics = topics['Topics'].values.tolist()
sub_topics = []
# topics
topics = topics['Topics'].values.tolist()
for topic in topics:
    if topic not in graph:
        graph.node(topic, topic, {'shape': 'rectangle'})

for i in range(len(all_topics)):
    sub_topics += all_topics[i].split('/')[1:]

for sub_topic in sub_topics:
    if sub_topics.count(sub_topic) > 1:
        substring = '/' + sub_topic
        # create clusters
        with graph.subgraph(name='cluster_' + sub_topic) as sub_topic:
            for topic in all_topics:
                if substring in topic:
                    sub_topic.node(topic, topic, {'shape': 'rectangle'})
            sub_topic.attr(label=substring)


# nodes
nodes = rosout['name'].unique()
for node in nodes:
    graph.node(node, node, {'shape': 'oval'})

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

# edges
for i in range(len(nodes)):
    publisher = nodes[i]
    for j in range(len(edge_info['topics'][i])):
        subscriber = edge_info['topics'][i][j]
        graph.edge(publisher, subscriber)

# msg in both rosout and rosout_agg
substring = "Subscribing to "
valid_msg = all_info['msg'].dropna()
for i in range(len(valid_msg)):
    if substring in valid_msg.iloc[i]:
        publisher = valid_msg.iloc[i].split(substring)[1]
        subscriber = all_info['name'].iloc[i]
        graph.edge(publisher, subscriber)

# add fixed node and edges
graph.node("/fixed node", "/rosout", {'shape': 'oval'})
graph.edge("/rosout", "/fixed node")
graph.edge("/fixed node", "/rosout_agg")

# generate graph
graph.unflatten(stagger=3,fanout=True).view()
# graph.view()