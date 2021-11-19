import pandas as pd
df_ids = pd.read_csv('data/player_ids.csv', index_col=0)
id_dict = [{'label': _[0], 'value': _[1]} for _ in df_ids.values]

print(id_dict)
