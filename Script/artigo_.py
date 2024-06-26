import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import prophet
import sklearn
import openpyxl
from prophet.diagnostics import cross_validation
from prophet import Prophet
from sklearn import metrics

df0 = pd.read_excel('volume_tratado_corte_mes.xlsx')
df0

df1 = df0[['data','volume']]
df1 = df0[['data', 'volume']].rename(columns={'data': 'ds', 'volume': 'y'})
df1

df1_2 = df1
df1_2['ds'] = pd.to_datetime(df1_2['ds'], format="%d/%m/%Y %H:%M:%S")
df1_2

df2 = df1_2
df2.set_index('ds', inplace=True)

df_hora_000 = df2.resample('h').sum()

summary2 = df_hora_000.describe(include='all')
print(summary2)

df_hora_001 = df_hora_000.loc[df_hora_000['y'] <= 4000]
df_hora_002 = df_hora_001.loc[df_hora_001['y'] >= 2500]
df_hora = df_hora_002

df_hora.reset_index(inplace=True)

df_hora

# Defino dataset de teste e treino
df_hora_treino = df_hora.iloc[:-767]
df_hora_teste = df_hora.iloc[-767:]

df_hora

df_hora_treino

df_hora_teste

modelo_A = Prophet(growth='linear', seasonality_mode='additive')
modelo_A.fit(df_hora_treino)

futuro_A = modelo_A.make_future_dataframe(periods=801, freq='1H')

previsao_A = modelo_A.predict(futuro_A)

mae_A = metrics.mean_absolute_error(df_hora_teste['y'].values, previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
rmse_A = metrics.mean_squared_error(df_hora_teste['y'].values, previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values, squared=False)
mape_A = np.mean(np.abs((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
ppe_A = np.mean((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values) * 100
bias_A = np.mean(df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
mapd_A = np.mean(np.abs((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
mdape_A = np.median(np.abs((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
r_squared_A = metrics.r2_score(df_hora_teste['y'].values, previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
smape_A = np.mean(2 * np.abs(df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / (np.abs(df_hora_teste['y'].values) + np.abs(previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values))) * 100
pmse_A = np.mean(np.square((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
mmape_A = np.mean(np.abs((df_hora_teste['y'].values - previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / (df_hora_teste['y'].values + previsao_A.loc[previsao_A['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / 2)) * 100

print('Modelo A:')
print('MAE: {}'.format(mae_A))
print('RMSE: {}'.format(rmse_A))
print('MAPE: {}%'.format(mape_A))
print('PPE: {}%'.format(ppe_A))
print('Bias: {}'.format(bias_A))
print('MAPD: {}%'.format(mapd_A))
print('MdAPE: {}%'.format(mdape_A))
print('R-squared: {}'.format(r_squared_A))
print('SMAPE: {}%'.format(smape_A))
print('PMSE: {}%'.format(pmse_A))
print('MMAPE: {}%'.format(mmape_A))

modelo_B = Prophet(growth='linear', seasonality_mode='multiplicative')
modelo_B.fit(df_hora_treino)

futuro_B = modelo_B.make_future_dataframe(periods=801, freq='1H')

previsao_B = modelo_B.predict(futuro_B)

mae_B = metrics.mean_absolute_error(df_hora_teste['y'].values, previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
rmse_B = metrics.mean_squared_error(df_hora_teste['y'].values, previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values, squared=False)
mape_B = np.mean(np.abs((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
ppe_B = np.mean((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values) * 100
bias_B = np.mean(df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
mapd_B = np.mean(np.abs((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
mdape_B = np.median(np.abs((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
r_squared_B = metrics.r2_score(df_hora_teste['y'].values, previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values)
smape_B = np.mean(2 * np.abs(df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / (np.abs(df_hora_teste['y'].values) + np.abs(previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values))) * 100
pmse_B = np.mean(np.square((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / df_hora_teste['y'].values)) * 100
mmape_B = np.mean(np.abs((df_hora_teste['y'].values - previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / (df_hora_teste['y'].values + previsao_B.loc[previsao_B['ds'].isin(df_hora_teste['ds']), 'yhat'].values) / 2)) * 100

print('Modelo B:')
print('MAE: {}'.format(mae_B))
print('RMSE: {}'.format(rmse_B))
print('MAPE: {}%'.format(mape_B))
print('PPE: {}%'.format(ppe_B))
print('Bias: {}'.format(bias_B))
print('MAPD: {}%'.format(mapd_B))
print('MdAPE: {}%'.format(mdape_B))
print('R-squared: {}'.format(r_squared_B))
print('SMAPE: {}%'.format(smape_B))
print('PMSE: {}%'.format(pmse_B))
print('MMAPE: {}%'.format(mmape_B))

df_hora_teste [['ds', 'y']]
previsao_A [['ds', 'yhat']]
previsao_B [['ds', 'yhat']]

previsao_B['yhat'] = previsao_B['yhat'].round(1)
previsao_A['yhat'] = previsao_A['yhat'].round(1)

previsao_A.rename(columns={'yhat': 'yhat_PROPHET_A'}, inplace=True)
previsao_B.rename(columns={'yhat': 'yhat_PROPHET_B'}, inplace=True)

resultado_merge = df_hora_teste.merge(previsao_A[['ds', 'yhat_PROPHET_A']], on='ds', how='left')
resultado_merge = resultado_merge.merge(previsao_B[['ds', 'yhat_PROPHET_B']], on='ds', how='left')

print(resultado_merge)

metricas_arredondadas = {
    'MAE': [round(mae_A, 2), round(mae_B, 2)],
    'RMSE': [round(rmse_A, 2), round(rmse_B, 2)],
    'MAPE (%)': [round(mape_A, 2), round(mape_B, 2)],
    'PPE (%)': [round(ppe_A, 2), round(ppe_B, 2)],
    'Bias': [round(bias_A, 2), round(bias_B, 2)],
    'MAPD (%)': [round(mapd_A, 2), round(mapd_B, 2)],
    'MdAPE (%)': [round(mdape_A, 2), round(mdape_B, 2)],
    'R-squared': [round(r_squared_A, 2), round(r_squared_B, 2)],
    'SMAPE (%)': [round(smape_A, 2), round(smape_B, 2)],
    'PMSE (%)': [round(pmse_A, 2), round(pmse_B, 2)],
    'MMAPE (%)': [round(mmape_A, 2), round(mmape_B, 2)]
}

tabela_metricas_arredondadas = pd.DataFrame(metricas_arredondadas, index=['Modelo A', 'Modelo B'])

tabela_metricas_pivot = tabela_metricas_arredondadas.transpose()

print(tabela_metricas_pivot)

df_hora.set_index('ds')['y'].plot(color='blue')
previsao_A.set_index('ds')['yhat_PROPHET_A'].plot(color='red')

df_hora.set_index('ds')['y'].plot(color='blue')
previsao_B.set_index('ds')['yhat_PROPHET_B'].plot(color='red')
