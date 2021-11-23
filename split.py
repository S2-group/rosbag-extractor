import rosbag
import sys
import os
import yaml
import subprocess
import string

bagfile = sys.argv[1]
print("filename: \n", bagfile)

new_start_time = sys.argv[2]
new_end_time = sys.argv[3]
outbag_name = sys.argv[4]

time_range = "t.secs >= " + new_start_time + \
    " and t.secs <= " + new_end_time
print("test str is: ", time_range)

# created a rosbag with given rosbag name
outbag = outbag_name + ".bag"
print("\noutbag name is: ", outbag)

'''
command = "rosbag " + "filter " + bagfile + " " + outbag + " " + test_str
print("\ncommand is: ", command)
'''

yaml.safe_load(subprocess.Popen(
    ['rosbag', 'filter', bagfile, outbag, time_range], stdout=subprocess.PIPE).communicate()[0])
