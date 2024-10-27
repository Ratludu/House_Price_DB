from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio

df = pd.read_csv("all_perth_310121.csv")

df["POSTCODE"] = df["POSTCODE"].apply(str)

df.sort_values(by = ["BUILD_YEAR"], inplace=True)

df["BUILD_YEAR"] = df["BUILD_YEAR"].apply(int)

print(df.groupby(['BUILD_YEAR']).mean(numeric_only=True).reset_index().head())