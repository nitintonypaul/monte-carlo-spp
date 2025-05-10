# Monte Carlo Simulation for predicting Stock Prices

---

### What is Monte Carlo Simulation?

**Monte Carlo Simulation** is a process by taking random events and generating a huge number of outcomes. In each case the outcome is stored in an array, or technically any method of reaccessible storage, and the average of all the outcomes is computed. This would be the predicted outcome of the random event. Monte Carlo Simulations are generally used in random events having more than just a few outcomes, unlike tossing a coin. For example, predicting the next stock price in the given time frame.

### What are we doing here?
Even though Monte Carlo is generally carried out by taking random outcomes of an event, that is not what this program does. Taking past share prices, grouping them into a data structure and finding their average may not seem fitting as the upcoming prices are not **directly** dependent on past prices. Instead we use a mathematical formula designed for dynamic optimization in randomness. The **Geometric Brownian Motion**.

### Geometric Brownian Motion
Here, we utilize GBM to predict the share price of the next time slot for a given time period.
The Geometric Brownian Motion we use is of the form

$$
S_t = S_0 e^{(\mu - 0.5 \sigma^2)t + \sigma W_t}
$$

Here:

$$S_t$$ = the predicited price

$$S_0$$ = the current price

$$e$$ = Euler's number

$$\mu$$ = Drift 

$$\sigma$$ = Volatility

$$t$$ = Time period in terms of trading days

$$W_t$$ = Wiener process

For the GBM we use in this Monte Carlo Simulation, we assume that $$\mu$$ and $$\sigma$$ (Drift and Volatility) remain **constant**. Whereas in reality, they are constantly fluctuating.

---

### Mathematical Explanation
I know, it looks confusing. But it's actually quite simple. What we are finding is $$S_t$$ which is the price which are predicting. It is predicted from $$S_0$$ (Price at the moment) multiplied with an expression. Let me break it down to you.

$$\sigma$$ denotes the **Volatility** or how wild the share price moves. A highly volatile share has a good chance of changing from a significantly low amount to something that's off the clouds and vice versa. An example is **GameStop** (GME) during 2021 when it went from around **$7** all the way up to an all time high of **$120.75**. 

$$\sigma$$ is computed by 

$$
\sigma = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (r_i - \bar{r})^2}
$$

where $$N$$ = number of data points used for observation 

$$r_i$$ is computed as:

$$
r_i = \ln\left(\frac{S_i}{S_{i-1}}\right)
$$

where $$S_i$$ and $${S_{i-1}}$$ are share prices of two consecutive days.

And finally, $$\bar{r}$$ is the mean of all $$r_i$$.


Now, $$\mu$$ denotes the **Drift** or the average return over a set period of time. It's based on historical data, just like $$\sigma$$. But since we assume both $$\mu$$ and $$\sigma$$ are constant throughout. We can compute $$\mu$$ by:

$$
\mu = \bar{r} - 0.5\sigma^2
$$


Where
$$\bar{r}$$ = mean of ($$r_i$$) and $$\sigma$$ = Volatility


And finally, $$W_t$$ is the **Wiener Process** which is randomly computed from a normal distribution (Here, between 0 and 1). It can be computed by:

$$
W_t = Z\sqrt{t}
$$

where $$t$$ is the **time in trading days** (i.e, if we are computing for a time period of one day, $$t=1/252$$ since there are 252 days in a trading year).

And, $$Z$$ is the random number selected from a normal distribution of 0 and 1.

For code convenience I've taken the equation as:

$$
S_t = S_0 e^{(\bar{r} - \sigma^2)t + \sigma W_t}
$$

Which is a simplified version of the original Geometric Brownian Motion for Monte Carlo Simulation.

---

### How do we use Monte Carlo Simulation here?
Very easy. We obtain the values of Drift ($$\mu$$), Volatility ($$\sigma$$) and Current Price ($$S_0$$) from an API (yfinance) and chuck the values into GBM for a desired $$t$$ while randomly selecting and computing $$W_t$$.
This process is repeated a huge number of times, while each time, the result $$S_t$$ is stored. Finally the average of all the values is obtained as the expected price after the desired time period $$t$$ from the start of the operation.

### PSEUDOCODE
Comments are given by ```#A Hashtag (This is a comment)```
```text
IMPORT dependencies (numpy, yfinance, math, datetime)

DECLARE function data_scrape(stock) #stock is a string
  COMPUTE stock as yf.Ticker(stock)
  FETCH data from stock.history(period="1y")
  FETCH prices from data["Close"]
  COMPUTE returns as np.log(prices / prices.shift(1)).dropna()
  FETCH mean from returns.mean()
  FETCH volatility from returns.std() #standard deviation
  RETURN mean and volatility as a tuple

FETCH stock from the user
FETCH data_today from yf.Ticker(stock).history(period="1d")
FETCH price from data_today["Close"].iloc[-1]   #Gets today's price
FETCH mean and volatility from data_scrape(stock)
FETCH date and time from datetime.now()

DECLARE price_sum, time, base_wt, iterations as 0, 1/252, (1/252) ** 0.5, 1000 respectively

#Simulate 1000 possible price paths using GBM
FOR an integer i from 0 to 1000:
  FETCH rand from np.random.normal(0,1)
  COMPUTE Wt = rand * base_wt
  COMPUTE St = price * (math.e ** ((mean - volatility ** 2) * time + volatility * Wt))
  INCREASE price_sum by St

FETCH expected_price from price_sum/iterations

PRINT stock
PRINT date, time and price
PRINT expected_price
```

---
