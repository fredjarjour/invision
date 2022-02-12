import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score
from main import database

# Selecting model variables (change object to access the database)

X, y = database.generate_training()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

gb = GradientBoostingRegressor()

# Probably going to take too long => 

# Rate at which correcting is being made
learning_rate = [0.001, 0.01, 0.1, 0.2]
# Number of trees in Gradient boosting
n_estimators=list(range(500,1000,100))
# Maximum number of levels in a tree
max_depth=list(range(4,9,4))
# Minimum number of samples required to split an internal node
min_samples_split=list(range(4,9,2))
# Minimum number of samples required to be at a leaf node.
min_samples_leaf=[1,2,5,7]
# Number of features to be considered at each split
max_features=['auto','sqrt']

# Hyperparameters dict
param_grid = {"learning_rate":learning_rate,
              "n_estimators":n_estimators,
              "max_depth":max_depth,
              "min_samples_split":min_samples_split,
              "min_samples_leaf":min_samples_leaf,
              "max_features":max_features}

# Creating model and running rsv to find the best parameters
gb_rs = RandomizedSearchCV(estimator = gb, param_distributions = param_grid, random_state=1)
gb_rs.fit(X_train,y_train)

# Finding best parameters
print("\n The best parameters across ALL searched params:\n", gb_rs.best_params_)

# Fiting model with best parameters
model = GradientBoostingRegressor(n_estimators=600, min_samples_split= 4, min_samples_leaf= 1, max_features= 'auto', max_depth=4, learning_rate=0.01)
model.fit(X_train, y_train)
GradientBoostingRegressor(learning_rate=0.01, max_depth=4, max_features='auto',
                          min_samples_split=4, n_estimators=600)

# Making predictions
predictions = model.predict(X_test)
print(predictions)

# Evaluates predictions 
print('r2:', r2_score(y_test, predictions))
print('MAE:', mean_absolute_error(y_test, predictions))
print('MSE:', mean_squared_error(y_test, predictions))

# Imports 
model = pd.read_pickle(r'predictor/price/vehicles/file.pkl')

# Dumps model into a pkl file
file = open("file.pkl", "wb") 
pickle.dump(model, file)