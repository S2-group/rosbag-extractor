import rosbag
import sys,os
import yaml
import subprocess

"""
https://github.com/aktaylor08/RosbagPandas/blob/f9997baa9a681edaa670d27df78955a5941bb3a4/src/rosbag_pandas/rosbag_pandas.py#L208
"""

bagfile = sys.argv[1]
print("filename: \n", bagfile)

#get all info in the bag
all_info = yaml.safe_load(subprocess.Popen(['rosbag', 'info', '--yaml', bagfile], stdout=subprocess.PIPE).communicate()[0])
print("\ninfo: \n", all_info)

#get all topic info in the bag
topic_info = []
topics = all_info['topics']
for topic in topics:
    topic_info.append(topic['topic'])
print("\ntopics: \n", topics)

'''
rqt_graph = yaml.safe_load(subprocess.Popen(['rqt_graph'], stdout=subprocess.PIPE).communicate()[0])
'''