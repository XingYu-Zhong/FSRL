

twoma_strategy = """
twoma_strategy:
This strategy is an automated trading script based on a double SMA crossover strategy designed to make buy or sell decisions by comparing the relative positions of short-term and long-term moving averages. Below is a detailed summary of the strategy:

### Strategy logic
1. **Initialization**: At the beginning of the strategy, set the strategy state to `IDLE` (idle), the number of buy and sell counts to zero, and initialize the trading environment through the `bao.init_strategy` method, which includes setting the initial cash, the start and end dates, and the list of stock codes.

2. **Execution strategy**:
    - The strategy calculates the 5- and 10-day moving averages (MA5 and MA10) of all target stocks at each step.
    - If MA5 is greater than MA10 and the stock is not currently held, it is considered a buy signal and the stock is purchased using equalized funds until the maximum purchase cash limit per stock is reached.
    - If MA5 is less than MA10 and the stock is currently held, it is considered a sell signal and the entire position is sold.
    - After a buy or sell operation, update the strategy status to `BUY` or `SELL`. If a sell operation is executed, the strategy status is reset to `IDLE` afterwards.

3. **Strategy termination conditions**:
    - The strategy ends if the set maximum number of sells or maximum number of strategy execution steps is reached.

4. **Strategy execution and result collection**:
    - Execute the strategy using the `bao.run_strategy` method, passing in the strategy function defined above.
    - At the end of execution, add a `strategy_name` column to the result DataFrame, labeled `twoma_strategy`.

### Features and caveats
- This strategy is simple to understand and is based on the classic technical analysis principle that short-term averages crossing long-term averages are the basis for buy and sell signals.
- The strategy splits the money equally into one investment amount per stock, which helps to diversify the risk.
- The strategy's buy and sell decisions are based solely on the relationship between MA5 and MA10, and do not take into account other factors that may affect the price of the stock, such as the market environment, company fundamentals, and so on.
- In practice, parameters need to be optimized, including choosing the appropriate moving average period and adjusting the maximum number of buy and sells and step limits to improve strategy performance.

"""
rsi_strategy="""
rsi_strategy:
This RSI strategy is based on the Relative Strength Index (RSI) to determine when to buy or sell a stock, and is suitable for investors who want to take advantage of market overbuying or over-selling when there is a significant change in price momentum. Below is a brief description of the strategy's execution logic:

### Strategy logic
1. **Initialization**: set the initial state to `IDLE`, the number of buys and sells to 0, and initialize the trading environment (including cash, date range, and stock list).
2. **RSI Calculation**:
    - Use 14 days as the RSI calculation period.
    - For each stock, obtain the last 20 days of closing price data.
    - Calculate the RSI value based on the average of the stock price increase or decrease.
3. **Trading Decision**:
    - **Sell Logic**: If the RSI value of a stock is greater than 70, it is considered an overbought, and if the stock is currently held, it is sold.
    - **Buy Logic**: If a stock's RSI value is less than 30, it is considered an oversell, and if the stock is not currently held, it is a buy.
4. **TRADE EXECUTION**: Execute buy and sell operations based on the above logic, using the maximum purchase cash limit allocated to each stock for buying.
5. **Strategy termination condition**: The strategy ends when the set maximum number of sells or maximum number of strategy execution steps is reached.

### Summary
This RSI strategy guides trading decisions by monitoring the market for overbought or oversold signals, and is suitable for investors seeking to profit from changes in momentum, especially when market price fluctuations are pronounced.

"""

bulin_strategy = """
bulin_strategy:
This Bollinger Bands Regression strategy is a trading strategy that guides buy and sell decisions based on the Bollinger Bands indicator, and is suitable for investors seeking to identify overbought or oversold signals during stock price fluctuations. Below is a brief description of the strategy's execution logic:
### Strategy logic
1. **Initialization**: set the initial state to `IDLE`, the number of buys and sells to 0, and initialize the trading environment (including cash, date range, and stock list).
2. **Bollinger Band Calculation**:
    - Calculate the upper (bollUpper) and lower (bollBottom) Bollinger bands using a 20-day moving average and standard deviation.
    - The standard deviation is multiplied by 2 (`std_range`) to determine the distance between the upper and lower rails and the middle rail.
3. **Trading decisions**:
    - **Sell Logic**: when the stock price crosses the upper Bollinger Band from below upwards, it is considered an overbought signal and is sold if the stock is currently held.
    - **Buy Logic**: when the stock price crosses the lower Bollinger Band from above and below, it is considered an excessive sell signal, buy if the stock is not currently held.
4. **TRADE EXECUTION**: Execution of buy and sell operations based on the above logic, using the maximum purchase cash limit allocated to each stock for buying.
5. **Strategy termination condition**: The strategy ends when the set maximum number of sells or maximum number of strategy execution steps is reached.

### Summary
The Bollinger Band Regression strategy utilizes the position of a stock's price relative to its volatility range to guide trading decisions, and is suitable for investors who wish to take advantage of overextended market sentiment when market prices are volatile.

"""

empty_strategy = """
empty_strategy:
This "Vacuum 20 Day Strategy" is an explicit investment strategy whose core objective is to sell all positions immediately at the beginning of the strategy and then remain in a short position until the end of the strategy. This strategy may be designed to avoid market uncertainty or the expectation that the market will fall, thus avoiding holding any stocks to minimize potential losses. Below is a brief description of the strategy's execution logic:

## Strategy Logic
Initialization: Initialize the trading environment, including setting up cash, date range and stock list.
First Step Execution:
In the first step of the strategy, all positions are sold immediately to achieve a short position.
Maintaining a short position:
The strategy does not perform any buying operations in all the next steps and remains in a short position until the end of the strategy execution.
Strategy end condition:
The strategy ends when the maximum number of steps of the strategy execution is reached (a 20-day period may be implied, but not explicitly stated).

## Summarization.
The "Vacuum 20 days strategy" may be suitable for investors who expect the market to fall or be extremely volatile in the short term, and who want to avoid risk by keeping their positions empty. The effectiveness of this strategy is highly dependent on the accuracy of the market forecast and the timing of the execution of the strategy. In the event that the market is expected to rise, this strategy may result in missed profit opportunities.
"""
vwap_strategy ="""
vwap_strategy:
This VWAP (Volume Weighted Average Price) strategy is a trading strategy that utilizes the VWAP indicator to guide buy and sell decisions and is designed to capture trading opportunities by comparing the current price of an individual stock to its VWAP value. The strategy is suitable for investors who wish to trade utilizing the price-volume relationship. Below is a brief description of the strategy's execution logic:

## Strategy Logic
Initialization: Set the initial status to IDLE, the number of buys and sells to 0, and initialize the trading environment (including cash, date range and stock list).
VWAP Calculation:
For each stock, obtain the closing price and volume data for the last 20 days.
Use this data to calculate the VWAP value, i.e., multiply each day's closing price by the volume and divide by the total volume.
Trading Decision:
Sell Logic: If the current price is above the VWAP value and the stock is currently held, sell all positions.
Buy Logic: If the current price is below VWAP and the stock is not currently held, buy using available cash.
Trade Execution: Execute buy and sell operations based on the above logic, using the maximum purchase cash limit allocated to each stock.
Strategy termination condition: The strategy ends when the set maximum number of sells or maximum number of strategy execution steps is reached.

## Summary
The VWAP strategy guides buying and selling decisions by comparing a stock's current price to its volume-weighted average price, and is suitable for investors who wish to trade when the price deviates from its average trading price. This strategy is particularly suited to short-term and intraday traders to help them identify potential deviations in market prices and trade accordingly.
"""

two_bulin_rsi = "Description of the specific strategy:\n"+twoma_strategy+"\n"+bulin_strategy+"\n"+rsi_strategy

two_bulin_rsi_empty_vwap = "Description of the specific strategy:\n"+twoma_strategy+"\n"+bulin_strategy+"\n"+rsi_strategy+"\n"+empty_strategy+"\n"+vwap_strategy