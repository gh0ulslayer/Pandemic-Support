import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import random
import math
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime
import operator 
plt.style.use('fivethirtyeight')


days_in_future = 20


def daily_increase(data):
    d = [] 
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d

def getplot(india_daily_increase):
      plt.figure(figsize=(16, 9))
      adjusted_dates = []
      for i in range(len(india_daily_increase)):
            adjusted_dates.append(int(i))
      plt.bar(adjusted_dates, india_daily_increase)
      plt.title('INdia Daily Increases in Confirmed Cases', size=30)
      plt.xlabel('Days Since 28/3/2020', size=30)
      plt.ylabel('Number of Cases', size=30)
      plt.xticks(size=20)
      plt.yticks(size=20)
      plt.show()

def plot_predictions(x, y, pred, algo_name, color,future_forecast):
    plt.figure(figsize=(16, 9))
    plt.plot(x, y)
    
    plt.plot(future_forecast, pred, linestyle='dashed', color=color)
    plt.title('Number of Coronavirus Cases Over Time', size=30)
    plt.xlabel('Days Since 1/22/2020', size=30)
    plt.ylabel('Number of Cases', size=30)
    plt.legend(['Confirmed Cases', algo_name], prop={'size': 20})
    plt.xticks(size=20)
    plt.yticks(size=20)
    plt.show()

confirmed_cases = pd.read_csv('''https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv''')

# print(confirmed_cases.head)
cols = confirmed_cases.keys()
# print(cols[70])
confirmed = confirmed_cases.loc[:, cols[100]:cols[-1]]
dates = confirmed.keys()


world_cases = []
india_cases = []

for i in dates:
      confirmed_sum = confirmed[i].sum()
      world_cases.append(confirmed_sum)
      india_cases.append(confirmed_cases[confirmed_cases['Country/Region']=='India'][i].sum())

world_daily_increase = daily_increase(world_cases)
india_daily_increase = daily_increase(india_cases)

# getplot(india_daily_increase)

days_since_3_28 = np.array([i for i in range(len(dates))]).reshape(-1, 1)

X_train_confirmed, X_test_confirmed, y_train_confirmed, y_test_confirmed = train_test_split(days_since_3_28, india_cases, test_size=0.0001, shuffle=False)


future_forecast = np.array([i for i in range(len(dates)+days_in_future)]).reshape(-1, 1)
adjusted_dates = future_forecast[:-20]

poly = PolynomialFeatures(degree=3)
poly_X_train_confirmed = poly.fit_transform(X_train_confirmed)
poly_X_test_confirmed = poly.fit_transform(X_test_confirmed)
poly_future_forecast = poly.fit_transform(future_forecast)

linear_model = LinearRegression(normalize=True, fit_intercept=False)
linear_model.fit(poly_X_train_confirmed, y_train_confirmed)
# test_linear_pred = linear_model.predict(poly_X_train_confirmed)
linear_pred = linear_model.predict(poly_future_forecast)


# plt.plot(linear_pred)
plt.plot(y_train_confirmed)
plt.plot(linear_pred)
plt.legend(['Test Data', 'Polynomial Regression Predictions'])
plt.show()

# svm_confirmed = SVR(shrinking=True, kernel='poly',gamma=0.01, epsilon=1,degree=3, C=0.1)
# svm_confirmed.fit(X_train_confirmed, y_train_confirmed)
# svm_pred = svm_confirmed.predict(X_train_confirmed)
# # svm_test_pred = svm_confirmed.predict(X_test_confirmed)
# plt.plot(y_train_confirmed)
# plt.plot(svm_pred)
# plt.legend(['Test Data', 'SVM Predictions'])
# plt.show()
