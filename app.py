import pandas as pd
import numpy as np

file_name = "sao_paulo_raw.csv"
df = pd.read_csv(file_name, index_col="ID")

## Preprocess
# Price Cond
df['Price Condominio'].replace({'R\$ ': ''}, inplace=True, regex=True)
df['Price Condominio'].replace({'\.': ''}, inplace=True, regex=True)
df['Price By Month'].replace({'R\$ ': ''}, inplace=True, regex=True)
df['Price By Month'].replace({'\.': ''}, inplace=True, regex=True)

neighbourhoods = ["bela vista", "pinheiros", "vila olimpia"]
for neighbourhood in neighbourhoods:
    is_in_neighbourhood = df["Location"].str.lower().str.contains(neighbourhood)
    if not df[is_in_neighbourhood].empty:
        df = df[is_in_neighbourhood]

# print(df.head())

cond_price_limit = 500
is_less_than_limit = df["Price Condominio"].astype(int) <= cond_price_limit
if not df[is_less_than_limit].empty:
    df = df[is_less_than_limit]

is_furnished = df["Condominio Content"].str.lower().str.contains("mobiliado")
if not df[is_furnished].empty:
    df = df[is_furnished]

loc_price_limit = 2000
is_less_than_limit = df["Price By Month"].astype(int) <= loc_price_limit
if not df[is_less_than_limit].empty:
    df = df[is_less_than_limit]

df.to_csv('sao_paulo_searchcriteria.csv')
