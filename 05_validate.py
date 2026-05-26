import pandas as pd

# check mean save % and shooting % against known league averages to confirm calculations are correct
df = pd.read_csv('training_data.csv')

meansvpct = df['savePercentage'].mean()
meanshootingpct = df['shootingPercentage'].mean()

print("Mean shooting %:", meanshootingpct)
print("Mean save %:", meansvpct)
