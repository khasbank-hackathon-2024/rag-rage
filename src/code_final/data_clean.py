import pandas as pd 
import numpy as np 
import joblib 


df = pd.read_csv('data_dummy/khas_bank_branches.csv')
df = df.drop(['type'], axis=1)
s = f"{df.iloc[1]['name']} нь {df.iloc[1]['open_time']} нээж {df.iloc[1]['close_time']} хаадаг. Салбарын байршил{df.iloc[1]['address']}.Холбогдох утасны дугаар {df.iloc[1]['phone']}"
print(s)