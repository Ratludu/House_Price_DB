from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio


df = pd.read_csv("all_perth_310121.csv")

df["POSTCODE"] = df["POSTCODE"].apply(str)

df.sort_values(by = ["BUILD_YEAR"], inplace=True)

app = Dash(__name__)
server = app.server

#########################################################################################################################
# map chart

def map_graph(df):
    map_fig = px.scatter_map(df, lat = "LATITUDE", lon = "LONGITUDE", color = "PRICE", template = "plotly_dark")

    map_fig.update_layout(paper_bgcolor = "#222")

    map_fig.update_layout(

    margin={'t':0,'l':0,'b':0,'r':0}
    )

    return map_fig


#########################################################################################################################
# bar chart

def bar_graph(df):
    bar_fig = px.histogram(df, x = "BUILD_YEAR", y = "PRICE", template=  "plotly_dark")

    bar_fig.update_layout(
        margin={'t':0,'l':0,'b':0,'r':25},
        # font_color = "white",
        xaxis_title = "Build Year",
        yaxis_title = "Price",
        paper_bgcolor = "#222",
        plot_bgcolor = "#222"
    )

    return bar_fig

#########################################################################################################################
# Line chart

def line_graph(df):
    line_fig = px.line(df, x = "BUILD_YEAR", y = "PRICE", color = "BEDROOMS",template="plotly_dark")

    line_fig.update_layout(
        margin={'t':25,'l':25,'b':25,'r':25},
        xaxis_title = "Build Year",
        yaxis_title = "Price",
        paper_bgcolor = "#222",
        plot_bgcolor = "#222"
    )

    return line_fig



app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("House Prices in Perth 🏠", style={"textAlign": "left"})
        ], width=12)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "Suburb_dropdown",
                className="dropdown-item",
                options=df["SUBURB"].unique(),
                placeholder= "Please select suburb",
                style = {"color": "black"}
            )
        ], width = 2),
        dbc.Col([
            dcc.Dropdown(
                id = "Bedroom_dropdown",
                className="dropdown-item",
                options=df["BEDROOMS"].sort_values().unique(),
                placeholder= "Please select bedrooms",
                style = {"color": "black"}
            )
        ], width = 2),
        dbc.Col([
            dcc.Dropdown(
                id = "Bathroom_dropdown",
                className="dropdown-item",
                options=df["BATHROOMS"].unique(),
                placeholder= "Please select bathrooms",
                style = {"color": "black"}
            )
        ], width = 2)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id="map_graph")
        ], width = 6),

        dbc.Col([
            dcc.Graph(figure={}, id = "bar_graph")
        ], width = 6)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id="line_graph")
        ])
    ])

])

@callback(
    Output("map_graph", "figure"),
    Output("bar_graph", "figure"),
    Output("line_graph", "figure"),
    Input("Suburb_dropdown", "value"),
    Input("Bedroom_dropdown", "value"),
    Input("Bathroom_dropdown", "value")
)

def update_map_graph(suburb, bedroom, bathroom):

    if suburb is None:
        filter_suburb = list(df["SUBURB"].unique())
    else:
        filter_suburb = [suburb]

    if bedroom is None:
        filter_bedroom = df["BEDROOMS"].unique()
    else:
        filter_bedroom = [bedroom]
    if bathroom is None:
        filter_bathroom = df["BATHROOMS"].unique()
    else:
        filter_bathroom = [bathroom]
    

    filtered_df = df[df["SUBURB"].isin(filter_suburb) & df["BEDROOMS"].isin(filter_bedroom) & df["BATHROOMS"].isin(filter_bathroom)]
    

    map_fig = map_graph(filtered_df)
    bar_fig = bar_graph(filtered_df)
    line_fig = line_graph(filtered_df)


    return map_fig, bar_fig, line_fig



if __name__ == "__main__":
    app.run(debug=True)