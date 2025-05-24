import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import plotly.graph_objects as go
import os


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2")
            ],
            href=page["path"],
            active="exact"
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="bg-light"

)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(html.H1("🎮 Video Game Sales Dashboard", style={'textAlign': 'center'}))
        ])
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ],
                # width=3),
                xs=4, sm=4, md=4, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ],
                # width=8.5)
                xs=8, sm=8, md=8, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
