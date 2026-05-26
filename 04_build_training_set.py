import pandas as pd

df = pd.read_csv('merged_with_stats.csv')

# only keep rows where the shooter has 100+ shots and the goalie has 750+ shots against
# this ensures stats are stable before they get used as features
df2 = df[(df['shotsTaken'] > 99) & (df['shotsAgainst'] > 749)]

df2.to_csv('training_data.csv', index=False)
