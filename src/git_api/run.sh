# extraction_script filename where_to_look terms start_result_index username hash
#./extract.sh internet_of_things description internet+things 51 someone hash


### extract repositories
# extraction_script filename start_result_index terms username hash
./extract_repo.sh repos 0 rosbag BerryC-VU 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

### extract commits
# extraction_script filename start_result_index terms username hash
./extract_commits.sh commits 0 rosbag BerryC-VU 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

### extract rosbag_experiment related repos+commits
./extract_ros_exp.sh ros_exp rosbag+experiment BerryC-VU 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

### merge all JSON files python3 ./merge.py json_path result_name
python3 ./merge.py data/repos merge/repos
python3 ./merge.py data/commits merge/commits
python3 ./merge.py data/ros_exp merge/ros_exp


