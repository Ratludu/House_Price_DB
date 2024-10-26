from dash import Dash, html
import dash

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Ploty Dash', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Overview'),
            html.Div('''
                This is an example of a simple Dash app with
                local, customized CSS.
            ''')
        ])
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
