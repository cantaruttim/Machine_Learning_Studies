import pandas as pd

Data_House = pd.read_csv("/content/NY-House-Dataset.csv", sep=",")
Data_House.head()

"""## Simple Linear Regression"""

from sklearn.linear_model import LinearRegression
import numpy as np

X = Data_House.iloc[:, 5].to_numpy()
X = X.reshape(-1, 1)
y = Data_House.iloc[:, 4].to_numpy()
y = y.reshape(-1, 1)

reg = LinearRegression().fit(X, y)

print(f"O Score do modelo é: {reg.score(X, y)}")
print(f"O coeficiente é: {reg.coef_}")
print(f"O valor do intercept é: {reg.intercept_}")
print(f"O valor do intercept é: {reg.intercept_}")


r_squared = reg.score(X, y)
r = np.sqrt(r_squared)

print(f"Coeficiente de correlação (r): {r}")

if reg.coef_[0][0] < 0:
    r *= -1

print(f"Coeficiente de correlação com sinal (r): {r}")

def plot(X, y):
  import matplotlib.pyplot as plt
  import seaborn as sns

  y_pred = reg.predict(X)

  # Create a scatter plot of observed vs predicted values
  plt.figure(figsize=(10, 6))
  sns.scatterplot(x=X.flatten(), y=y.flatten(), label='Observado')
  sns.scatterplot(x=X.flatten(), y=y_pred.flatten(), label='Previsto')

  plt.plot(X.flatten(), y_pred.flatten(), color='red', linewidth=2, label='Reta de Regressão')

  formula = f'y = {reg.intercept_[0]:.4f} + {reg.coef_[0][0]:.4f}x'
  plt.text(X.min(), y_pred.max(), formula, fontsize=12, color='blue')


  plt.xlabel('X')
  plt.ylabel('y')
  plt.title('Observado vs Previsto com Reta de Regressão')
  plt.legend()
  plt.grid(True)
  return plt.show()

plt = plot(X, y)
plt
