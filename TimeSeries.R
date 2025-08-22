install.packages("TSA")
library(TSA)

data(JJ)
plot(JJ, type="o", ylab="Quarterly Earnings per Share")

## MOVING AVAREGE
w <- rnorm(500, mean = 0, sd = 1)
v <- filter(w, sides = 2, rep(1/3, 3))
par(mfrow = c(2, 1), mar = c(4, 4, 2, 1))  # bottom, left, top, right
plot.ts(w, main = "White Noise")
plot.ts(v, main = "Moving Average")

