import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc

dash.register_page(__name__, path="/", name="Overview")

df = pd.read_csv("data/video_games_sales.csv")
df = df.dropna(subset=["Year_of_Release", "Global_Sales"])
df["Year_of_Release"] = df["Year_of_Release"].astype(int)

layout = dbc.Container([
    html.H2("📊 Global Video Game Sales Overview", style={"textAlign": "center"}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=px.bar(
                df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False),
                x="Platform", y="Global_Sales", title="Total Sales by Platform"
            ))
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=px.line(
                df.groupby("Year_of_Release")["Global_Sales"].sum().reset_index(),
                x="Year_of_Release", y="Global_Sales", title="Global Sales Over Time"
            ))
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=px.treemap(
                df.groupby(["Genre", "Platform"])["Global_Sales"].sum().reset_index(),
                path=["Genre", "Platform"], values="Global_Sales",
                title="Sales by Genre and Platform"
            ))
        ])
    ])
])