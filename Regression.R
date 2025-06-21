Data_Price <- read.csv("data/NY-House-Dataset.csv", header=T)

y <- Data_Price$PRICE
x <- Data_Price$PROPERTYSQFT
# x <- as.numeric(as.factor(Data_Price$TYPE))

# valid_rows <- complete.cases(x, y)
# x <- x[valid_rows]
# y <- y[valid_rows]

plot(
  x, y,
  main = "Scatterplot HousePrice vs Store Area (sqrt)",
  xlab="House sqft", ylab="House Pricing",
  pch = 19, cex=0.3, col="darkred"
)
# relationship direction
abline(lm(y~x))
lines(lowess(x,y), col="green")

cat("The correlation among HousePrice and StoreArea is ", cor(x,y))
# 0.1108888


##### SIMPLE LINEAR REGRESSION #####

fitted_Model <-lm(y~x)
summary(fitted_Model)
# Y = -837809.4 + (1462.7)x

# how the model fits the actual value
res <-stack(data.frame(Observed = y, Predicted = fitted(fitted_Model)))
res <-cbind(res, x =rep(x, 2))

library("lattice")
xyplot(values ~x, data = res, group = ind, auto.key =TRUE)


##### MULTIPLE LINEAR REGRESSION #####
