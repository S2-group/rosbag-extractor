#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:01:35 2022

@author: michel
"""

import bagpy
from bagpy import bagreader
import pandas as pd

b = bagreader('./turtlesim1.bag')

print(b.topic_table)

csvfiles = []
for t in b.topics:
    data = b.message_by_topic(t)
    print(data)
    csvfiles.append(data)
# mt = b.message_types

# nm = b.n_messages

# bmessage = b.reader
# all_info = yaml.safe_load(subprocess.Popen(bmessage, stdout=subprocess.PIPE).communicate()[0])

# for bm in bmessage:
#    print(bm.message)
#    all_info = yaml.safe_load(subprocess.Popen(bm.message, stdout=subprocess.PIPE).communicate()[0])

    # print("######")
    # print(bm.topic)
    

# yaml.safe_load(subprocess.Popen(['rqt_graph'], stdout=subprocess.PIPE).communicate()[0])


# LASER_MSG = b.message_by_topic('/vehicle/front_laser_points')
# LASER_MSG
# df_laser = pd.read_csv(LASER_MSG)
# df_laser
