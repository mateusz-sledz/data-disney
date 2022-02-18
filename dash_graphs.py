import pandas as pd
import plotly.express as px
from dash import dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

df = pd.read_csv('disney_plus_titles.csv')

###################################### Movies and Tv Shows comparison
g_by = df.groupby(['type'])
values = [g_by.size()[0], g_by.size()[1]]

fig = px.bar(df, x=g_by.groups.keys(), y=values, title='Movies vs TV Shows - Count',
             labels={
                 'x': '',
                 'y': 'total count'
             }, width=600, height=600, color=g_by.groups.keys())
fig.update_layout(title_font_family='Lato')
fig.update_traces(hovertemplate='type: %{label}<br>count: %{value}<extra></extra>')

###################################### Graph number 2

g_by_release = df.groupby(['release_year'])


@app.callback(
    Output('content-release-date', 'figure'),
    Input('start_y', 'value'),
    Input('end_y', 'value'))
def update_figure(start_year, end_year):
    filtered_df = df[(start_year <= df['release_year']) & (df['release_year'] <= end_year)]

    g_by_release = filtered_df.groupby(['release_year'])

    values_years = [count for count in g_by_release.size()]

    fig = px.bar(filtered_df, x=list(g_by_release.groups.keys()), y=values_years, labels={
        'x': 'year',
        'y': 'total count'
    }, height=600, color=g_by_release.groups.keys())
    fig.update_layout(title_font_family='Lato')
    fig.update_traces(hovertemplate='year: %{label}<br>count: %{value}<extra></extra>')
    fig.update_layout(transition_duration=500)

    return fig

###################################### Graph number 3

g_by_rating = df.groupby(['rating']).size().reset_index(name='count')

fig3 = px.treemap(g_by_rating, path=['rating'], values='count', title='Rating distribution', height=600, width=1000)
fig3.update_layout(title_font_family='Lato')
fig3.update_traces(hovertemplate='rating: %{label}<br>count: %{value}<extra></extra>')
fig3.data[0].textinfo = 'label+value'

###################################### Graph number 4

df['time'] = df['duration'].str.replace(' min', '')

results = df[df['type'] == 'Movie']

results = results.astype({'time': int})
results = results.sort_values('time')

fig4 = px.histogram(results, x='time', labels={
    'x': 'length in minutes',
    'y': 'total count'
}, nbins=50, width=800, height=600, title='Movies duration distribution', color=results['time'])
fig4.update_layout(title_font_family='Lato')
fig4.update_traces(hovertemplate='duration (min): %{x}<br>count: %{y}<extra></extra>')

###################################### Graph number 5

df['seasons'] = df['duration'].str.replace(' Seasons| Season', '')

results = df[df['type'] == 'TV Show']

results = results.astype({'seasons': int})
results = results.sort_values('seasons')

fig5 = px.histogram(results, x='seasons', labels={
    'x': 'number of seasons',
    'y': 'total count'
}, width=800, height=600, title=' TV Shows duration distribution (seasons)', color=results['seasons'])
fig5.update_layout(title_font_family='Lato')
fig5.update_traces(hovertemplate='duration (number of seasons): %{x} <br>count: %{y}<extra></extra>')


###### App layout

app.layout = html.Div(style={'fontFamily': 'Lato', 'margin': '12px 36px'}, children=[
    html.H1(children='Disney+ Movies and TV Shows'),
    html.Div([
        dcc.Graph(
            id='movie-type-distribution',
            figure=fig
        ),
        dcc.Graph(
            id='rating_distribution',
            figure=fig3
        ),
    ], style={
        "display": "flex",
        "justifyContent": "space-around",
    }),
    html.Div([
        "Distribution of content release date in Disney+"
    ], style={
        "fontWeight": "600",
        "textAlign": "center",
        "width": "100%",
        "fontSize": 20,
        "marginBottom": 8,
    }),
    html.Div([
        html.Div([
            "Starting Year: ",
            dcc.Dropdown(list(g_by_release.groups.keys()), 1928, id='start_y')
        ],
            style={
                "width": "25%",
            },
        ),
        html.Div([
            "End Year: ",
            dcc.Dropdown(list(g_by_release.groups.keys()), 2021, id='end_y')
        ],
            style={
                "width": "25%"
            },
        )]
        , style={
            "display": "flex",
            "justifyContent": "space-around",
            "fontWeight": "600",
        }),
    dcc.Graph(
        id='content-release-date'
    ),
    html.Div([
        "Distribution of content duration in Disney"
    ], style={
        "fontWeight": "600",
        "textAlign": "center",
        "width": "100%",
        "fontSize": 20,
        "marginBottom": 12,
    }),
    html.Div([
        html.Div([
            dcc.Graph(
                id='movies-duration',
                figure=fig4
            ),
        ], style={
            "width": "50%"
        }),

        html.Div([
            dcc.Graph(
                id='series-duration',
                figure=fig5
            )
        ], style={
            "width": "50%"
        }),
    ], style={
        "display": "flex",
    }),

])

if __name__ == '__main__':
    app.run_server(debug=True)
