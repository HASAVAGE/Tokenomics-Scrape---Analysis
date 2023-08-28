import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

# Whitepaper 'constants'
initialLOAN = 72647650990.8235
poolRewards = 200e6 * 6
farmRewards = 1e9
stakeRewards = 8e9
totalRewards = poolRewards + farmRewards + stakeRewards


# Define Functions
def date_convert(date_to_convert):
    return datetime.datetime.strptime(date_to_convert, '%d/%m/%Y %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')


def linear_regression(column):
    x = np.array(df['hours-elapsed']).reshape((-1, 1))
    y = np.array(df[column]).reshape((-1, 1))
    model = LinearRegression().fit(x, y)
    if model.score(x, y) > 0.7:
        print(column)
        print('Rsq:', model.score(x, y))
        print('Model:', model.coef_, 'x +',  model.intercept_)
        if i == 'Issued':
            print('Annual Inflation Rate:', ((model.coef_*8760 + model.intercept_)/last_row['Issued']))
            print('Predicted supply next year:', last_row['Issued']*
                  ((model.coef_*8760 + model.intercept_)/last_row['Issued']))
        print('__________________________________________________________________________________________________')
        dex = plt.plot(x, model.coef_ * x + model.intercept_, color='Red')
        return dex

# Read .csv, save file in data frame
loan = pd.read_csv(r'C:\Users\19788\Desktop\Archive\Scripts\Incoming\loan.csv')
df = pd.DataFrame(loan)

# Create column group, removed Vesting & Undistributed Exchanges
group1 = ['Issued',
          'Circulating',
          'Staked',
          'Farming and Staking Rewards',
          'Pooled Liquidity']

for i in group1:
    df[i] = abs(df[i])

# Adjust data frame with calculated columns
df['Circulating/Issued'] = df['Circulating'] / df['Issued']
df['Staked/Issued'] = df['Staked'] / df['Issued']
df['Circulating/Staked'] = df['Circulating'] / df['Staked']
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y %H:%M:%S")
df['Date'] = df['Date'].apply(lambda x: (x - datetime.datetime(1970, 1, 1)).total_seconds())
df['hours-elapsed'] = (df['Date'] - df['Date'][0]) / 3600
group1.append('Circulating/Issued')
group1.append('Staked/Issued')
group1.append('Circulating/Staked')
last_row = df.iloc[-1]

# Plot group 1
for i in group1[3:]:
    plt.figure()
    plt.scatter(x=df['hours-elapsed'], y=df[i])
    plt.xlabel('hours elapsed')
    plt.ylabel(i)
    linear_regression(i)

# Plot group 2
#fig, ax = plt.subplots()
#ax.plot(df['hours-elapsed'], df['Circulating/Issued'], label='Circulating/Issued')
#ax.plot(df['hours-elapsed'], df['Staked/Issued'], label='Staked/Issued')
#ax.plot(df['hours-elapsed'], df['Circulating/Staked'], label='Circulating/Staked')
#ax.set(xlabel='Time (h)', ylabel='Proportion',
#       title='Ratios over time')
#plt.legend(loc='right', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
#ax.grid()

# Predict Staked/Issued
x = np.array(df['hours-elapsed']).reshape((-1, 1))
y = np.array(df['Staked/Issued']).reshape((-1, 1))
model = LinearRegression().fit(x, y)
print('Current Staked/Issued:', last_row['Staked/Issued'])
print('Time to reach 50% staked:', ((0.5 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')
print('Time to reach 75% staked:', ((0.75 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')
print('Time to reach 100% staked:', ((1 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')

# Predict Staked/Issued
x = np.array(df['hours-elapsed']).reshape((-1, 1))
y = np.array(df['Circulating/Staked']).reshape((-1, 1))
model = LinearRegression().fit(x, y)
print('__________________________________________________________________________________________________')
print('Current Circulating/Staked:', last_row['Circulating/Staked'])
print('Time to reach 10% circulating:', ((0.1 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')
print('Time to reach 5% circulating:', ((0.05 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')
print('Time to reach 0% circulating:', ((0 - float(model.intercept_)) / float(model.coef_)) / 24, 'days')
print('__________________________________________________________________________________________________')

# Plot group 2
plt.show()
