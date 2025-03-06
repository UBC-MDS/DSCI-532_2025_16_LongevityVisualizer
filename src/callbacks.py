from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from data import METRIC_LABELS, CONTINENT_COLORS

def register_callbacks(app, df):
    """Register all callback functions for the Dash app."""
    
    # Callback to update country dropdown options based on selected continent
    @app.callback(
        Output("country-dropdown", "options"), 
        Input("continent-dropdown", "value")
    )
    def set_countries_options(selected_continent):
        if "(All)" in selected_continent:
            filtered_df = df
        else:
            filtered_df = df[df["continent"].isin(selected_continent)]
        return [{"label": "(All)", "value": "(All)"}] + [
            {"label": i, "value": i} for i in filtered_df["country"].unique()
        ]

    # Callback to set default country dropdown value
    @app.callback(
        Output("country-dropdown", "value"), 
        Input("country-dropdown", "options")
    )
    def set_countries_value(available_options):
        return available_options[1]["value"]

    # Callback to update the metric cards
    @app.callback(
        [
            Output("average_life", "children"),
            Output("average_gdp", "children"),
            Output("average_service", "children"),
        ],
        [Input("continent-dropdown", "value"), Input("year-slider-top", "value")],
    )
    def update_average_values(selected_continent, selected_year):
        # Filter dataset based on selected continent(s)
        filtered_df = df[df["year"] == selected_year]

        # Filter dataset for previous year
        previous_years = df[df["year"] == selected_year - 1]

        if "(All)" not in selected_continent:
            filtered_df = filtered_df[filtered_df["continent"].isin(selected_continent)]
            previous_years = previous_years[
                previous_years["continent"].isin(selected_continent)
            ]

        # Handle case where no data is available
        if filtered_df.empty:
            return "No Data Available", "No Data Available", "No Data Available"

        # Compute Averages
        avg_life = filtered_df["life_exp"].mean()
        avg_gdp = filtered_df["gdp"].mean()
        avg_service = filtered_df["services"].mean()

        # Compute preceding year averages
        prev_avg_life = previous_years["life_exp"].mean()
        prev_avg_gdp = previous_years["gdp"].mean()
        prev_avg_service = previous_years["services"].mean()

        # Helper function to calculate percentage change
        def calculate_change(current, previous):
            if previous == 0 or pd.isna(previous):
                return ""
            change = ((current - previous) / previous) * 100
            return f"{'▲' if change > 0 else '🔻'} {abs(change):.2f}%"

        # Compute percentage changes
        percentage_change_life = calculate_change(avg_life, prev_avg_life)
        percentage_change_gdp = calculate_change(avg_gdp, prev_avg_gdp)
        percentage_change_service = calculate_change(avg_service, prev_avg_service)

        # cards to return
        _avg_life = [
            dbc.CardHeader(
                "🌍 Average Longevity",
                style={
                    "backgroundColor": "#B97403",
                    "color": "white",
                    "textAlign": "center",
                    "fontSize": "20px",
                },
            ),
            dbc.CardBody(
                f"{avg_life:.2f} years",
                style={"textAlign": "center", "fontSize": "35px"},
            ),
            dbc.CardFooter(f"{percentage_change_life}", style={"textAlign": "center"}),
        ]
        _avg_gdp = [
            dbc.CardHeader(
                "💰 Average GDP per Capita",
                style={
                    "backgroundColor": "#B97403",
                    "color": "white",
                    "textAlign": "center",
                    "fontSize": "20px",
                },
            ),
            dbc.CardBody(
                f"${int(avg_gdp):,}",
                style={"textAlign": "center", "fontSize": "35px"},
            ),
            dbc.CardFooter(f"{percentage_change_gdp}", style={"textAlign": "center"}),
        ]
        _avg_service = [
            dbc.CardHeader(
                "⛑️ Average Service Workers Percentage",
                style={
                    "backgroundColor": "#B97403",
                    "color": "white",
                    "textAlign": "center",
                    "fontSize": "20px",
                },
            ),
            dbc.CardBody(
                f"{avg_service:.2f}%",
                style={"textAlign": "center", "fontSize": "35px"},
            ),
            dbc.CardFooter(f" {percentage_change_service}", style={"textAlign": "center"}),
        ]
        # Format the output
        return _avg_life, _avg_gdp, _avg_service

    # Callback to update the map chart
    @app.callback(
        Output("map-graph", "figure"),
        [Input("continent-dropdown", "value"), Input("year-slider-top", "value")],
    )
    def update_map(selected_continent, selected_year):
        if "(All)" in selected_continent:
            dff = df[df["year"] == selected_year]
        else:
            dff = df[
                (df["year"] == selected_year) & (df["continent"].isin(selected_continent))
            ]

        if dff.empty:
            return go.Figure()

        color_min = df["life_exp"].min()
        color_max = df["life_exp"].max()

        fig_map = px.choropleth(
            dff,
            locations="country",
            locationmode="country names",
            color="life_exp",
            hover_name="country",
            color_continuous_scale=[[0, "white"], [1, "darkgreen"]],
            title=f"Life Expectancy ({selected_year})",
            projection="natural earth",
        )

        fig_map.update_layout(
            title={
                "text": f"<b>Life Expectancy in {selected_year}</b>",
                "font": {"size": 16},
                "x": 0.1,
                "xanchor": "left",
            },
            coloraxis_colorbar=dict(title="Life Expectancy"),
            coloraxis=dict(cmin=color_min, cmax=color_max),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
        )

        return fig_map

    # Callback to update the bubble chart
    @app.callback(
        Output("bubble-graph", "figure"),
        [Input("continent-dropdown", "value"), 
         Input("year-slider-top", "value"), 
         Input("metric-dropdown-bottom", "value")],
    )
    def update_bubble(selected_continent, selected_year, selected_metric):
        if "(All)" in selected_continent:
            dff = df[df["year"] == selected_year]
        else:
            dff = df[
                (df["year"] == selected_year) & (df["continent"].isin(selected_continent))
            ]

        if dff.empty:
            return go.Figure()

        dff_bubble = dff.dropna(subset=[selected_metric, "co2_consump", "life_exp"])

        # x axis scale
        global_x_min = df[selected_metric].min()
        global_x_max = df[selected_metric].max()
        # y axis scale
        global_life_exp_min = df["life_exp"].min()
        global_life_exp_max = df["life_exp"].max()
        # bubble size
        global_co2_min = df["co2_consump"].min()
        global_co2_max = df["co2_consump"].max()

        unique_continents = sorted(df["continent"].dropna().unique())

        metric_label = METRIC_LABELS.get(selected_metric, selected_metric) 

        fig_bubble = px.scatter(
            dff_bubble,
            x=selected_metric,
            y="life_exp",
            size="co2_consump",
            color="continent",
            hover_name="country",
            category_orders={"continent": unique_continents},
            color_discrete_map=CONTINENT_COLORS,
        )

        fig_bubble.update_layout(
            title={
                "text": f"<b>Life Expectancy vs. {metric_label} in {selected_year}</b>",
                "font": {"size": 16},
                "x": 0.1,
                "xanchor": "left",
            },
            annotations=[
                dict(
                    x=0,
                    y=1,
                    xref="paper",
                    yref="paper",
                    text="Bubble Size Represents CO2 Emissions per Person",
                    showarrow=False,
                    font=dict(size=9, color="gray"),
                    xanchor="left",
                )
            ],
            margin={"r": 20, "t": 50, "l": 40, "b": 40},
            xaxis=dict(
                title=metric_label,
                range=[global_x_min, global_x_max + (global_x_max - global_x_min) * 0.1], 

            ),
            yaxis=dict(
                title="Life Expectancy",
                range=[global_life_exp_min, global_life_exp_max + 10],
            ),
            dragmode="pan",
            hovermode="closest",
        )

        return fig_bubble

    # Callback to update the country-specific metric chart
    @app.callback(
        Output("country-metric-chart", "spec"),
        [
            Input("metric-dropdown-bottom", "value"),
            Input("continent-dropdown", "value"),
            Input("country-dropdown", "value"),
        ],
    )
    def update_country_metric(selected_metric, selected_continent, selected_country):
        filtered_df = df

        if "(All)" not in selected_continent:
            filtered_df = filtered_df[filtered_df["continent"].isin(selected_continent)]

        if isinstance(selected_country, str):
            selected_country = [selected_country]

        if "(All)" not in selected_country:
            filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]

        metric_label = METRIC_LABELS.get(
            selected_metric, selected_metric
        )  # Default to variable name if not found

        if filtered_df.empty:
            return (
                alt.Chart(pd.DataFrame({"year": [], selected_metric: []}))
                .mark_line()
                .encode(
                    alt.X("year:O", title="Year"),
                    alt.Y(selected_metric, title=metric_label),
                    alt.Color("country:N", title="Country"),
                )
                .properties(title="No data available")
                .to_dict(format="vega")
            )

        # Line Chart
        line = (
            alt.Chart(filtered_df)
            .mark_line()
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=metric_label),
                alt.Color("country:N", title="Country"),
                tooltip=["year", selected_metric, "country"],
            )
        )

        # Points on the Line
        points = (
            alt.Chart(filtered_df)
            .mark_point(size=50, filled=True)
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=metric_label),
                alt.Color("country:N", title="Country"),
                tooltip=["year", selected_metric, "country"],
            )
        )

        # Combine Line + Points
        alt_chart = (
            (line + points)
            .properties(title=f"{metric_label} Over Time by Country", width="container")
            .interactive()
        )

        return alt_chart.to_dict(format="vega")

    # Callback to update the continent-level metric chart
    @app.callback(
        Output("continent-metric-chart", "spec"),
        [Input("metric-dropdown-bottom", "value"), Input("continent-dropdown", "value")],
    )
    def update_continent_metric(selected_metric, selected_continent):
        filtered_df = df

        # Filter by selected continents
        if "(All)" not in selected_continent:
            filtered_df = filtered_df[filtered_df["continent"].isin(selected_continent)]

        metric_label = METRIC_LABELS.get(selected_metric, selected_metric)

        if filtered_df.empty:
            return (
                alt.Chart(pd.DataFrame({"year": [], selected_metric: []}))
                .mark_line()
                .encode(
                    alt.X("year:O", title="Year"),
                    alt.Y(selected_metric, title=metric_label),
                    alt.Color("continent:N", title="Continent"),
                )
                .properties(title="No data available")
                .to_dict(format="vega")
            )

        # Compute Average Metric per Continent
        continent_avg = (
            filtered_df.groupby(["year", "continent"])[selected_metric].mean().reset_index()
        )

        # Line Chart
        line = (
            alt.Chart(continent_avg)
            .mark_line()
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=f"Avg {metric_label}"),
                alt.Color("continent:N", title="Continent"),
                tooltip=["year", selected_metric, "continent"],
            )
        )

        # Points on the Line
        points = (
            alt.Chart(continent_avg)
            .mark_point(size=50, filled=True)
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=f"Avg {metric_label}"),
                alt.Color("continent:N", title="Continent"),
                tooltip=["year", selected_metric, "continent"],
            )
        )

        # Combine Line + Points
        alt_chart = (
            (line + points)
            .properties(
                title=f"Average {metric_label} Over Time by Continent", width="container"
            )
            .interactive()
        )

        return alt_chart.to_dict(format="vega")