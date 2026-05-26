import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv('training_data.csv')

df['lateralDistanceFromLastEvent'] = abs(df['arenaAdjustedYCord'] - df['lastEventyCord_adjusted'])
df['verticalDistanceFromLastEvent'] = abs(df['arenaAdjustedXCord'] - df['lastEventxCord_adjusted'])

OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
categorical_cols = ['lastEventCategory', 'shotType']

y = df['goal']
X = df[['arenaAdjustedShotDistance', 'averageRestDifference', 'distanceFromLastEvent',
        'savePercentage', 'shootingPercentage', 'lastEventCategory', 'lastEventShotAngle',
        'shotType', 'speedFromLastEvent', 'timeSinceLastEvent', 'distanceFromLastEvent',
        'shotAngleAdjusted', 'shotRebound', 'shotRush']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# one-hot encode categorical features
OH_train = pd.DataFrame(OH_encoder.fit_transform(X_train[categorical_cols]))
OH_test = pd.DataFrame(OH_encoder.transform(X_test[categorical_cols]))
OH_train.index = X_train.index
OH_test.index = X_test.index

num_X_train = X_train.drop(categorical_cols, axis=1)
num_X_test = X_test.drop(categorical_cols, axis=1)
X_train = pd.concat([num_X_train, OH_train], axis=1)
X_test = pd.concat([num_X_test, OH_test], axis=1)

# 5000 estimators with early stopping — stops if no improvement after 50 rounds
model = XGBClassifier(n_estimators=5000, learning_rate=0.01, n_jobs=6, random_state=0,
                      early_stopping_rounds=50)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

# predict_proba gives goal probability per shot — sum across game gives predicted goals
scores = model.predict_proba(X_test)[:, 1]
goalsPredicted = scores.sum()
Error = y_test.sum() - goalsPredicted

print("Total goals in test set:", y_test.sum())
print("Total goals predicted in test set:", goalsPredicted)
print("Difference:", Error)
print("% error:", (Error / y_test.sum()) * 100)

df_test = df.loc[X_test.index].copy()
df_test['xG'] = scores
Predicted_goals = df_test.groupby('game_id')['xG'].sum()
Actual_goals = df_test.groupby('game_id')['goal'].sum()
Avg_error = (Predicted_goals - Actual_goals).abs().mean()

print("Average error in predicted goals per game:", Avg_error)
print("Training set size:", len(X_train))
