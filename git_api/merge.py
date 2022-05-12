import json
import pandas as pd
import os
import sys

json_path = sys.argv[1]
result_path = sys.argv[2]

# print(json_path)
# print(result_path)
# print(len(os.listdir(json_path)))

# merge json files into DataFrame
files = []
for i in range(len(os.listdir(json_path))):
    files.append(json_path + "/" + str(i) + ".json")
print("files finished")

merged = []
for i in range(len(os.listdir(json_path))):
    with open(files[i]) as f:
        tmp = json.load(f)['items']
        if tmp:
            merged.append(tmp)
        # else:
        #    print("List is empty")
print("merge finished")

df = pd.DataFrame()
for i in range(len(merged)):
    new_data = pd.DataFrame(pd.json_normalize(merged[i]))
    df = pd.concat([df, new_data])


# converting to csv files (repo & ros_repo)
# rosout = rosout[['name', 'full_name', 'html_url', 'description',
#          'created_at', 'updated_at', 'git_url']].reset_index(drop=True)
# rosout.to_csv(result_path + ".csv")

# converting to csv files (commits)
df = df[['commit.message', 'repository.html_url']].reset_index(drop=True)

df2 = df.groupby('repository.html_url')
repos = list(df2.groups.keys())
# print(len(repos))

result = pd.DataFrame()
for i in range(len(repos)):
    msg = df[df['repository.html_url'] == repos[i]]['commit.message'].values
    tmp_df = pd.DataFrame(msg, columns = [repos[i]]).transpose()
    result = pd.concat([result, tmp_df])

result.to_csv(result_path + ".csv")

