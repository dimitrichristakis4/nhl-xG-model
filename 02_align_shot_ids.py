import pandas as pd

# shift season 2 shot IDs so they are numerically sequential after season 1
df = pd.read_csv('shots_2025_new.csv')
df['shotID'] = df['shotID'] + 119870
df.to_csv('shots_2025_reindexed.csv', index=False)
