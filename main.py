#Monte Carlo Simulation to predict the next stock price

#Uses Geometric Brownian Motion to compute the next stock price within the given time frame
#This process is iterated many times and the average is taken to predict the next stock price

#Importing dependencies
import yfinance as yf
import numpy as np
import math
from datetime import datetime

#Function to obtain mean and volatility
def dataScrape(stock):

    #Convert into ticker symbol object
    stock = yf.Ticker(stock)

    #Finding data over a period of 1y
    data = stock.history(period="1y")
    prices = data["Close"]

    #Computing returns
    returns = np.log(prices / prices.shift(1)).dropna()

    #Computing Mean and volatility
    mean = returns.mean()
    volatility = returns.std()

    #Returning Mean and Volatility
    return (mean, volatility)

#Obtaining Stock name from the user (Ticker Symbol)
stock = input("Enter stock name: ")

#Fetching Price at the moment
dataToday = yf.Ticker(stock).history(period="1d")
price  = dataToday["Close"].iloc[-1]

#Obtaining mean and volatility from the function
mean, volatility = dataScrape(stock)

#Finding the date and time at the moment
currentDatetime = datetime.now()
formattedDatetime = currentDatetime.strftime("%H:%M:%S %d-%m-%Y")

#Declaring priceSum to store prices, time which is denoted in days/trading-days, basWt and iterations
priceSum = 0
time = 1/252
baseWt = (time)**0.5
iterations = 1000

#Carrying out the MCS by for loop for 'iterations' amount of times
for i in range(iterations):

    #Finding a random from standard deviation
    rand = np.random.normal(0,1)

    #Computing Wt
    Wt = rand*baseWt

    #Substituting in Geometric Brownian Motion
    St = price * (math.e ** ((mean - volatility**2)*time + volatility*Wt))

    #Adding to priceSum
    priceSum += St

#Obtaining expected price
expectedPrice = priceSum/iterations

#Printing result
print("=========================================================")
print(f"Stock chosen: {stock}")
print(f"Price as of {formattedDatetime} is {price}")
print(f"Price one day from {formattedDatetime} is expected to be: {expectedPrice}")
print("=========================================================")