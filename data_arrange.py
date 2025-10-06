#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import os
import pandas as pd

DIR_PATH = "/Users/ipekoner/Desktop/f1-ml/f1-data"

def load_and_preview_csv(file_name, dir_path):
    file_path =os.path.join(dir_path, file_name)
    df = pd.read_csv(file_path)
    return df.head(), df.info(), df.describe()

filenames = [f for f in os.listdir(DIR_PATH) if f.endswith(".csv")]

data_overview = {}

for file in filenames:
    data_overview[file] = load_and_preview_csv(file, DIR_PATH)

print(data_overview.keys())

print(os.listdir(DIR_PATH))


# In[3]:


import pandas as pd

results = pd.read_csv(os.path.join(DIR_PATH, "results.csv"))
drivers = pd.read_csv(os.path.join(DIR_PATH, "drivers.csv"))

results_subset = results[["raceId","driverId","constructorId","grid","position"]]

merged = results_subset.merge(drivers, on="driverId", how="inner")

final_df = merged[["raceId","driverId","constructorId","grid","position", "forename", "surname"]]

final_df


# In[4]:


races = pd.read_csv(os.path.join(DIR_PATH, "races.csv"))

merged = results.merge(drivers, on="driverId", how="inner") #merging drivers to results with the key as driverId 

merged = merged.merge(races[["raceId","name", "date", "year"]], on="raceId", how="inner") #taking the merged and merging races to it with the selected columns with the key as raceId
#also, next time pls just extract the year from the date by using datetime, this is kinda stupid lmao
final_df = merged[["raceId","name", "driverId","constructorId","date", "year", "grid","position", "forename", "surname"]]

final_df


# In[5]:


merged["grid"] = pd.to_numeric(merged["grid"], errors = "coerce")
merged["position"] = pd.to_numeric(merged["position"], errors = "coerce")

merged["delta"] = merged["grid"] - merged["position"]

print(merged[["raceId","name", "driverId","constructorId","grid","position", "forename", "surname", "delta"]])

merged["delta"] = merged["grid"] - merged["position"]

merged


# In[6]:


teams = pd.read_csv(os.path.join(DIR_PATH, "constructors.csv"))
team_points = pd.read_csv(os.path.join(DIR_PATH, "constructor_results.csv"))

team_points = team_points[["raceId", "constructorId", "points"]].rename(
    columns={"points": "constructor_points"}
)
teams = teams[["constructorId", "name"]].rename(columns={"name": "constructor_name"})



merged = merged.merge(team_points, on=["raceId", "constructorId"], how="left")
merged = merged.merge(teams, on="constructorId", how="left")


merged = merged[["raceId","date", "year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points"]]

merged




# In[7]:


merged = merged.dropna(subset=["position"])


# In[8]:


merged = merged.copy()
merged["position"] = pd.to_numeric(merged["position"], errors = "coerce")
merged["avg_position"] =merged.groupby("driverId")["position"].transform("mean")
merged = merged[["raceId","date","year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points", "avg_position"]]
merged


# In[9]:


merged.isnull().sum()


# In[10]:


merged["constructor_points"] = merged["constructor_points"].fillna(0)


# In[11]:


merged.isnull().sum()


# In[12]:


total_avg_position = merged.groupby(["driverId", "surname"])["position"].mean().reset_index()

total_avg_position = total_avg_position.rename(columns={"position": "avg_position_total"})

total_avg_position.head()


# In[13]:


merged["constructor_points"] = pd.to_numeric(merged["constructor_points"], errors = "coerce")
merged["constructor_points_sum"] = merged.groupby("constructorId")["constructor_points"].transform("sum")

merged = merged[["raceId","date","year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points", "avg_position","constructor_points_sum"]]


merged


# In[14]:


merged["constructor_points"] = pd.to_numeric(merged["constructor_points"], errors = "coerce")
merged["constructor_points_avg"] = merged.groupby("constructorId")["constructor_points"].transform("mean")

merged = merged[["raceId","date", "year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points", "avg_position","constructor_points_sum", "constructor_points_avg"]]


merged


# In[15]:


merged["season_avg_position"] = merged.groupby(["driverId", "year"])["position"].transform("mean")

merged = merged[["raceId","date", "year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points", "avg_position","constructor_points_sum", "constructor_points_avg","season_avg_position"]]
merged


# In[16]:


merged["podium"] = (merged["position"] <= 3).astype(int)

merged["pole"] = (merged["grid"] == 1).astype(int)

merged = merged[["raceId","date", "year","name", "driverId","constructorId","grid","position", "forename", "surname", "delta", "constructor_name", "constructor_points", "avg_position","constructor_points_sum", "constructor_points_avg","season_avg_position", "podium", "pole"]]
merged


# In[17]:


#check the bias and variance cost func lowkey i forgot
from sklearn.preprocessing import LabelEncoder
import pandas as pd

le = LabelEncoder()
merged["driverId_encoded"] = le.fit_transform(merged["driverId"])
merged["constructorId_encoded"] = le.fit_transform(merged["constructorId"])
merged["GP_name_encoded"] = le.fit_transform(merged["name"])

merged

#print("Category mapping:", le.classes_)


# In[18]:


merged["driver_fullname"] = merged["forename"] + " " + merged["surname"]
merged


# In[19]:


merged.isnull().sum()


# In[20]:


merged = merged.copy()
merged["season_avg_delta"] = merged.groupby(["driverId", "year"])["delta"].transform("mean")
merged


# In[21]:


merged.to_csv("f1_merged_database_new.csv")


# In[22]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

X = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y = merged["podium"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state= 42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state = 42)

rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
print(f"Accurracy: {accuracy: .2f}")
print("\nClassification Report:", classification_rep)

sample = X_test.iloc[0:1]
prediction = rf_classifier.predict(sample)


# In[23]:


from imblearn.over_sampling import RandomOverSampler
X_class = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y_class = merged["podium"]

X_train, X_test, y_train, y_test = train_test_split(X_class, y_class, test_size = 0.2, random_state=42)
sm= RandomOverSampler(random_state = 42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42, class_weight ="balanced")
rf_classifier.fit(X_train_res, y_train_res)
y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
print(f"Accurracy: {accuracy: .2f}")
print("\nClassification Report:", classification_rep)


# In[24]:


from imblearn.over_sampling import SMOTE
X_class_1 = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y_class_1 = merged["podium"]

X_train, X_test, y_train, y_test = train_test_split(X_class_1, y_class_1, test_size = 0.2, random_state=42)
ac= SMOTE(random_state = 42)
X_train_res, y_train_res = ac.fit_resample(X_train, y_train)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_res, y_train_res)
y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
print(f"Accurracy: {accuracy: .2f}")
print("\nClassification Report:", classification_rep)


# In[25]:




# In[28]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score 
import math

X_reg = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y_reg = merged["position"]

X_train, X_test, y_train, y_test = train_test_split( X_reg, y_reg, test_size = 0.2,  random_state = 42)
rf_regressor = RandomForestRegressor(n_estimators = 300, random_state = 42, min_samples_leaf = 2,)
rf_regressor.fit(X_train, y_train)
y_pred_reg = rf_regressor.predict(X_test)

mae = mean_absolute_error(y_test, y_pred_reg)
mse = mean_squared_error(y_test, y_pred_reg)
rmse = math.sqrt(mean_squared_error(y_test, y_pred_reg))
r2 = r2_score(y_test, y_pred_reg)


print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"r2: {r2})")

sample = X_test.iloc[0:1]
predicted_position = rf_regressor.predict(sample)[0]
print(f"Predicted finishing position: {predicted_position:.1f}")


# In[35]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score 
from sklearn.model_selection import RandomizedSearchCV
import math

X_reg = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y_reg = merged["position"]

X_train, X_test, y_train, y_test = train_test_split( X_reg, y_reg, test_size = 0.2, random_state = 42)

param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'bootstrap': [True, False]
}

random_search = RandomizedSearchCV(estimator = RandomForestRegressor (random_state = 42), param_distributions = param_grid, n_iter = 10, cv = 3, verbose = 2, n_jobs = -1, scoring = "neg_mean_absolute_error", random_state = 42)



random_search.fit(X_train, y_train)
print(random_search.best_estimator_)



# In[36]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score 
import math

X_reg = merged[["driverId_encoded", "constructorId_encoded", "GP_name_encoded", "constructor_points_avg", "constructor_points_sum", "season_avg_position", "season_avg_delta", "grid"]]
y_reg = merged["position"]

X_train, X_test, y_train, y_test = train_test_split( X_reg, y_reg, test_size = 0.2,  random_state = 42)
rf_regressor = RandomForestRegressor(max_depth=10, min_samples_leaf=2, n_estimators=50, random_state=42)
rf_regressor.fit(X_train, y_train)
y_pred_reg = rf_regressor.predict(X_test)

mae = mean_absolute_error(y_test, y_pred_reg)
mse = mean_squared_error(y_test, y_pred_reg)
rmse = math.sqrt(mean_squared_error(y_test, y_pred_reg))
r2 = r2_score(y_test, y_pred_reg)


print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"r2: {r2})")

sample = X_test.iloc[0:1]
predicted_position = rf_regressor.predict(sample)[0]
print(f"Predicted finishing position: {predicted_position:.1f}")


# In[ ]:
import joblib
joblib.dump(rf_classifier, "rf_podium_model.joblib")
joblib.dump(rf_regressor, "rf_position_model.joblib")

#do hyperparameter tuning for randomforestregressor

