from dash import dcc, Input, Output, html, State, Dash
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP, 'style.css'
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Restaurant Analytics: Understand Restaurant Frequency!"
app._favicon = "favicon.ico"

df = pd.read_csv('restaurants_zomato.csv', encoding="ISO-8859-1")

# country iso with counts
col_label = "country_code"
col_values = "count"

v = df[col_label].value_counts()
new = pd.DataFrame({
    col_label: v.index,
    col_values: v.values
})

hexcode = 0
borders = [hexcode for x in range(len(new))],
map = dcc.Graph(
    id='8',
    figure={
        'data': [{
            'locations': new['country_code'],
            'z':new['count'],
            'colorscale': 'Earth',
            'reversescale':True,
            'hover-name':new['country_code'],
            'type': 'choropleth'
        }],
        'layout': {'title': dict(
            text='Restaurant Frequency by Location',
            font=dict(size=20,
                      color='white')),
                   "paper_bgcolor": "#111111",
                   "plot_bgcolor": "#111111",
                   "height": 800,
                   "geo": dict(bgcolor='rgba(0,0,0,0)')}})


# groupby country code/city and count rating
df2 = pd.DataFrame(df.groupby(by='Restaurant Name')['Votes'].mean())
df2 = df2.reset_index()
df2 = df2.sort_values(['Votes'], ascending=False)
df3 = df2.head(10)

bar1 = dcc.Graph(id='bar1',
                 figure={
                     'data': [go.Bar(x=df3['Restaurant Name'],
                                     y=df3['Votes'])],
                     'layout': {'title': dict(
                         text='Top Restaurants in India',
                         font=dict(size=20,
                                   color='white')),
                                "paper_bgcolor": "#111111",
                                "plot_bgcolor": "#111111",
                                'height': 600,
                                "line": dict(
                         color="white",
                         width=4,
                         dash="dash",
                     ),
                         'xaxis': dict(tickfont=dict(
                             color='white'), showgrid=False, title='', color='white'),
                         'yaxis': dict(tickfont=dict(
                             color='white'), showgrid=False, title='Number of Votes', color='white')
                     }})


# pie chart - rating

col_label = "Rating text"
col_values = "Count"

v = df[col_label].value_counts()
new2 = pd.DataFrame({
    col_label: v.index,
    col_values: v.values
})

pie3 = dcc.Graph(
    id="pie3",
    figure={
        "data": [
            {
                "labels": new2['Rating text'],
                "values":new2['Count'],
                "hoverinfo":"label+percent",
                "hole": .7,
                "type": "pie",
                'marker': {'colors': [
                        '#0052cc',
                        '#3385ff',
                        '#99c2ff'
                ]
                },
                "showlegend": True
            }],
        "layout": {
            "title": dict(text="Rating Distribution",
                          font=dict(
                              size=20,
                              color='white')),
            "paper_bgcolor": "#111111",
            "showlegend": True,
            'height': 600,
            'marker': {'colors': [
                '#0052cc',
                '#3385ff',
                '#99c2ff'
            ]
            },
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "",
                    "x": 0.2,
                    "y": 0.2
                }
            ],
            "showlegend": True,
            "legend": dict(fontColor="white", tickfont={'color': 'white'}),
            "legenditem": {
                "textfont": {
                    'color': 'white'
                }
            }
        }}
)

graphRow1 = dbc.Row([dbc.Col(map, md=12)])
graphRow2 = dbc.Row([dbc.Col(bar1, md=6), dbc.Col(pie3, md=6)])

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.P(children="🍴", className="header-emoji"),
            html.H1(
                children="Restaurant Analytics", className="header-title"
            ),
            html.P(
                children="Analyze the restaurant frequency and the ratings"
                " of various restaurants the across world",
                className="header-description",
            ),
        ],
        className="header",
    ), graphRow1, html.Br(), graphRow2], style={
    'backgroundColor': '#222222'})


if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
