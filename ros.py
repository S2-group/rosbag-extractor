import sys
import subprocess

bagfile = sys.argv[1]
print("filename: \n", bagfile)

# get all info in the bag
all_info = subprocess.run(['rosbag', 'info', bagfile])
print("\nall info: \n", all_info)

# generate computational graph
subprocess.run(['rqt_graph'], shell=True)

'''
# get all topic info in the bag
topic_info = []
topics = all_info['topics']
for topic in topics:
    topic_info.append(topic['topic'])
# print("\ntopics: \n", topics)
'''

# time_start = all_info['start']
# time_end = all_info['end']
# time_duration = all_info['duration']
# print("\n start:    ", time_start, "\n  end:     ", time_end, "\n duration: ", time_duration)
