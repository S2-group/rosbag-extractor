from graphviz import Digraph

# graph = Digraph(strict=True)  # root graph
list_of_str = []


# For each list of strings in the given list,
# get the str at given level, and only keep the unique subtopic
def extract_subtopic(list_s, level):
    result = []
    for l in list_s:
        if len(l) > level:
            if l[level] not in result:
                result.append(l[level])
    return result


# the name of subgraph must start with cluster
def get_sub_graph_name(name, graph_n):
    return '{0}_{1}_{2}'.format('cluster', name, graph_n)


def group_topics(parent_graph, level, old_list_t, longest_len, name, graph_n):
    if level < longest_len:
        # unique subtopics of current level
        sub_t = extract_subtopic(old_list_t, level)
        # print("subtopics: ", sub_t)

        for t in sub_t:
            name.append(t)
            # list that contains subtopic t
            new_list_t = []
            # longest length of subtopic among all lists in new_list_t
            longest_len = 0
            for list_l in old_list_t:
                if len(list_l) > level and list_l[level] == t:
                    new_list_t.append(list_l)
                    if len(list_l) > longest_len:
                        longest_len = len(list_l)

            cluster_name = '/'.join(name)
            sub_graph = Digraph(get_sub_graph_name(cluster_name, graph_n))
            sub_graph.attr(label=cluster_name)

            if len(new_list_t) > 1:
                for list_l in new_list_t:
                    topic_name = '/'.join(list_l)
                    sub_graph.node(topic_name, label=topic_name)
                parent_graph.subgraph(sub_graph)

            group_topics(sub_graph, level + 1, new_list_t, longest_len, name, graph_n)

            parent_graph.subgraph(sub_graph)

        # print('End of current level ----- ', level)
        # print("NOW BACK TO Previous level: ", level - 1)
        name.pop()

    else:
        # print("NO MORE")
        name.pop()
        return


def main(graph, topics, graph_n):
    # topics = ['/a/x/1', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2','/c']
    # topics = ['/a/x/1/m', '/a/x/1/n', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2',
    #           '/c', '/a/x/m/2', '/b/y/1', '/b/c', '/a/a', '/d/c/c/c/c/c/c/c', '/b/ccccccccccccccccccc']

    # # add each topic into the graph, label with its own name
    for topic in topics:
        graph.node(topic, topic, {'shape': 'rectangle'})

    longest_len = 0

    list_of_str = []
    # split each topic into a list of strings by '/'
    for topic in topics:
        tmp = list(topic.split('/'))
        list_of_str.append(tmp)
        if len(tmp) > longest_len:
            longest_len = len(tmp)

    # group_topics function takes 4 parameters (level, parent_graph, list_of_str, cluster_name)
    # parent_graph -> parent_graph of current level, starting with root graph => graph
    # level -> root level is always an empty string '', so recursion starts with 1
    # list_of_str -> list of strings that are ...
    # longest_len -> longest length among all lists in list_of_str
    # cluster_name -> a list of strings for creating cluster, always starting with ''
    # graph_n -> the number of graph in the series (if time-space is specified)
    group_topics(graph, 1, list_of_str, longest_len, [''], graph_n)

    # # view graph
    # graph.unflatten(stagger=3, fanout=True).view()


# if __name__ == '__main__':
    # graph=Digraph()
    # topics = ['/a/x/1', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2', '/c']
    # main(graph, topics, str(0))