from dash.dependencies import Input, Output
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from src.data import METRIC_LABELS, CONTINENT_COLORS


def register_callbacks(app, df, geo_df):
    """Register all callback functions for the Dash app."""

    # Callback to update country dropdown options based on selected continent
    @app.callback(
        [Output("country-dropdown", "options"), Output("country-dropdown", "value")],
        [Input("continent-dropdown", "value"), Input("map-graph", "signalData")],
    )
    def set_countries_options(selected_continent, clicked_region):
        print(clicked_region)
        print("clicked_region")
        bool_check = clicked_region.get("select_region")
        # if clicked_region and "country" in clicked_region["select_region"]:
        if bool_check:
            if "(All)" in selected_continent:
                filtered_df = df
                options = [{"label": "(All)", "value": "(All)"}] + [
                    {"label": i, "value": i} for i in filtered_df["country"].unique()
                ]
                value = clicked_region["select_region"]["country"]
                return options, value
            else:
                filtered_df = df[df["continent"].isin(selected_continent)]
                options = [{"label": "(All)", "value": "(All)"}] + [
                    {"label": i, "value": i} for i in filtered_df["country"].unique()
                ]
                value = clicked_region["select_region"]["country"]
                return options, value
        else:
            if "(All)" in selected_continent:
                filtered_df = df
            else:
                filtered_df = df[df["continent"].isin(selected_continent)]
            options = [{"label": "(All)", "value": "(All)"}] + [
                {"label": i, "value": i} for i in filtered_df["country"].unique()
            ]
            value = filtered_df["country"].unique()[0]
            return options, value

    # Callback to set default country dropdown value
    # @app.callback(
    #     Output("country-dropdown", "value"),
    #     Input("country-dropdown", "options")
    # )
    # def set_countries_value(available_options):
    #     return available_options[1]["value"]

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
                    "backgroundColor": "#4077A6",
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
                    "backgroundColor": "#4077A6",
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
                    "backgroundColor": "#4077A6",
                    "color": "white",
                    "textAlign": "center",
                    "fontSize": "20px",
                },
            ),
            dbc.CardBody(
                f"{avg_service:.2f}%",
                style={"textAlign": "center", "fontSize": "35px"},
            ),
            dbc.CardFooter(
                f" {percentage_change_service}", style={"textAlign": "center"}
            ),
        ]
        # Format the output
        return _avg_life, _avg_gdp, _avg_service

    # Callback to update the map chart
    @app.callback(
        Output("map-graph", "spec"),
        [Input("continent-dropdown", "value"), Input("year-slider-top", "value")],
    )
    def update_map(selected_continent, selected_year):
        if "(All)" in selected_continent:
            dff = geo_df[geo_df["year"] == selected_year]
        else:
            dff = geo_df[
                (geo_df["year"] == selected_year)
                & (geo_df["continent"].isin(selected_continent))
            ]

        if dff.empty:
            # return go.Figure()
            return {}

        select = alt.selection_point(fields=["country"], name="select_region")

        map = (
            (
                alt.Chart(
                    dff, width="container", title=f"Life expectancy in {selected_year}"
                )
                .mark_geoshape(stroke="black")
                .encode(
                    alt.Color("life_exp").title("Winner"),
                    tooltip=["country", "life_exp"],
                )
            )
            # .properties(width=600, heigth=600)
            .add_params(select)
        )

        map_with_selection = map.encode(
            opacity=alt.condition(select, alt.value(0.8), alt.value(0.2))
        )

        return map_with_selection.interactive().to_dict(format="vega")

    # Callback to update the bubble chart
    @app.callback(
        Output("bubble-graph", "spec"),
        [
            Input("continent-dropdown", "value"),
            Input("year-slider-top", "value"),
            Input("map-graph", "signalData"),
            Input("metric-dropdown-bottom", "value"),
        ],
    )
    def update_bubble(
        selected_continent, selected_year, clicked_region, selected_metric
    ):

        bool_check = clicked_region.get("select_region")

        metric_label = METRIC_LABELS.get(
            selected_metric, selected_metric
        )  # Default to variable name if not found

        if bool_check:
            if "(All)" in selected_continent:
                dff = df[df["year"] == selected_year]
            else:
                dff = df[
                    (df["year"] == selected_year)
                    & (df["continent"].isin(selected_continent))
                ]

            if dff.empty:
                return {}

            # **Define fixed colors for continents**
            continent_colors = {
                "Africa": "#1f77b4",  # Blue
                "Asia": "#ff7f0e",  # Orange
                "Europe": "#2ca02c",  # Green
                "North America": "#d62728",  # Red
                "Oceania": "#9467bd",  # Purple
                "South America": "#8c564b",  # Brown
            }
            countries = clicked_region["select_region"]["country"]
            chart = (
                alt.Chart(dff)
                .mark_circle()
                .encode(
                    # x=alt.X("gdp:Q", title="GDP"),
                    x=alt.X(selected_metric, title=metric_label),
                    y=alt.Y("life_exp:Q", title="Life Expectancy"),
                    size=alt.Size("co2_consump:Q", title="CO2 Consumption"),
                    color=alt.Color(
                        "continent:N",
                        scale=alt.Scale(range=list(continent_colors.values())),
                    ),
                    tooltip=[
                        "country:N",
                        "gdp:Q",
                        "life_exp:Q",
                        "co2_consump:Q",
                        "continent:N",
                    ],
                    opacity=alt.condition(
                        alt.expr.if_(
                            alt.expr.indexof(countries, alt.datum.country) != -1,
                            True,
                            False,
                        ),
                        alt.value(0.9),
                        alt.value(0.05),
                    ),
                )
                .properties(
                    width="container",
                    title=f"Scatter plot of Life Expectancy against {metric_label}",
                )
                .interactive()
            )
        else:
            if "(All)" in selected_continent:
                dff = df[df["year"] == selected_year]
            else:
                dff = df[
                    (df["year"] == selected_year)
                    & (df["continent"].isin(selected_continent))
                ]

            if dff.empty:
                return {}

            # **Define fixed colors for continents**
            continent_colors = {
                "Africa": "#1f77b4",  # Blue
                "Asia": "#ff7f0e",  # Orange
                "Europe": "#2ca02c",  # Green
                "North America": "#d62728",  # Red
                "Oceania": "#9467bd",  # Purple
                "South America": "#8c564b",  # Brown
            }

            chart = (
                alt.Chart(dff)
                .mark_circle()
                .encode(
                    # x=alt.X("gdp:Q", title="GDP"),
                    x=alt.X(selected_metric, title=metric_label),
                    y=alt.Y("life_exp:Q", title="Life Expectancy"),
                    size=alt.Size("co2_consump:Q", title="CO2 Consumption"),
                    color=alt.Color(
                        "continent:N",
                        scale=alt.Scale(range=list(continent_colors.values())),
                    ),
                    tooltip=[
                        "country:N",
                        "gdp:Q",
                        "life_exp:Q",
                        "co2_consump:Q",
                        "continent:N",
                    ],
                )
                .properties(
                    width="container",
                    title=f"Scatter plot of Life Expectancy against {metric_label}",
                )
                .interactive()
            )
        return chart.to_dict(format="vega")

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
        [
            Input("metric-dropdown-bottom", "value"),
            Input("continent-dropdown", "value"),
        ],
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
            filtered_df.groupby(["year", "continent"])[selected_metric]
            .mean()
            .reset_index()
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
                title=f"Average {metric_label} Over Time by Continent",
                width="container",
            )
            .interactive()
        )

        return alt_chart.to_dict(format="vega")
