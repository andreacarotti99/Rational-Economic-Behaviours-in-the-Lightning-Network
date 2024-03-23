import pandas as pd

# these must be substituted with the path to final_data for different alfas
path_alfa01 = ""
path_alfa0001 = ""
path_alfa0 = ""

path_bc_gammas = "/src/replicate_strategy_game/HBC/bc_gammas.csv"

df_alfa01 = pd.read_csv(path_alfa01)
df_alfa0001 = pd.read_csv(path_alfa0001)
df_bc_gammas = pd.read_csv(path_bc_gammas)
df_alfa0 = pd.read_csv(path_alfa0)

df_alfa01 = pd.merge(df_alfa01, df_bc_gammas, on='node')
df_alfa0001 = pd.merge(df_alfa0001, df_bc_gammas, on='node')
df_alfa0 = pd.merge(df_alfa0, df_bc_gammas, on='node')

print(df_alfa01)

# print(df_alfa0001)
corr_coeff_1 = df_alfa01['bc_gamma_0.0'].corr(df_alfa01['total_fee'])
corr_coeff_2 = df_alfa01['bc_gamma_0.2'].corr(df_alfa01['total_fee'])
corr_coeff_3 = df_alfa01['bc_gamma_0.6'].corr(df_alfa01['total_fee'])
corr_coeff_4 = df_alfa01['bc_gamma_0.8'].corr(df_alfa01['total_fee'])
corr_coeff_5 = df_alfa01['bc_gamma_1.0'].corr(df_alfa01['total_fee'])

print(corr_coeff_1)
print(corr_coeff_2)
print(corr_coeff_3)
print(corr_coeff_4)
print(corr_coeff_5)

corr_coeff_1 = df_alfa0001['bc_gamma_0.0'].corr(df_alfa0001['total_fee'])
corr_coeff_2 = df_alfa0001['bc_gamma_0.2'].corr(df_alfa0001['total_fee'])
corr_coeff_3 = df_alfa0001['bc_gamma_0.6'].corr(df_alfa0001['total_fee'])
corr_coeff_4 = df_alfa0001['bc_gamma_0.8'].corr(df_alfa0001['total_fee'])
corr_coeff_5 = df_alfa0001['bc_gamma_1.0'].corr(df_alfa0001['total_fee'])
corr_coeff_6 = df_alfa0001['bc_fee'].corr(df_alfa0001['total_fee'])

print()
print(corr_coeff_1)
print(corr_coeff_2)
print(corr_coeff_3)
print(corr_coeff_4)
print(corr_coeff_5)
print(corr_coeff_6)

corr_coef = df_alfa0['bc_fee'].corr(df_alfa0['total_fee'])

df_alfa0.to_csv('test.csv')
print()
print(corr_coef)
