import bagpy
from bagpy import bagreader
import pandas as pd
import sys
import ast
import networkx as nx
from matplotlib import pyplot as plt

# './SLAM_2021-06-03-12-32-22.bag'
bagname = sys.argv[1]
b = bagreader(bagname + ".bag")

# print(b.topic_table)

# topics into dataFrame for further extraction to generate graph
topics = pd.DataFrame(b.topics, columns=['Topics'])
# print(topics)

'''
# create a list of csv files based on the topics
csvfiles = []
for t in b.topics:
    data = b.message_by_topic(t)
    # print(data)
    csvfiles.append(data)
'''

df = pd.read_csv(bagname + '/rosout.csv')
df2 = pd.read_csv(bagname + '/rosout_agg.csv')
df = pd.concat([df, df2]).reset_index()

all_info = df[['name', 'topics']]
# print(all_info)

nodes = df['name'].unique()
# print(nodes[1])

graph_info = pd.DataFrame(data={'name': nodes}, columns=['name', 'topics'])
list_of_topics = []
# list_of_msgs = []
# substring = "Subscribing to "

for i in range(len(nodes)):
    for j in range(len(all_info)):
        # merge topics with the same node name
        if all_info['name'][j] == nodes[i]:
            # evaluate string as list and merge them into one list
            list_of_topics += ast.literal_eval(all_info['topics'][j])

    # only keep the unique value in the list of topics
    # reference:
    # https://www.freecodecamp.org/news/python-unique-list-how-to-get-all-the-unique-values-in-a-list-or-array/
    graph_info['topics'][i] = list(set(list_of_topics))
    # graph_info['msg'][i] = list_of_msgs
# print(graph_info)


# DAG graph
graph = nx.Graph()

pos = nx.spring_layout(graph)  # positions for all nodes

for i in range(len(nodes)):
    graph.add_node(nodes[i])

for i in range(len(topics)):
    graph.add_node(topics['Topics'][i])

for i in range(len(nodes)):
    from_node = nodes[i]
    for j in range(len(graph_info['topics'][i])):
        to_node = graph_info['topics'][i][j]
        graph.add_edge(from_node, to_node)

# add fixed node and edges
graph.add_node("/rosout")
graph.add_edge("/rosout", "/rosout_agg")

# print(graph.node())
# print(graph.edges())

# TODO: find a better layout of the graph
# draw graph
# node_color = "" Set node_color
nx.is_directed(graph)
nx.is_directed_acyclic_graph(graph)
nx.draw_networkx(graph, arrows=True)

# show graph
plt.show()

# save graph
# plt.savefig(path, format="")
# plt.savefig("test.png", format="PNG")
