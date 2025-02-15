import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

# Load the dataset
df = pd.read_csv('data/raw/gapminder_data_graphs.csv')
df = df.dropna(subset=["country", "continent", "year", "life_exp", "hdi_index", 
                       "co2_consump", "gdp", "services"])

app = dash.Dash(__name__)

# Layout of the application
app.layout = html.Div([
    html.Div([
        html.Label('Select Continent:'),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': i, 'value': i} for i in df['continent'].unique()],
            value='Asia'
        ),
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown'
        ),
        html.Label('Select Year Range:'),
        dcc.RangeSlider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=[df['year'].min(), df['year'].max()],
            marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1, 5)},
            step=None
        ),
    ], style={'padding': 20}),
    dcc.Graph(id='indicator-graphic')
])

# Callback for updating the country dropdown based on selected continent
@app.callback(
    Output('country-dropdown', 'options'),
    Input('continent-dropdown', 'value'))
def set_countries_options(selected_continent):
    filtered_df = df[df['continent'] == selected_continent]
    return [{'label': i, 'value': i} for i in filtered_df['country'].unique()]

@app.callback(
    Output('country-dropdown', 'value'),
    Input('country-dropdown', 'options'))
def set_countries_value(available_options):
    return available_options[0]['value']

# Callback for updating the graph
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value')])
def update_graph(continent, country, year_range):
    filtered_df = df[(df['continent'] == continent) &
                     (df['country'] == country) &
                     (df['year'] >= year_range[0]) &
                     (df['year'] <= year_range[1])]

    trace = go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['life_exp'],
        mode='lines+markers',
        name='Life Expectancy'
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            title=f'Life Expectancy for {country}',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Life Expectancy'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
