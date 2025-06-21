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

Data_lm_Model <- Data_Price[, c(
  "LATITUDE", "LONGITUDE", "LOCALITY", "STATE", 
  "PROPERTYSQFT", "BEDS", "BATH", "PRICE"
)]

sapply(Data_lm_Model, function(x) sum(is.na(x)))

# LATITUDE    LONGITUDE 
#   0            0 
# LOCALITY      STATE 
#   0            0 
# PROPERTYSQFT  BEDS 
#   0            0 
#   BATH        PRICE 
#   0            0 


# We have preferred removing the 231 cases which correspond to missing
# values in StreetHouseFront. Na.omit function will remove the missing cases.
# Data_lm_Model <-na.omit(Data_lm_Model)
# rownames(Data_lm_Model) <-NULL

# transofrmando variáveis categóricas em numéricas
Data_lm_Model$LOCALITY <- factor(Data_lm_Model$LOCALITY)
Data_lm_Model$STATE <- factor(Data_lm_Model$STATE)

fitted_model_multiple <- lm(
  PRICE ~ LATITUDE + LONGITUDE + LOCALITY + STATE + BATH + BEDS + PROPERTYSQFT,
  data = Data_lm_Model
)
summary(fitted_model_multiple)


# Gerar data.frame com ID fictício se não houver coluna HOUSE_ID
Data_lm_Model$ID <- seq_len(nrow(Data_lm_Model))

# Criar data.frame com colunas: ID, Observado (PRICE), Predito (modelo)
actual_predicted <- as.data.frame(cbind(
  ID = as.numeric(Data_lm_Model$ID),
  Actual = as.numeric(Data_lm_Model$PRICE),
  Predicted = as.numeric(fitted(fitted_model_multiple))
))
head(actual_predicted)


plot(
  actual_predicted$Actual,
  actual_predicted$Predicted,
  xlab = "Preço Real",
  ylab = "Preço Previsto",
  main = "Preço Real vs. Previsto",
  pch = 19,
  col = "green"
)
abline(0, 1, col = "red", lwd = 2)

library(ggplot2)
library(tidyr)

# Corrigir e organizar os dados com coluna "HouseNumber" para o eixo x
actual_predicted$HouseNumber <- 1:nrow(actual_predicted)

long_data <- pivot_longer(
  actual_predicted,
  cols = c("Actual", "Predicted"),
  names_to = "Series",
  values_to = "Price"
)

# Plotando
ggplot(long_data, aes(x = HouseNumber, y = Price, color = Series)) +
  geom_line() +
  labs(
    x = "House Number",
    y = "House Sale Price",
    title = "Actual vs Predicted House Prices"
  ) +
  theme_minimal()


install.packages("car")
library(car)

# Cook's D plot
# identify D values > 4/(n-k-1)
cutoff <-4/((nrow(Data_lm_Model)-length(fitted_model_multiple$coefficients)-2))
plot(fitted_model_multiple, which=4, cook.levels=cutoff)
## 2 1076 2147

# Influence Plot
influencePlot(fitted_model_multiple, id.method="identify",
              main="Influence Plot", sub="Circle size is proportional to Cook's Distance", id.location =FALSE)

# Outlier Plot
outlierTest(fitted_model_multiple)


# Model DEBUG (observed data)
print("Dados observados: ")
Debug <- Data_lm_Model[c(2, 1076, 2147), ]
Debug

#      LATITUDE LONGITUDE  LOCALITY  STATE                       PROPERTYSQFT  BEDS  BATH        PRICE
#2    40.76639 -73.98099   New York  New York, NY 10019          17545.000     7     10.000000   195000000
#1076 40.77564 -73.96425   New York  County Manhattan, NY 10075  2184.208      8     8.0000000   60000000
#2147 40.73527 -73.85665   New York  Queens, NY 11374            55300.000     3     2.373861    5827000

print("Dados fitted: ")
fitted_model_multiple$fitted.values[c(342,621,1023)]
#  342        621       1023 
#  4445747.7  824645.3  1589348.4 

print("Summary of Observed values: ")
summary(Debug)












