import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv('disney_plus_titles.csv')

###################################### Movies and Tv Shows comparison
g_by = df.groupby(['type'])
values = [g_by.size()[0], g_by.size()[1]]

fig = px.bar(df, x=g_by.groups.keys(), y=values)

###################################### Graph number 2

g_by_release = df.groupby(['release_year'])
 
values_years = [count for count in g_by_release.size()]

fig2 =  px.bar(df, x=g_by_release.groups.keys(), y=values_years)

###################################### Graph number 3

g_by_rating = df.groupby(['rating']).size().reset_index(name='count')

fig3 = px.treemap(g_by_rating, path=['rating'], values='count')

###################################### Graph number 4

df['time'] = df['duration'].str.replace(' min', '')

results = df[df['type'] == 'Movie']

results = results.astype({"time": int})
results = results.sort_values('time')

fig4 = px.histogram(results, x='time', nbins=50)


###################################### Graph number 5

df['seasons'] = df['duration'].str.replace(' Seasons| Season', '')

results = df[df['type'] == 'TV Show']

results = results.astype({"seasons": int})
results = results.sort_values('seasons')

fig5 = px.histogram(results, x='seasons')

###### App layout

app.layout = html.Div(children=[
    html.H1(children='Disney+ Movies and TV Shows'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='example-u',
        figure=fig2
    ),

    dcc.Graph(
        id='example-op',
        figure=fig3
    ),

    dcc.Graph(
        id='exampl',
        figure=fig4
    ),

    dcc.Graph(
        id='exampl--',
        figure=fig5
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
