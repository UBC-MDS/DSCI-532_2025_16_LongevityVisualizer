import pandas as pd
import geopandas as gpd
from src.cache_config import cache  

import os
import pandas as pd


@cache.memoize()
def load_data():
    """Load and preprocess the Gapminder dataset, saving it as a Parquet file."""
    parquet_path = "data/processed/gapminder_data.parquet"
    
    # Load the parquet data
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)

    # Preprocessing raw data
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
    
    # Save to Parquet for future use
    os.makedirs("data/processed", exist_ok=True)  # Ensure the directory exists
    df.to_parquet(parquet_path, engine="pyarrow", index=False)
    
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

@cache.memoize()
def load_geodata():
    geo_df = gpd.read_file("data/processed/gapminder.json")

    return geo_df