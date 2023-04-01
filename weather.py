import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# retrieve weather data from ThingSpeak API
#url = 'https://api.thingspeak.com/channels/2071618/feeds.json?api_key=T7FZHLOVDBQK0GZB&results=2'
#response = requests.get(url)
#data = response.json()['feeds']
#df = pd.DataFrame(data)
df=pd.read_csv('feeds.csv')

# preprocess the data
df = df.drop(['entry_id', 'created_at', 'latitude', 'longitude'], axis=1)
df['date'] = pd.to_datetime(df['field1'])
df['temperature'] = pd.to_numeric(df['field1'])
df['humidity'] = pd.to_numeric(df['field2'])
df['pressure'] = pd.to_numeric(df['field3'])
df['rain'] = pd.to_numeric(df['field4'])
df = df.set_index('date')

# split the data into training and testing sets
X = df.drop('temperature', axis=1)
y = df['temperature']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = model.score(X_test, y_test)
print('MSE:', mse)
print('RMSE:', rmse)
print('R-squared:', r2)

# make predictions on new weather data
new_data = {'date': ['2023-03-19'], 'humidity': [70], 'pressure': [1013.25], 'rain': [0]}
df_new = pd.DataFrame(new_data)
df_new['date'] = pd.to_datetime(df_new['date'])
df_new = df_new.set_index('date')
temp_pred = model.predict(df_new)
print('Predicted temperature:', temp_pred[0])

# plot the results
plt.plot(y_test.index, y_test.values, label='Actual')
plt.plot(y_test.index, y_pred, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.legend()
plt.show()
