Machine Learning Engineer Nanodegree
Capstone Proposal
Partha Deka
February 13th, 2017
Domain Background
I have chosen the Investment and Trading Capstone project provided as one of the options. I wanted to use my Machine Learning knowledge to solve a real problem and where I can learn the domain too. I have always been interested in investment and trading as an amateur and now I want to use my machine learning knowledge and see if it could help in predicting stock prices in the short-term future.  I extensively took help of the free courses – “Machine learning for Trading” and “Time Series Forecasting” for this Capstone Project. 
Problem Statement
Build machine learning models that learn from historical stock price attributes and predict the stock price on a future date (any day after the last training date), I am only predicting the Adjusted Closing pricing. 
Building few models such as Linear Regression, KNN Regression which learn from historical stock data, attributes such as: Open, High, Low, Close, Volume, Adjusted Closing and “Adjusted Closing price” n days ahead in future. After the model is built on the historical data, it would predict the Adjusted Closing price for a date (only one date) which is n days ahead in future from the last date of training. Please note splitting the datasets has to be done in the ascending order of dates manually, and not using the SKLEARN test train split module which randomly split the data. In the stock price prediction world, we must not train a model on future datasets and try to predict the stock prices for past dates (Source - “Machine learning for Trading” Udacity course)
I am also using Non-seasonal ARIMA (model for Time series prediction) based model. This model is based on three terms: AR –Autoregressive - P, I – differencing - d, MA – Moving Average - q.  Parameters p, d, and q are non-negative integers, p is the order (number of time lags) of the autoregressive model, d is the degree of differencing (the number of times the data have had past values subtracted), and q is the order of the moving-average model. Three items should be considered to determine a first guess at an ARIMA model: a time series plot of the data, the ACF, and the PACF. 
AR model: Identification of an AR model is often best done with the PACF. the theoretical PACF “shuts off” past the order of the model.  The phrase “shuts off” means that in theory the partial autocorrelations are equal to 0 beyond that point
MA model: For an MA model, the theoretical PACF does not shut off, but instead tapers toward 0 in some manner.  A clearer pattern for an MA model is in the ACF.  The ACF will have non-zero autocorrelations only at lags involved in the model.
Sample PACF for an AR model below where the PACF shuts off past the 1st order so, AR =1 in this case:
 


Sample ACF for a MA model below where MA =1 
 

Udacity Free Course: Time Series Forecasting
https://onlinecourses.science.psu.edu/stat510/node/62
https://onlinecourses.science.psu.edu/stat510/node/49
https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average
http://www.inertia7.com/projects/time-series-stock-market-python


Datasets and Inputs
I have downloaded daily historical stocks data from Yahoo Finance between 12-05-2011 and 12-02-2016 for the following stocks along with SNP 500(American Market index, I want to see how these stock trend with respect to market trends explained by SNP 500). Also, please note that ‘Facebook’ went public around 2013 timeframe, so we have don’t data for ‘Facebook’ prior to that:
'AAPL', 'GOOG', 'AMZN', 'FACEBOOK', 'GE', 'GLD', 'MICROSOFT'
 Each of this stock has the following attributes:
 Open, High, Low, Close, Volume, Adj Close and Date
Solution Statement
The solution would be to build a Python based machine learning regression model for each stock provided by the user, where each model learns from the historical data of the stock between user provided start date and end date, and predicts the ‘Adj Close’ price for the user provided future date which must be greater than the end date. The data between the user provided ‘Start date’ and ‘End date’ would be divided into two parts in the ascending order of the dates, first 70% would be kept for training and the rest 30% for testing. The machine learning regression model must have a R2 score of 0.85 or above on the trained dataset and R2 score of 0.6 and above on the test dataset. Additionally, on an average the predicted prices from all the models must be more or less within +/- 5% of the actual stock prices on the test dataset.
Benchmark Model
The benchmark scores for the models: R2 Score of 0.6 on test data (unseen data) and a R2 Score of 0.85 on train data.  Additionally, on an average the predicted prices for all the models must be more or less within +/- 5% of the actual stock prices.

Evaluation Metrics
R2 score on the train and test datasets are calculated to measure the performance of the model. Best possible score is 1. Besides R2 score, I am also calculating the variation of the predicted stock price compared to the actual prices in the test dataset. R2 Score is used to test the performance of all three models – Linear Regression, KNN Regression and ARIMA

For e.g.: 
Score on training data for GOOG:0.97
Score on test data for GOOG: 0.88
The prediction on the test dataset 6 days after the training date for GOOG is +/- 2.721% compared to the actual values

In statistics, the coefficient of determination, denoted R2 or r2 and pronounced "R squared", is a number that indicates the proportion of the variance in the dependent variable that is predictable from the independent variable. The coefficient R^2 is defined as (1 - u/v), where u is the regression sum of squares ((y_true - y_pred) ** 2). sum () and v is the residual sum of squares ((y_true - y_true. mean ()) ** 2). sum (). Best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse). A constant model that always predicts the expected value of y, disregarding the input features, would get a R^2 score of 0.0.

Source: 
http://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html

http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression.score

https://en.wikipedia.org/wiki/Coefficient_of_determination

Project Design:
I would start-off with various financial analysis of the historical data such as plotting a comparative analysis of the various stocks prices, plotting the normalized stock prices, plotting daily returns, plotting Bollinger bands, calculating cumulative returns, creating portfolio stocks, plotting portfolio statistics, Optimizing the Portfolio by optimizing the Sharpe ratio, scatter plots. Also, co-relation between my portfolio daily return and SNP_500 daily return, Beta value to see how reactive is my optimized portfolio compared to the market, alpha value to see how well it performs compared to the market.

The next part would be to build machine learning models to predict ‘Adj Close’ price for a future date as discussed above. Please note that the reason for doing the financial analysis on the historical is to kind of depict that we can do the same analysis on the Predicted Stock prices. Although the goal of this project is just to predict the ‘Adj Close’ price for a stock for a particular future, to build a real investment strategy we need to perform financial perform analysis on the predicted stocks such as maintaining an optimized portfolio.

Here are Steps I would follow:

1. Plot data¶
    -plot selected data
    -normalize data
    -Rolling mean
    -rolling standard deviation
    -Bollinger bands
    -daily return

2. Analysis:
    -Cumulative return
    -creating portfolio
    -plotting portfolio statistic

3. Optimizing the Portfolio by optimizing or minimizing the negative sharpe ratio

4. plotting optimal portfolio statistics

5. Scatter plot, co-relation between my portfolio daily return and SNP_500 daily return, Beta value to see how
    reactive is my optimized portfolio compared to the market, alpha value to see how well it performs compared to     the market         

6. Plotting histograms

7. Stock price prediction interface – Linear Regression

8. Stock price prediction interface – KNN regression

9. Stock price prediction: ARIMA

Please take my code checked into github: https://github.com/ParthaPritamDeka/Machine_Learning/blob/master/Capstone Project/Machine_learning_for_Trading/Project/Submission/All_Analysis.ipynb


