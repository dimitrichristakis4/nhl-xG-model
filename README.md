# nhl-xG-model
XGBoost xG model trained on two seasons of MoneyPuck NHL shot data. Uses each shooter's cumulative shooting % and the goalie's cumulative save % at the time of every shot, so the model accounts for who is shooting and who is in net, not just shot location.

## Results

Tested on a held-out 20% of the dataset:

- Total actual goals: 1,460
- Total predicted goals: 1,416.4
- Aggregate error: 3.0%
- Avg error per game: 0.753 goals

## Data

Shot data sourced from [MoneyPuck](https://moneypuck.com/data.htm). Two seasons merged into one dataset. `training_data.csv` is the final feature-engineered dataset used for model training and testing.

## Pipeline

Run scripts in order:

1. `01_cumulative_stats.py` - computes cumulative shooting % and save % for every shooter and goalie up to each shot in the dataset (minimum 100 shots for shooters, 750 shots against for goalies before a stat is used)
2. `02_align_shot_ids.py` - reindexes season 2 shot IDs to be numerically sequential after season 1
3. `03_merge_seasons.py` - merges both seasons into one dataset
4. `04_build_training_set.py` - filters to shooters with 100+ shots and goalies with 750+ shots against, ensuring stable sample sizes before any stat is used
5. `05_validate.py` - computes mean save % and shooting % across the training dataset and compares to league averages from the two seasons used to verify the cumulative stat calculations are accurate
6. `06_model.py` - trains an XGBoost classifier, outputs aggregate goal predictions and error metrics

## Features

- `arenaAdjustedShotDistance`
- `shotAngleAdjusted`
- `lastEventShotAngle`
- `shotType` (one-hot encoded)
- `lastEventCategory` (one-hot encoded)
- `speedFromLastEvent`
- `timeSinceLastEvent`
- `distanceFromLastEvent`
- `averageRestDifference`
- `shotRebound`
- `shotRush`
- Cumulative shooter shooting % at time of shot
- Cumulative goalie save % at time of shot

## Why cumulative stats instead of season averages

Using a player's full-season stats to predict a shot from game 3 leaks future data into training. The cumulative stats only use what was actually known at the time of each shot, with minimum sample thresholds to prevent noisy early-season fluctuations from distorting the model.

## Model

XGBClassifier — 5,000 estimators, learning rate 0.01, early stopping after 50 rounds with no improvement on the test set. Categorical features one-hot encoded before fitting.
