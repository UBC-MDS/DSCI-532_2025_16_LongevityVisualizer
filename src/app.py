import dash
import dash_bootstrap_components as dbc
import altair as alt
import os
import sys

# Get the project root directory (parent of src/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.cache_config import cache 
from src.data import load_data, get_unique_years, load_geodata
from src.components import create_layout
from src.callbacks import register_callbacks

# Enable VegaFusion for Altair charts
alt.data_transformers.enable("vegafusion")

# Initialize the app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Longevity Visualizer"
server = app.server  # Define server at module level for Gunicorn to find
cache.init_app(server) #Initialize the caching

def main():
    # Load and preprocess data
    df = load_data()
    unique_years = get_unique_years(df)
    continents = df["continent"].unique()
    geo_data = load_geodata()

    # Set up the layout
    app.layout = create_layout(unique_years, continents)

    # Register callbacks
    register_callbacks(app, df, geo_data)

    return app


# Execute main function to configure the app
app = main()

if __name__ == "__main__":
    app.run_server(debug=False)  # Use run_server instead of server.run
