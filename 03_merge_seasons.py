import pandas as pd

df1 = pd.read_csv('shots_2024.csv')
df2 = pd.read_csv('shots_2025_reindexed.csv')

pd.concat([df1, df2], ignore_index=True).to_csv('merged.csv', index=False)
