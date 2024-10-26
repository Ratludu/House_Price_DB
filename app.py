from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio

df = pd.read_csv("all_perth_310121.csv")

df["POSTCODE"] = df["POSTCODE"].apply(str)


app = Dash(__name__)

#########################################################################################################################
# Map visual

map_fig = px.scatter_map(df, lat = "LATITUDE", lon = "LONGITUDE", color = "PRICE", template = "plotly_dark")

map_fig.update_layout(paper_bgcolor = "#222")

map_fig.update_layout(
        margin={'t':0,'l':0,'b':0,'r':0}
    )

#########################################################################################################################
# bar chart

bar_fig = px.histogram(df, x = "BUILD_YEAR", y = "PRICE", template=  "plotly_dark")

bar_fig.update_layout(
    margin={'t':0,'l':0,'b':0,'r':25},
    # font_color = "white",
    xaxis_title = "Build Year",
    yaxis_title = "Price",
    paper_bgcolor = "#222",
    plot_bgcolor = "#222"
)

#########################################################################################################################
# Something else

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("House Prices in Perth", style={"textAlign": "left"})
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Placeholder for slicers")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=map_fig, id="controls-and-graph")
        ], width = 6),

        dbc.Col([
            dcc.Graph(figure=bar_fig, id = "bar_graph")
        ], width = 6)
    ])
])



if __name__ == "__main__":
    app.run_server(debug=True)