# extraction_script filename where_to_look terms start_result_index username hash
#./extract.sh internet_of_things description internet+things 51 someone hash


### extract repositories
# extraction_script filename terms username hash
#./extract_repo.sh repos rosbag BerryC-VU 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

### extract commits
# extraction_script filename terms username hash
#./extract_commits.sh commits rosbag BerryC-VU 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

### extract rosbag_experiment related repos+commits
./extract_ros_exp.sh ros_exp rosbag+experiment BerryC-VU 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

### merge all JSON files
# python3 ./merge.py