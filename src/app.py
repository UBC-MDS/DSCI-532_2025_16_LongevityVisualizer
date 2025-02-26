import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('data/raw/gapminder_data_graphs.csv')
df = df.dropna(subset=["country", "continent", "year", "life_exp", "hdi_index", 
                       "co2_consump", "gdp", "services"])

# Initialize the app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Global widgets
widgets = [
            html.H1('Longevity Visualizer'),
            html.Br(),
            dbc.Card([
                dbc.CardBody([
                    html.Label('Select Continent:'),
                    dcc.Dropdown(
                        id='continent-dropdown',
                        options=[{"label": "All", "value": "All"}] + 
                                [{'label': i, 'value': i} for i in df['continent'].unique()],
                        value='All',
                        clearable=False
                    ),
                    html.Br(),
                    html.Label('Select Country:'),
                    dcc.Dropdown(id='country-dropdown'),
                    html.Br(),
                    html.Label('Select Year Range:'),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=[df['year'].min(), df['year'].max()],
                        marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1, 5)},
                        step=None
                    ),
                ])
            ], className="mb-4")
        ]

# Cards
card_holder = dbc.Card([
                    dbc.CardBody([
                    html.H1('placeholder'),
                    html.Br()
                ])
            ], className="mb-4")
first_graphic_card = dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='indicator-graphic')
                ])
            ], className="mb-4")
map_chart = dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="map-graph")
                    ])
                ], className="mb-4")
bubble_chart = dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id="bubble-graph")
                        ])
                    ], className="mb-4")
# Layout
app.layout = dbc.Container([
    dbc.Row([
        # First Column: Global widgets
        dbc.Col(widgets, style={"backgroundColor": "#fdd835", "padding": "15px", "height": "100vh"}, md=4),  # 4/12 grid width for inputs
        # Second Column: Charts
        dbc.Col([
            # First row for 3 cards
            dbc.Row([
                dbc.Col([
                    card_holder
                ]),
                dbc.Col([
                    card_holder
                ]),
                dbc.Col([
                    card_holder
                ]),
            ], className="mt-4"),
            # Second row for 2 charts
            dbc.Row([
                dbc.Col([
                    map_chart
                ]),
                dbc.Col([
                    bubble_chart
                ]),
            ]),
            # Third row for 2 charts
            dbc.Row([
                dbc.Col([
                    first_graphic_card
                ]),
                dbc.Col([
                    card_holder
                ]),
            ])
        ], md=8)  # 8/12 grid width for graph
    ])
], fluid=True)

# Callbacks

# Widget
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

# Map Chart
@app.callback(
    Output("map-graph", "figure"),
    [Input("continent-dropdown", "value"), Input("year-slider", "value")]
)
def update_map(selected_continent, year_range):
    start_year, end_year = year_range  # Extract range values
    dff = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    # Calculate the average life expectancy per country
    dff_avg = dff.groupby("country", as_index=False).agg({"life_exp": "mean"})

    # Merge with original data to retain country locations
    dff_avg = dff_avg.merge(df[['country', 'continent']], on='country', how='left').drop_duplicates()

    # If a specific continent is selected, filter again
    if selected_continent != "All":
        dff_avg = dff_avg[dff_avg["continent"] == selected_continent]

    # Create choropleth map
    fig_map = px.choropleth(
        dff_avg, locations="country", locationmode="country names", color="life_exp",
        hover_name="country", color_continuous_scale=px.colors.sequential.Viridis,
        title=f"Avg Life Expectancy ({selected_continent}, {start_year}-{end_year})", 
        projection="natural earth"
    )

    fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    return fig_map

# Bubble chart
@app.callback(
    Output("bubble-graph", "figure"),
    [Input("continent-dropdown", "value"), Input("year-slider", "value")]
)
def update_bubble(selected_continent, year_range):
    start_year, end_year = year_range
    dff = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    # Calculate the average values per country
    dff_avg = dff.groupby(["country", "continent"], as_index=False).agg({
        "gdp": "mean",
        "co2_consump": "mean",
        "life_exp": "mean"
    })

    # If a specific continent is selected, filter again
    if selected_continent != "All":
        dff_avg = dff_avg[dff_avg["continent"] == selected_continent]

    # Create bubble chart (GDP vs Life Expectancy, bubble size = CO2 consumption)
    fig_bubble = px.scatter(
        dff_avg, x="gdp", y="life_exp", size="co2_consump", color="continent",
        hover_name="country", title=f"Avg Life Expectancy vs. GDP ({start_year}-{end_year})"
    )

    fig_bubble.update_layout(margin={"r": 20, "t": 50, "l": 40, "b": 40})
    return fig_bubble

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
