from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio
from model import price_prediction



df = pd.read_csv("all_perth_310121.csv")

raw_df = df.copy()

df["POSTCODE"] = df["POSTCODE"].apply(str)
df["BUILD_YEAR"] = df["BUILD_YEAR"].apply(int)
df["BEDROOMS"] = df["BEDROOMS"].apply(int)

# Change bedrooms so that if it is greater than 3, it will be 3+

df["BEDROOMS"] = df["BEDROOMS"].apply(lambda x: "3+" if x > 3 else x)

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

    bar_fig = px.histogram(df.groupby(['BUILD_YEAR']).mean(numeric_only = True).reset_index(), x = "BUILD_YEAR", y = "PRICE", template=  "plotly_dark")

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
    
    line_fig = px.line(df.groupby(['BUILD_YEAR', 'BEDROOMS']).mean(numeric_only = True).reset_index(), x = "BUILD_YEAR", y = "PRICE", color = "BEDROOMS",template="plotly_dark")

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
        ], width=10),
        dbc.Col([
            dbc.Button("Download CSV", id="btn_csv", color="primary", className="mr-1", 
                       style = {"margin-top":"1rem", "margin-left": "3rem"} ),
            dcc.Download(id="download-dataframe-csv")
        ], width=2)

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
                options=df["BEDROOMS"].unique(),
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
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("Predict the price of your house:", style={"textAlign": "left"})
        ], width=10)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Input(id="input_bedrooms", type="number", placeholder="Enter number of bedrooms"),
            

        ]),
        
        dbc.Col([
            
            dbc.Input(id="input_bathrooms", type="number", placeholder="Enter number of bathrooms"),
            

        ]),

         dbc.Col([

            dbc.Input(id="input_garage", type="number", placeholder="Enter number of garage"),

        ])
    ]),

    dbc.Row([

        dbc.Col([
            html.Br()
        ])
    ]),

    dbc.Row([

        html.P(id = "output")
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
        filter_suburb = df["SUBURB"].unique()
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

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(raw_df.to_csv, "mydf.csv")

@callback(
    Output("output", "children"),
    Input("input_bedrooms", "value"),
    Input("input_bathrooms", "value"),
    Input("input_garage", "value")
)

def update_output(bedrooms, bathrooms, garage):
    if bedrooms is not None and bathrooms is not None and garage is not None:
        return f"The predicted price is: {price_prediction(bedrooms, bathrooms, garage)[0]:,.2f}"
    else:
        return "Please enter the number of bedrooms, bathrooms and garage"




if __name__ == "__main__":
    app.run_server(debug=True)