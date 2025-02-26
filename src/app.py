import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import plotly.express as px
import dash_vega_components as dvc
from dash import Dash
alt.data_transformers.enable('vegafusion')

# Load the dataset
df = pd.read_csv('data/raw/gapminder_data_graphs.csv')
df = df.dropna(subset=["country", "continent", "year", "life_exp", "hdi_index", 
                       "co2_consump", "gdp", "services"])
unique_years = sorted(df["year"].unique())
metric_options = [
    {"label": "Life Expectancy", "value": "life_exp"},
    {"label": "HDI", "value": "hdi_index"},
    {"label": "CO2 Consumption", "value": "co2_consump"},
    {"label": "GDP per Capita", "value": "gdp"},
    {"label": "Services (%)", "value": "services"},
]

# Initialize the app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Global widgets
title = [
    dbc.Row([
        html.H1('Longevity Visualizer'),
        html.Br()
    ])
]
top_half = [
    dbc.Card([
        dbc.CardBody([
            html.Label('Select Continent(s):'),
            dcc.Dropdown(
                id='continent-dropdown',
                multi=True,
                options=[{"label": "(All)", "value": "(All)"}] + 
                        [{'label': i, 'value': i} for i in df['continent'].unique()],
                value='(All)',
                clearable=False
            ),
            html.Br(),
            html.Label('Select Year:'),
            dcc.Slider(
                id="year-slider-top",
                min=min(unique_years),
                max=max(unique_years),
                value=unique_years[0],
                marks={str(y): str(y) for y in unique_years},
                step=None,
                updatemode='drag'
            ),
        ])
    ], className="mb-4")
]
bottom_half = [
    dbc.Card([
        dbc.CardBody([
            html.Label('Select Metric:'),
            dcc.Dropdown(
                id="metric-dropdown-bottom", 
                options=metric_options, 
                value="life_exp", 
                clearable=False
            ),
            html.Br(),
            html.Label('Select Country(s):'),
            dcc.Dropdown(
                id='country-dropdown',
                multi=True,
                value=[],
                clearable=False
            ),
            html.Br(),
            html.Label('Select Year:'),
            dcc.RangeSlider(
                id="year-slider-bottom",
                min=min(unique_years),
                max=max(unique_years),
                value=[min(unique_years), max(unique_years)],
                marks={str(y): str(y) for y in unique_years},
                step=None,
                updatemode='drag'
            ),
        ])
    ], className="mb-4")
]
widgets = [ 
           dbc.Row(title),
           dbc.Row(top_half),
           dbc.Row(bottom_half)
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
metric_chart = dbc.Card([
                    dbc.CardBody([
                        dvc.Vega(id="metric-chart", spec={})
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
                    metric_chart
                ]),
                dbc.Col([
                    first_graphic_card
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
    if "(All)" in selected_continent:
        filtered_df = df
    else:
        filtered_df = df[df["continent"].isin(selected_continent)]
    return [{"label": "(All)", "value": "(All)"}] + [{'label': i, 'value': i} for i in filtered_df['country'].unique()]

@app.callback(
    Output('country-dropdown', 'value'),
    Input('country-dropdown', 'options'))
def set_countries_value(available_options):
    return available_options[1]['value']

# Map Chart
@app.callback(
    Output("map-graph", "figure"),
    [Input("continent-dropdown", "value"), Input("year-slider-top", "value")]
)
def update_map(selected_continent, selected_year):
    if "(All)" in selected_continent:
        dff = df[df["year"] == selected_year]
    else:
        dff = df[(df["year"] == selected_year) & (df["continent"].isin(selected_continent))]

    if dff.empty:
        return go.Figure()

    fig_map = px.choropleth(
        dff, locations="country", locationmode="country names", color="life_exp",
        hover_name="country", color_continuous_scale=px.colors.sequential.Viridis,
        title=f"Life Expectancy ({selected_continent}, {selected_year})", projection="natural earth"
    )
    fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    
    return fig_map

# Bubble chart
@app.callback(
    Output("bubble-graph", "figure"),
    [Input("continent-dropdown", "value"), Input("year-slider-top", "value")]
)
def update_bubble(selected_continent, selected_year):
    if "(All)" in selected_continent:
        dff = df[df["year"] == selected_year]
    else:
        dff = df[(df["year"] == selected_year) & (df["continent"].isin(selected_continent))]

    if dff.empty:
        return go.Figure()
    
    dff_bubble = dff.dropna(subset=["gdp", "co2_consump", "life_exp"])
    fig_bubble = px.scatter(
        dff_bubble, x="gdp", y="life_exp", size="co2_consump", color="continent",
        hover_name="country", title="Life Expectancy vs. GDP (Bubble Size = CO2)"
    )
    fig_bubble.update_layout(margin={"r": 20, "t": 50, "l": 40, "b": 40})
    
    return fig_bubble

# Metric chart
@app.callback(
    Output('metric-chart', 'spec'),
    [Input("metric-dropdown-bottom", "value"),
     Input('continent-dropdown', 'value'),
     Input("country-dropdown", "value"),
     Input("year-slider-bottom", "value"),]
)
def update_metric(selected_metric, selected_continent, selected_country, year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    if "(All)" not in selected_continent:
        filtered_df = filtered_df[filtered_df["continent"].isin(selected_continent)]

    if isinstance(selected_country, str):
        selected_country = [selected_country]
        
    if "(All)" not in selected_country:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]

    if filtered_df.empty:
        return alt.Chart(pd.DataFrame({'year': [], selected_metric: []})).mark_line().encode(
            alt.X('year:O', title="Year"),
            alt.Y(selected_metric, title=selected_metric),
            alt.Color('country:N', title="Country")
        ).properties(title="No data available").to_dict()

    # **Line Chart**
    line = alt.Chart(filtered_df).mark_line().encode(
        alt.X('year:O', title="Year"),
        alt.Y(selected_metric, title=selected_metric),
        alt.Color('country:N', title="Country"),
        tooltip=['year', selected_metric, 'country']
    )

    # **Points on the Line**
    points = alt.Chart(filtered_df).mark_point(size=50, filled=True).encode(
        alt.X('year:O', title="Year"),
        alt.Y(selected_metric, title=selected_metric),
        alt.Color('country:N', title="Country"),
        tooltip=['year', selected_metric, 'country']
    )

    # **Combine Line + Points**
    alt_chart = (line + points).properties(
        title=f"{selected_metric} Over Time",
        width=600
    ).interactive()

    return alt_chart.to_dict(format='vega')



@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider-bottom', 'value')])
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
