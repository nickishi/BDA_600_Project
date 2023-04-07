install.packages("fBasics")
install.packages("lmtest")
install.packages('tseries')
install.packages('astsa')
install.packages('TSA')
library(fBasics) # Load the package fBasics.
library(tseries)
library(astsa)
library(lmtest)
library(TSA)

setwd("~/Desktop/PersonalProjects_Github/BDA_600_Project")
data <- read.csv('cumulative_weekly_returns.csv')
data$X = as.Date(data$X, tryFormat = "%Y-%m-%d")
head(data)

plot(data$X, data$layoff_group, type = 'l', xlab = 'Time', ylab = 'Return', main = 'Cumulative Return of Layoff Group 2020 - 2022')
plot(data$X, data$no_layoff_group, type = 'l', xlab = 'Time', ylab = 'Return', main = 'Cumulative Return of NoLayoff Group 2020 - 2022')

n = dim(data)[1]
dates = as.Date(data$X[2:n], tryFormat = "%Y-%m-%d")
layoff_data = data$layoff_group
no_layoff_data = data$no_layoff_group

# log to make stationary
logx1 = log(layoff_data)
dlogx1 = diff(logx1)

plot(dates, dlogx1, type='l')
adf.test(dlogx1) # P < .05, REGECT H0. data is stationary

par(mfrow = c(2, 1))
acf(dlogx1) # white noise :-(
pacf(dlogx1) # white noise :-(
eacf(dlogx1)
par(mfrow = c(1, 1))
