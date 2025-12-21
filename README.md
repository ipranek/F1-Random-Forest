Overview (Project In Progress):

This project is a Random Forest machine learning interactive web application. This project predicts whether an F1 driver with a specific constructor on a specific track (determined by the user) will be able to finish on the podium, given they start with pole position. 

Using historical Formula 1 data (1950–2024), the model incorporates:
  Driver information (skill & consistency through average positions)
  Constructor (team) performance (points & averages across seasons)
  Race information (Grand Prix names)
  Starting position (grid)
Currently in the process of including an experimental conversational interface that allows users to query race data and model predictions using LLMs. 

Motivation:
Pole position is a crucial achievement, but it doesn't guarantee a podium finish. Therefore, this project explores how historical race data, driver performance, and constructor strength influence race outcomes, as well as how ML predictions can be explained using SHAP values and LLM interfaces. 

Tech Stack:
Backend: Python Flask
Machine Learning: scikit-learn: Random Forest Classifier and Regressor
Data storage and preprocessing: SQLite, Pandas, NumPy
Model Explanation: SHAP
NLP Interface: LangChain

Modelling Approach:

Random Forest Classifier --> to model the probability of seeing if someone who gets pole position can end up on the podium that same weekend. Class imbalance is handled with SMOTE, and the final accuracy is 86%. 
Random Forest Regression --> to model where a person who got pole position can end up in the race rankings. Hyperparameter tuning is done using RandomizedSearchCV. The performance improvements are: MAE: 2.16 -> 2.07; R-squared: 0.63 -> 0.66. 

How to Run Locally?

pip install -r requirements.txt
python app.py
