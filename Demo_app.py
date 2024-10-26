from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv("all_perth_310121.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("House Prices in Perth"),
        dcc.Graph(id="graph"),
        dcc.Dropdown(
            id = "type",
            options = [1,2,3,4],
            value = 1,
            multi = True,

        ),
    ])


@app.callback(
    Output("graph", "figure"),
    Input("type", "value")
)

def update_graph(type):

    filtered_df = df[df["BEDROOMS"] == type]

    fig = px.scatter_mapbox(
        filtered_df,
        lon="LONGITUDE",
        lat="LATITUDE",
        color="PRICE",
        size="PRICE",
    )

    fig.update_layout(mapbox_style="open-street-map")
    

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)