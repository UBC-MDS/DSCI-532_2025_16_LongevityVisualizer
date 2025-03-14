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
        def calculate_change(current, previous, previous_year):
            if pd.isna(previous) or previous == 0 or pd.isna(current):
                return f"No data for {previous_year}", {"color": "#6c757d", "textAlign": "center", "marginBottom": "1px", "backgroundColor": "#f8f9fa"}
    
            change = ((current - previous) / previous) * 100
            arrow = "▲" if change > 0 else "🔻"
            color = "green" if change > 0 else "red"
            bg_color = "#d4edda" if change > 0 else "#f8d7da"  

            return f"{arrow} {abs(change):.2f}% from {previous_year}", {
                "color": color,
                "textAlign": "center",
                "marginBottom": "1px",
                "backgroundColor": bg_color,  # Changes the footer color
                "borderRadius": "5px",
                "padding": "5px"
            }


        # Compute percentage changes
        percentage_change_life, style_life = calculate_change(avg_life, prev_avg_life, selected_year - 1)
        percentage_change_gdp, style_gdp = calculate_change(avg_gdp, prev_avg_gdp, selected_year - 1)
        percentage_change_service, style_service = calculate_change(avg_service, prev_avg_service, selected_year - 1)


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
            dbc.CardFooter(percentage_change_life, style=style_life)        
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
            dbc.CardFooter(percentage_change_gdp, style=style_gdp)
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
            dbc.CardFooter(percentage_change_service, style=style_service)
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
                .mark_geoshape(stroke="black", cursor='pointer')
                .encode(
                    alt.Color("life_exp").title("Life Expectancy"),
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

        metric_label_title = (
        metric_label.replace("(USD)", "")
        .replace("(%)", "")
        .replace("(tonnes)", "")
        .strip()
        )


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
            
            # Find min and max for consistent y-axis scaling
            y_min = dff['life_exp'].min() * 0.95  # 5% buffer
            y_max = dff['life_exp'].max() * 1.05  # 5% buffer
            
            countries = clicked_region["select_region"]["country"]
            chart = (
                alt.Chart(dff)
                .mark_circle()
                .encode(
                    # x=alt.X("gdp:Q", title="GDP"),
                    x=alt.X(selected_metric, title=metric_label),
                    y=alt.Y(
                        "life_exp:Q", 
                        title="Life Expectancy",
                        scale=alt.Scale(domain=[y_min, y_max], zero=False)
                    ),
                    size=alt.Size("co2_consump:Q", title="CO2 Consumption"),
                    color=alt.Color(
                        "continent:N",
                        scale=alt.Scale(domain=list(continent_colors.keys()), range=list(continent_colors.values())),
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
                    title=f"Scatter plot of Life Expectancy against {metric_label_title}",
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
            
            # Find min and max for consistent y-axis scaling
            y_min = dff['life_exp'].min() * 0.95  # 5% buffer
            y_max = dff['life_exp'].max() * 1.05  # 5% buffer
            
            chart = (
                alt.Chart(dff)
                .mark_circle()
                .encode(
                    # x=alt.X("gdp:Q", title="GDP"),
                    x=alt.X(selected_metric, title=metric_label),
                    y=alt.Y(
                        "life_exp:Q", 
                        title="Life Expectancy",
                        scale=alt.Scale(domain=[y_min, y_max], zero=False)
                    ),
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
                    title=f"Scatter plot of Life Expectancy against {metric_label_title}",
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

        metric_label_title = (
        metric_label.replace("(USD)", "")
        .replace("(%)", "")
        .replace("(tonnes)", "")
        .strip()
        )

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
            .properties(title=f"{metric_label_title} Over Time by Country", width="container")
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

        metric_label_title = (
        metric_label.replace("(USD)", "")
        .replace("(%)", "")
        .replace("(tonnes)", "")
        .strip()
        )

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

        unique_continents = continent_avg["continent"].unique().tolist()
        
        continent_colors = {
            "Africa": "#1f77b4",  # Blue
            "Asia": "#ff7f0e",  # Orange
            "Europe": "#2ca02c",  # Green
            "North America": "#d62728",  # Red
            "Oceania": "#9467bd",  # Purple
            "South America": "#8c564b",  # Brown
        }

        # Ensure only colors for selected continents are used
        selected_continent_colors = {k: v for k, v in continent_colors.items() if k in unique_continents}

        line = (
            alt.Chart(continent_avg)
            .mark_line()
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=f"Avg {metric_label}"),
                alt.Color(
                    "continent:N",
                    scale=alt.Scale(domain=list(selected_continent_colors.keys()), 
                                    range=list(selected_continent_colors.values())),
                    title="Continent"
                ),
                tooltip=["year", selected_metric, "continent"],
            )
        )

        points = (
            alt.Chart(continent_avg)
            .mark_point(size=50, filled=True)
            .encode(
                alt.X("year:O", title="Year"),
                alt.Y(selected_metric, title=f"Avg {metric_label}"),
                alt.Color(
                    "continent:N",
                    scale=alt.Scale(domain=list(selected_continent_colors.keys()), 
                                    range=list(selected_continent_colors.values())),
                    title="Continent"
                ),
                tooltip=["year", selected_metric, "continent"],
            )
        )

        alt_chart = (
            (line + points)
            .properties(
                title=f"Average {metric_label_title} Over Time by Continent",
                width="container",
            )
            .interactive()
        )

        return alt_chart.to_dict(format="vega")


    #Metric definitions to map for the dropdown menu. 
    METRIC_DEFINITIONS = {
    "gdp": "GDP per capita is the total value of goods and services a country produces (Gross Domestic Product) divided by its population. It measures the average economic output per person, giving an idea of a country's standard of living.",
    "life_exp": "Life expectancy indicates the number of years a person would be expected to live based on current health, living and mortality conditions.",
    "hdi_index": "A measure of a country's overall development, considering life expectancy, education (literacy and schooling), and income per capita. It ranges from 0 to 1, with higher values indicating better development.",
    "co2_consump": "The total amount of carbon dioxide emissions produced by a country, region, or individual, usually from burning fossil fuels for energy, transportation, and industry. It is often measured in metric tons per capita.",
    "services": "Percentage of the workforce engaged in service industries. This includes workers who are part of the economy that provides non-tangible goods, such as healthcare, education, finance, retail, entertainment, and tourism, rather than physical products.",
}

    @app.callback(
        Output("metric-definition", "children"),
        Input("metric-dropdown-bottom", "value")
    )
    #Adds the mapped metric definitions for the drop down menu. 
    def update_metric_definition(selected_metric):
        return METRIC_DEFINITIONS.get(selected_metric, "Definition not available.")
