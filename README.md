# Longevity Visualizer: Explore Global Health & Economic Trends

Welcome to **Longevity Visualizer**, an interactive dashboard that lets you explore global trends in life expectancy, human development, CO2 consumption, GDP, and services. Built on the Gapminder dataset, our platform offers insightful visualizations that help researchers, policymakers, and curious minds alike understand the factors driving global well-being.

---

## For Dashboard Users

### Why Longevity Visualizer?

In today’s rapidly changing world, access to comprehensive and interactive data visualizations is essential. Longevity Visualizer empowers you by providing:

- **Interactive Map Visualization:**  
  Discover life expectancy across countries using an intuitive choropleth map. Higher color intensity represents higher life expectancy, and clicking on a country reveals detailed statistics.

- **Bubble Chart Analysis:**  
  Explore the relationship between life expectancy and GDP per capita. The bubble sizes indicate CO2 consumption, helping you gauge environmental impact alongside economic metrics.

- **Comparative Trend Analysis:**  
  Use our bottom section to select metrics such as HDI, CO2, Life Expectancy, or Services (%) and compare these values across multiple countries via line charts.

Dive into the dashboard to uncover patterns and insights that can inform decisions and spark discussions about global development.

If you encounter any issues or have questions, please open an issue on our GitHub repository.

---

## Getting Started

Begin your journey by exploring our dashboard and discovering global trends today!
## Usage Instructions
Check out the [Dashboard](https://dsci-532-2025-16-longevityvisualizer.onrender.com) deployed on Render!

![Demo GIF](img/demo.gif)

The gif above outlines an overview of the dashboard.

To select a continent, use the corresponding drop-down menu. The corresponding cards and map and bubble charts will change depending on this selection.

To select a year to view data for, use the slider. 

To select a metric and country, use the dropdown slider. The corresponding line charts will change depending on this selection. 

---

## For Developers and Contributors

Interested in contributing to **Longevity Visualizer**? We welcome your help to enhance and expand the platform. Here’s how you can get started:

### Check out Contributing Guidelines

First, check out our [Contributing Guidelines](https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer/blob/main/CONTRIBUTING.md) before contributing to this project.

### Running the App Locally

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer.git

2. **Navigate to the Project Directory:**
    ```bash
    cd DSCI-532_2025_16_LongevityVisualizer

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Run the application:** 
    ```bash
    python -m src.app

## License

`longevity_visualizer` was created by Long Nguyen, Zhiwei Zhang, Abdul Safdar, and Chukwunonso Ebele-Muolokwu. It is licensed under the terms of the MIT license.

## Credits

`longevity_visualizer` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
