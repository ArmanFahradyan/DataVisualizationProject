
import dash
# from dash import dcc, html
# from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import plotly.graph_objects as go
import os

from dash import Dash, dcc, html, Input, Output, callback


dash.register_page(__name__, path='/plots', title='Sales', name='Plots')


# Load data
df = pd.read_csv(os.path.join("data", "video_games_sales.csv"))
df = df.dropna(subset=["Year_of_Release", "Global_Sales"])
df["Year_of_Release"] = df["Year_of_Release"].astype(int)

# Dropdown options
publishers = df["Publisher"].value_counts()[:10].index
genres = sorted(df["Genre"].dropna().unique())
regions = {
    "North America": "NA_Sales",
    "Europe": "EU_Sales",
    "Japan": "JP_Sales",
    "Other": "Other_Sales",
    "Global": "Global_Sales"
}

# Layout

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="publisher-sales-over-time"),
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=9, xl=9, xxl=9),
        dbc.Col([
            html.Label("Select Publisher:"),
            html.Div([dcc.Dropdown(id="publisher-dropdown",
                                   options=[{"label": p, "value": p} for p in publishers],
                                   value="Electronic Arts")
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=3, xl=3, xxl=3)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="genre-sales-pie"),
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=9, xl=9, xxl=9),
        dbc.Col([
            html.Label("Select Genre:"),
            html.Div([dcc.Dropdown(id="genre-dropdown",
                                   options=[{"label": g, "value": g} for g in genres],
                                   value="Action")
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=3, xl=3, xxl=3)
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="top-games-region"),
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=9, xl=9, xxl=9),
        dbc.Col([
            html.Label("Select Region:"),
            html.Div([dcc.Dropdown(id="region-dropdown",
                                   options=[{"label": k, "value": v} for k, v in regions.items()],
                                   value="Global_Sales")
            ], style={"padding": 20})
        ], xs=6, sm=6, md=6, lg=3, xl=3, xxl=3)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="top-platforms-slider-graph")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.RangeSlider(
                id="year-slider",
                min=df["Year_of_Release"].min(),
                max=df["Year_of_Release"].max(),
                step=1,
                marks={y: str(y) for y in range(df["Year_of_Release"].min(), df["Year_of_Release"].max()+1, 5)},
                value=[2000, 2005],  # default range
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ])
    ], style={"marginBottom": 30}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="genre-trend-graph")
        ], xs=8, sm=8, md=8, lg=10, xl=10, xxl=10),

        dbc.Col([
            html.Label("Select Genres:"),
            dcc.Checklist(
                id="genre-checklist",
                options=[{"label": genre, "value": genre} for genre in sorted(df["Genre"].dropna().unique())],
                value=["Action", "Sports"],  # default genres
                inline=True,
                labelStyle={"marginRight": "15px"}
            )
        ], xs=4, sm=4, md=4, lg=2, xl=2, xxl=2)
    ])

])


# Callbacks
@callback(
    Output("publisher-sales-over-time", "figure"),
    Input("publisher-dropdown", "value")
)
def update_publisher_sales(publisher):
    filtered = df[df["Publisher"] == publisher]
    sales = filtered.groupby("Year_of_Release")["Global_Sales"].sum().reset_index()
    fig = px.line(sales, x="Year_of_Release", y="Global_Sales", title=f"Global Sales Over Time for {publisher}")
    return fig


@callback(
    Output("genre-sales-pie", "figure"),
    Input("genre-dropdown", "value")
)
def update_genre_sales(genre):
    filtered = df[df["Genre"] == genre]
    sales_by_region = {
        "NA": filtered["NA_Sales"].sum(),
        "EU": filtered["EU_Sales"].sum(),
        "JP": filtered["JP_Sales"].sum(),
        "Other": filtered["Other_Sales"].sum()
    }
    fig = px.pie(
        names=sales_by_region.keys(),
        values=sales_by_region.values(),
        title=f"Sales Distribution by Region for {genre} Games",
        hole=0.4
    )
    return fig


@callback(
    Output("top-games-region", "figure"),
    Input("region-dropdown", "value")
)
def update_top_games(region_col):
    top_games = df[["Name", region_col]].sort_values(by=region_col, ascending=False).dropna().head(10)
    fig = px.bar(
        top_games,
        x=region_col,
        y="Name",
        orientation="h",
        title=f"Top 10 Games in {region_col.replace('_Sales', '').replace('_', ' ')}",
        labels={region_col: "Sales (millions)", "Name": "Game"}
    )
    return fig


@callback(
    Output("top-platforms-slider-graph", "figure"),
    Input("year-slider", "value")
)
def update_top_platforms(year_range):
    start_year, end_year = year_range
    dff = df[(df["Year_of_Release"] >= start_year) & (df["Year_of_Release"] <= end_year)]

    top_platforms = (
        dff.groupby("Platform")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    fig = px.bar(
        top_platforms,
        x="Platform",
        y="Global_Sales",
        title=f"Top 5 Platforms by Global Sales ({start_year} - {end_year})",
        labels={"Global_Sales": "Sales (millions)"}
    )
    return fig


@callback(
    Output("genre-trend-graph", "figure"),
    Input("genre-checklist", "value")
)
def update_genre_trend(selected_genres):
    if not selected_genres:
        return go.Figure()  # Empty figure if none selected

    filtered = df[df["Genre"].isin(selected_genres)]
    grouped = (
        filtered.groupby(["Year_of_Release", "Genre"])["Global_Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        grouped,
        x="Year_of_Release",
        y="Global_Sales",
        color="Genre",
        title="Genre Popularity Over Time",
        labels={"Global_Sales": "Global Sales (millions)", "Year_of_Release": "Year"}
    )

    fig.update_layout(legend_title="Genre")
    return fig