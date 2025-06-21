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

import matplotlib.pyplot as plt
import statsmodels.api as sm

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

"""## Multiple Regression"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Carregar os dados
data = pd.read_csv("/content/NY-House-Dataset.csv", sep=",")

# Selecionar colunas relevantes
features = [
    "LATITUDE", "LONGITUDE", "LOCALITY", "STATE",
    "PROPERTYSQFT", "BEDS", "BATH", "PRICE"
]
data_model = data[features].copy()

# Verificar valores ausentes
print(data_model.isna().sum())

# Remover linhas com valores ausentes
data_model.dropna(inplace=True)
data_model.reset_index(drop=True, inplace=True)

# Codificar variáveis categóricas
label_enc_locality = LabelEncoder()
label_enc_state = LabelEncoder()

data_model["LOCALITY"] = label_enc_locality.fit_transform(data_model["LOCALITY"])
data_model["STATE"] = label_enc_state.fit_transform(data_model["STATE"])

# Separar variáveis independentes e dependente
X = data_model.drop(columns=["PRICE"])
y = data_model["PRICE"]

# Regressão linear múltipla
model = LinearRegression()
model.fit(X, y)

# Previsões
data_model["Predicted"] = model.predict(X)
data_model["Actual"] = y
data_model["HouseNumber"] = np.arange(1, len(data_model) + 1)

# Exibir os coeficientes
print("Coeficientes do modelo:")
for name, coef in zip(X.columns, model.coef_):
    print(f"{name}: {coef:.2f}")
print(f"Intercepto: {model.intercept_:.2f}")
print(f"R²: {model.score(X, y):.4f}")

# Criar DataFrame com valores reais vs preditos
actual_predicted = data_model[["HouseNumber", "Actual", "Predicted"]]

# Plot Real vs Predito
plt.figure(figsize=(10, 5))
sns.scatterplot(data=actual_predicted, x="Actual", y="Predicted", color="green", s=20)
plt.plot([actual_predicted["Actual"].min(), actual_predicted["Actual"].max()],
         [actual_predicted["Actual"].min(), actual_predicted["Actual"].max()],
         color="red", lw=2, linestyle="--", label="Linha ideal")
plt.xlabel("Preço Real")
plt.ylabel("Preço Previsto")
plt.title("Preço Real vs. Preço Previsto")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Dados longos para ggplot-like com seaborn
long_data = pd.melt(
    actual_predicted,
    id_vars="HouseNumber",
    value_vars=["Actual", "Predicted"],
    var_name="Series",
    value_name="Price"
)

# Plot tipo ggplot2 com seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=long_data, x="HouseNumber", y="Price", hue="Series")
plt.xlabel("House Number")
plt.ylabel("House Sale Price")
plt.title("Actual vs Predicted House Prices")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Real vs Predito
plt.figure(figsize=(10, 5))
sns.scatterplot(data=actual_predicted, x="Actual", y="Predicted", color="green", s=20)

# Adicionar a linha ideal (y=x)
plt.plot([actual_predicted["Actual"].min(), actual_predicted["Actual"].max()],
         [actual_predicted["Actual"].min(), actual_predicted["Actual"].max()],
         color="red", lw=2, linestyle="--", label="Linha ideal")

# Adicionar a linha do modelo
plt.plot(actual_predicted["Actual"], actual_predicted["Predicted"], color="blue", lw=.5, label="Linha do Modelo")

plt.xlabel("Preço Real")
plt.ylabel("Preço Previsto")
plt.title("Preço Real vs. Preço Previsto")
plt.legend()
plt.grid(True)

# Ajustar os limites dos eixos X e Y para melhor visualização
# Você pode ajustar esses valores manualmente ou dinamicamente
min_val = min(actual_predicted["Actual"].min(), actual_predicted["Predicted"].min()) * 0.9
max_val = max(actual_predicted["Actual"].max(), actual_predicted["Predicted"].max()) * 1.1

plt.xlim(min_val, max_val)
plt.ylim(min_val, max_val)

plt.tight_layout()
plt.show()

print(y)

print(X)
