import dash
import dash_bootstrap_components as dbc
import altair as alt

from src.data import load_data, get_unique_years
from src.components import create_layout
from src.callbacks import register_callbacks

# Enable VegaFusion for Altair charts
alt.data_transformers.enable("vegafusion")

def main():
    # Load and preprocess data
    df = load_data()
    unique_years = get_unique_years(df)
    continents = df["continent"].unique()
    
    # Initialize the app with Bootstrap styling
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "Longevity Visualizer"
    server = app.server
    
    # Set up the layout
    app.layout = create_layout(unique_years, continents)
    
    # Register callbacks
    register_callbacks(app, df)
    
    return app

if __name__ == "__main__":
    app = main()
    app.server.run(debug=False)