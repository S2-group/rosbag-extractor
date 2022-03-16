import rosbag
import sys
import os
import yaml
import subprocess
import string

bagfile = sys.argv[1]
print("filename: \n", bagfile)

# get all info in the bag
all_info = yaml.safe_load(subprocess.Popen(['rosbag', 'info', '--yaml', bagfile], stdout=subprocess.PIPE).communicate()[0])
# print("\nall info: \n", all_info)

# get all topic info in the bag
topic_info = []
topics = all_info['topics']
for topic in topics:
    topic_info.append(topic['topic'])
# print("\ntopics: \n", topics)

# publishers and subscribers
# publishers = yaml.safe_load(subprocess.Popen(['rostopic', 'list', '-p', bagfile]).communicate()[0])
# print("\npublishers: \n", publishers)

'''
time_start = all_info['start']
time_end = all_info['end']
time_duration = all_info['duration']
print("\n start:    ", time_start, "\n  end:     ",
      time_end, "\n duration: ", time_duration)
'''

# generate computational graph
yaml.safe_load(subprocess.Popen(['rqt_graph'], stdout=subprocess.PIPE).communicate()[0])
