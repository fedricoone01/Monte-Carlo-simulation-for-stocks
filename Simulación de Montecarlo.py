# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:37:05 2022

@author: Fede
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from pandas_datareader import data


#Select an asset
stock = data.DataReader('MELI', 'yahoo',start='1/1/2017')


#------ Calculate the data to feed the simulation ------
total_growth = (stock['Adj Close'][-1] / stock['Adj Close'][1])
total_days = (stock.index[-1] - stock.index[0]).days
number_of_years = total_days / 365.0

#Growth rate
compound_growth_rate = total_growth ** (1/number_of_years) - 1
print ("compound_growth_rate (mean returns) : ", str(round(compound_growth_rate,3)))
#Standard deviation
std_dev = stock['Adj Close'].pct_change().std()

#standard deviation annualization factor
number_of_trading_days = 252
std_dev = std_dev * math.sqrt(number_of_trading_days)
print ("std_dev (standard deviation of return : )", str(round(std_dev,3)))


#------ Run Monte Carlo simulation ------
#Execution with 1 random walk
daily_return_percentages = np.random.normal(compound_growth_rate/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),number_of_trading_days)+1
price_series = [stock['Adj Close'][-1]]

for j in daily_return_percentages:
    price_series.append(price_series[-1] * j)

plt.style.use('bmh')
plt.figure().suptitle("Random walk")
plt.plot(price_series)
plt.show()

#We increase the number of random walks
number_of_trials = 1000
closing_prices = []

for i in range(number_of_trials):
    #calculate randomized return percentages following our normal distribution and using the mean / std dev we calculated above
    daily_return_percentages = np.random.normal(compound_growth_rate/number_of_trading_days, std_dev/math.sqrt(number_of_trading_days),
    number_of_trading_days)+1
    price_series = [stock['Adj Close'][-1]]

    for j in daily_return_percentages:
        #extrapolate price out for next year
        price_series.append(price_series[-1] * j)

    #append closing prices in last day of window for histogram
    closing_prices.append(price_series[-1])
    #plot all random walks
    plt.plot(price_series)

plt.show()


#------ Analysis of results ------
#The most probable ending point
mean_end_price = round(np.mean(closing_prices),2)
print("\nExpected price in 1 year: USD", str(mean_end_price))

#lastly, we can split the distribution into percentiles to help us gauge risk vs. reward
#Pull top 10% of possible outcomes
top_ten = round(np.percentile(closing_prices,100-10),2)
#Pull bottom 10% of possible outcomes
bottom_ten = round(np.percentile(closing_prices,10),2)

#create histogram again
plt.hist(closing_prices,bins=80)
plt.axvline(top_ten,color='r',linestyle='dashed',linewidth=2)
plt.axvline(stock['Adj Close'][-1],color='black', linestyle='dashed',linewidth=2)
plt.axvline(bottom_ten,color='r',linestyle='dashed',linewidth=2)
plt.legend(["Bottom 10%","Actual price","Top 10%"])
plt.show()

print("\n There is a 10% chance that the price will fall below USD", str(bottom_ten))
print("\n There is a 10% chance that the price exceeds USD", str(top_ten))





