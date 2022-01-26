import json
import pandas as pd
import os
import sys

json_path = sys.argv[1]
result_path = sys.argv[2]

# print(json_path)
# print(result_path)
# print(len(os.listdir(json_path)))

files = []
for i in range(len(os.listdir(json_path))):
    files.append(json_path + "/" + str(i) + ".json")

merged = []
for i in range(len(os.listdir(json_path))):
    with open(files[i]) as f:
        merged.append(json.load(f)['items'])

df = pd.DataFrame()
for i in range(len(merged)):
    df = df.append(pd.json_normalize(merged[i]))

df = df[['name', 'full_name', 'html_url', 'description', 'created_at', 'updated_at', 'git_url']].reset_index(drop=True)

os.makedirs('result', exist_ok=True)
df.to_csv(result_path + ".csv")

