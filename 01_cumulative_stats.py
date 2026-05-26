import pandas as pd

df = pd.read_csv('merged.csv')
df = df.sort_values('shotID').reset_index(drop=True)

shooters = df['shooterName'].unique()
shots_dict = {shots: 0 for shots in shooters}
goals_dict = {goals: 0 for goals in shooters}

goalies = df['goalieNameForShot'].unique()
goalies_shots_dict = {shots_against: 0 for shots_against in goalies}
goalies_goals_dict = {goals_against: 0 for goals_against in goalies}

shots_taken_list = []
goals_scored_list = []
shooting_percentage_list = []
shots_against_list = []
goals_against_list = []
save_percentage_list = []

for i in sorted(df['shotID'].unique()):
    row = df[df['shotID']==i][['shooterName', 'goalieNameForShot', 'goal', 'shotWasOnGoal', 'shotOnEmptyNet']].iloc[0]

    # record stats before this shot so we never use future data
    shots_taken_list.append(shots_dict[row['shooterName']])
    goals_scored_list.append(goals_dict[row['shooterName']])
    shots_against_list.append(goalies_shots_dict[row['goalieNameForShot']])
    goals_against_list.append(goalies_goals_dict[row['goalieNameForShot']])

    if shots_dict[row['shooterName']] == 0:
        shooting_percentage_list.append(0)
    else:
        shooting_percentage_list.append(goals_dict[row['shooterName']] / shots_dict[row['shooterName']])

    if goalies_shots_dict[row['goalieNameForShot']] == 0:
        save_percentage_list.append(0)
    else:
        save_percentage_list.append(1 - (goalies_goals_dict[row['goalieNameForShot']] / goalies_shots_dict[row['goalieNameForShot']]))

    # only count shots on goal, exclude empty net (goalie not present)
    if row['shotWasOnGoal'] == 1 and row['shotOnEmptyNet'] == 0:
        shots_dict[row['shooterName']] += 1
        goalies_shots_dict[row['goalieNameForShot']] += 1
        if row['goal'] == 1:
            goals_dict[row['shooterName']] += 1
            goalies_goals_dict[row['goalieNameForShot']] += 1

df['shotsTaken'] = shots_taken_list
df['goalsScored'] = goals_scored_list
df['shootingPercentage'] = shooting_percentage_list
df['shotsAgainst'] = shots_against_list
df['goalsAgainst'] = goals_against_list
df['savePercentage'] = save_percentage_list

print("Saving file...")
df.to_csv('merged_with_stats.csv', index=False)
print("Done.")
