import pandas as pd
import os
import math

# df = pd.read_csv('../genre_data.csv')
# genre_dict = df.set_index('key').T.to_dict()
genre_dict = {}

# df = pd.read_csv('../person_data.csv')
# person_dict = df.set_index('key').T.to_dict()
person_dict = {}

# df = pd.read_csv('../lang_data.csv')
# lang_dict = df.set_index('key').T.to_dict()
lang_dict = {}

data = pd.read_csv('../temp_data.csv', dtype=str)
data = data.dropna()
res_df = pd.DataFrame(columns=data.columns)

def hash(data, dict):
    res = []
    for val in data:
        val = val.strip().lower().replace(" ", "_")
        if val not in dict:
            dict[val] = len(dict)
        res.append(dict[val])
    return res


for i in data.index:
    row = data.loc[i]
    print(row)
    row['title'] = row['title'].strip().lower().replace(" ", "_")
    row['duration'] = row['duration'].split(" ")[0].strip()
    row['genre'] = ','.join([str(x) for x in hash(row['genre'].split(","), genre_dict)])
    row['cast'] = ','.join([str(x) for x in hash(row['cast'].split(","), person_dict)])
    row['director'] = ','.join([str(x) for x in hash(row['director'].split(","), person_dict)])
    row['language'] = ','.join([str(x) for x in hash(row['language'].split(","), lang_dict)])
    res_df.loc[len(res_df.index)] = row

if os.path.exists('../genre_data.csv'):
    os.remove('../genre_data.csv')
df = pd.DataFrame(list(genre_dict.items()), columns=['key', 'value'])
df.to_csv('../genre_data.csv')

if os.path.exists('../person_data.csv'):
    os.remove('../person_data.csv')
df = pd.DataFrame(list(person_dict.items()), columns=['key', 'value'])
df.to_csv('../person_data.csv')

if os.path.exists('../lang_data.csv'):
    os.remove('../lang_data.csv')
df = pd.DataFrame(list(lang_dict.items()), columns=['key', 'value'])
df.to_csv('../lang_data.csv')

res_df.to_csv('../processed_data.csv')