# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:59:21 2020

@author: adare
"""

import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

APP_PATH = os.path.dirname(os.path.realpath('__file__'))

df_lat_lon = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "lat_lon_counties.csv"))
)
df_lat_lon["municipality_id"] = df_lat_lon["municipality_id"].astype(str).str.rjust(4,'0')

df_full_data = pd.read_csv(
    os.path.join(
        APP_PATH, os.path.join("data", "top_10_jobs_cleaned.csv")
    )
)

index = df_full_data[df_full_data["municipality_id"].isna()].index.values
df_full_data = df_full_data.drop(index, axis=0)

df_full_data["municipality_id"] = df_full_data["municipality_id"].astype(float)
df_full_data["municipality_id"] = df_full_data["municipality_id"].astype(int)
df_full_data["municipality_id"] = df_full_data["municipality_id"].astype(str).str.rjust(4,'0')

df_lat_lon["hover"] = df_lat_lon["hover"] + ', '+df_lat_lon["municipality_id"]

YEARS = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

BINS = ['1-50', '51-100', '101-200', '201-500', '501-750', '751-1000', '1001-2000', '2001-3000', '3001-4000', '4001-6000',
          '6001-10000', '1001-20000']

DEFAULT_COLORSCALE = [
    "#fff4c9",
    "#ffeb9c",
    "#ffe478",
    "#ffdc4f",
    "#ffd52b",
    "#fecd00",
    "#deb100",
    "#c79f00",
    "#a68400",
    "#917400",
    "#6e5800",
    "#594700"
]

DEFAULT_OPACITY = 0.98
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("sweden_round_flag_with_pattern_64.png")),
                html.H4(children="Job Market in Sweden- Based on Swedish Public Employment Service Data"),
                html.P(
                    id="description",
                    children="This dataset consists of 6.3M job postings (11.7M job positions) published on Platsbanken\
                    from the year 2006 up to and including 2019. Each listing contains metadata on location, dates,\
                    employer name, job type and any additional job details.",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#fecd00"},
                                        }
                                        for year in YEARS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap of the jobs available in year {0}".format(
                                        min(YEARS)
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=dict(
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=62.8258, lon=20.2630
                                                ),
                                                pitch=0,
                                                zoom=3.8,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                { 
                                    "label": 'säljare',
                                    "value": "säljare",
                                },
                                {
                                    "label": "lärare",
                                    "value": "lärare",
                                },
                                {
                                    "label": "sjuksköterska",
                                    "value": "sjuksköterska",
                                },
                                  {
                                    "label": "kock/kokerska",
                                    "value": "kock/kokerska",
                                },
                                  {
                                    "label": "butikspersonal",
                                    "value": "butikspersonal",
                                },

                                  {
                                    "label": "undersköterska",
                                    "value": "undersköterska",
                                },

                                  {
                                    "label": "ekonom",
                                    "value": "ekonom",
                                },

                                  {
                                    "label": "programmerare/systemutvecklare",
                                    "value": "programmerare/systemutvecklare",
                                },
                                 {
                                    "label": "vårdare",
                                    "value": "vårdare",
                                },
                                {
                                    "label": "tekniker",
                                    "value": "tekniker",
                                },
                                {
                                    "label": "butikspersonal",
                                    "value": "butikspersonal",
                                },
                            ],
                            value="säljare",
                            id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#006aa8",
                                    plot_bgcolor="#006aa8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("county-choropleth", "figure"),
    [Input("years-slider", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(year, figure):
    cm = dict(zip(BINS, DEFAULT_COLORSCALE))
    
    data = [
        dict(
            lat=df_lat_lon["latitude"],
            lon=df_lat_lon["longitude"],
            text=df_lat_lon["hover"],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=10, color="white", opacity=0),
        )
    ]

    annotations = [
        dict(
            showarrow=False,
            align="right",
            text="<b>Number of job available<br>per county per year</b>",
            font=dict(color="#ffd000"),
            bgcolor="#1f2630",
            x=0.95,
            y=0.95,
        )
    ]

    for i, bin in enumerate(reversed(BINS)):
        color = cm[bin]
        annotations.append(
            dict(
                arrowcolor=color,
                text=bin,
                x=0.95,
                y=0.85 - (i / 20),
                ax=-60,
                ay=0,
                arrowwidth=5,
                arrowhead=0,
                bgcolor="#1f2630",
                font=dict(color="#fecd00"),
            )
        )

    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = 62.8258
        lon = 20.2630
        zoom = 3.8

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=annotations,
        dragmode="lasso",
    )

    base_url = "https://raw.githubusercontent.com/AdaRey00/platsbanken/main/"
    for bin in BINS:
        geo_layer = dict(
            sourcetype="geojson",
            source=base_url + str(year) + "/" + bin + ".geojson",
            type="fill",
            color=cm[bin],
            opacity=DEFAULT_OPACITY,
            # CHANGE THIS
            fill=dict(outlinecolor="#afafaf"),
        )
        layout["mapbox"]["layers"].append(geo_layer),

    fig = dict(data=data, layout=layout)
    return fig 

@app.callback(Output("heatmap-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Heatmap of the jobs available in year {0}".format(
        year
    )

@app.callback(
    Output("selected-data", "figure"),
    [
        Input("county-choropleth", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data(selectedData, chart_dropdown, year):
    if selectedData is None:
        return dict(
            data=[dict(x=0, y=0)],
            layout=dict(
                title="Click-drag on the map to select counties",
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#fecd00"),
                margin=dict(t=75, r=50, b=100, l=75),
            ),
        )
    
    pts = selectedData["points"]
    fips = [str(pt["text"].split(",")[-1]).replace(" ", "") for pt in pts]
#    for i in range(len(fips)):
#        if len(fips[i]) == 4:
#            fips[i] = "0" + fips[i]
    dff = df_full_data[df_full_data["municipality_id"].isin(fips)]
    dff = dff.sort_values("year")
   

    
    dropdown_df = dff[dff.profession_name == chart_dropdown].groupby(['municipality_id', 'municipality_name'])['nbr_of_placement'].sum().reset_index(level=[0])
    dropdown_df.municipality_id = dropdown_df.municipality_id.astype(str).str.rjust(4,'0')
    fig = dropdown_df.iplot(
            kind="bar", y='nbr_of_placement', asFigure=True
        )

    fig_layout = fig["layout"]
    fig_data = fig["data"]
    #fig_data[0]["text"] = dropdown_df.values.tolist()
    
    c = dropdown_df.values.tolist()
    new_c = [x[1] for x in c]
    
    fig_data[0]["text"] = new_c
    fig_data[0]["marker"]["color"] = "#fecd00"
    fig_data[0]["marker"]["opacity"] = 1
    fig_data[0]["marker"]["line"]["width"] = 0
    fig_data[0]["textposition"] = "outside"
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#fecd00"
    fig_layout["title"]["font"]["color"] = "#fecd00"
    fig_layout["xaxis"]["tickfont"]["color"] = "#fecd00"
    fig_layout["yaxis"]["tickfont"]["color"] = "#fecd00"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["margin"]["t"] = 75
    fig_layout["margin"]["r"] = 50
    fig_layout["margin"]["b"] = 100
    fig_layout["margin"]["l"] = 50
    
    return fig

    fig = dff.iplot(
        kind="bar",
        x="municipality_name",
        y="nbr_of_placement",
        text="municipality_name",
        categories="municipality_name",
        colors=[
            "#1b9e77",
            "#d95f02",
            "#7570b3",
            "#e7298a",
            "#66a61e",
            "#e6ab02",
            "#a6761d",
            "#666666",
            "#1b9e77",
        ],
        vline=['municipality_name'],
        asFigure=True,
    )

    for i, trace in enumerate(fig["data"]):
        trace["mode"] = "lines+markers"
        trace["marker"]["size"] = 4
        trace["marker"]["line"]["width"] = 1
        trace["type"] = "scatter"
        for prop in trace:
            fig["data"][i][prop] = trace[prop]

        # Only show first 500 lines
        fig["data"] = fig["data"][0:500]

        fig_layout = fig["layout"]
        # See plot.ly/python/reference
        fig_layout["yaxis"]["title"] = "jobs for counties for each year"
        fig_layout["xaxis"]["title"] = ""
        fig_layout["yaxis"]["fixedrange"] = True
        fig_layout["xaxis"]["fixedrange"] = False
        fig_layout["hovermode"] = "closest"
        fig_layout["title"] = "<b>{0}</b> counties selected".format(len(fips))
        fig_layout["legend"] = dict(orientation="v")
        fig_layout["autosize"] = True
        fig_layout["paper_bgcolor"] = "#1f2630"
        fig_layout["plot_bgcolor"] = "#1f2630"
        fig_layout["font"]["color"] = "#fecd00"
        fig_layout["xaxis"]["tickfont"]["color"] = "#fecd00"
        fig_layout["yaxis"]["tickfont"]["color"] = "#fecd00"
        fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"

    if len(fips) > 500:
        fig["layout"][
            "title"
        ] = "Jobs available per county per year <br>(only 1st 500 shown)"

    return fig

if __name__ == "__main__":
    app.run_server(debug=False, use_reloader=False)