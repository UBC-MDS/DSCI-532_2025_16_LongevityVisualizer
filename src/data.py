import pandas as pd

def load_data():
    """Load and preprocess the Gapminder dataset."""
    df = pd.read_csv("data/raw/gapminder_data_graphs.csv")
    df = df.dropna(
        subset=[
            "country",
            "continent",
            "year",
            "life_exp",
            "hdi_index",
            "co2_consump",
            "gdp",
            "services",
        ]
    )
    return df

def get_unique_years(df, step=4):
    """Get unique years from dataset with a specified step."""
    return sorted(df["year"].unique())[::step]

# Constants for metrics
METRIC_OPTIONS = [
    {"label": "Life Expectancy", "value": "life_exp"},
    {"label": "HDI", "value": "hdi_index"},
    {"label": "CO2 Emissions per Person (tonnes)", "value": "co2_consump"},
    {"label": "GDP per Capita (USD)", "value": "gdp"},
    {"label": "Service Workers Percentage (%)", "value": "services"},
]

METRIC_LABELS = {
    "life_exp": "Life Expectancy",
    "hdi_index": "HDI",
    "co2_consump": "CO2 Emissions per Person (tonnes)",
    "gdp": "GDP per Capita (USD)",
    "services": "Service Workers Percentage (%)",
}

# Continent color mapping for consistent visualization
CONTINENT_COLORS = {
    "Africa": "#1f77b4",  # Blue
    "Asia": "#ff7f0e",  # Orange
    "Europe": "#2ca02c",  # Green
    "North America": "#d62728",  # Red
    "Oceania": "#9467bd",  # Purple
    "South America": "#8c564b",  # Brown
}