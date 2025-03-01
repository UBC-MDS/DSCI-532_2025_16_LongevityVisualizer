# Longevity Visualizer App Reflection

## Implemented Features

In this milestone, we implemented the core components of our Longevity Visualizer dashboard. Users can filter data by continent, country, metric, and year to explore global longevity trends. 

At the top, we implemented three cards summarizing key statistics as well as their , including average longevity, average GDP per capita, and average service worker percentage. These cards display both current values and percentage changes from the previous year, providing clearer insights. 

The dashboard features four key visualizations:
- A choropleth map displaying life expectancy worldwide for the selected year. 
- A scatter plot showing the relationship between GDP per capita and life expectancy, with bubble size representing CO₂ emissions, color representing continents, and tooltips showing additional metrics. 
- A line chart tracking the historical trend of a selected metric for a specific country.
- A second line chart showing the trend of the selected metric’s average value across multiple selected countries over time. 

## Deviations from the Proposal

Compared to our initial plan, we made the following adjustments:

1. **Added country-level data for line charts**: Since life expectancy varies widely within continents, we included country-level data in the scatter plot and first line chart to provide more detailed insights. 
2. **Replaced the bar chart with a second line chart**: Instead of using a bar chart for continent-level comparisons, we found a line chart better captures trends over time. Since the scatter plot already represents continent-level differences via bubble size, the line chart fills the gap by providing temporal insights. 
3. **Eliminated the second time slider**: Originally, we had two time sliders, but this added complexity. Now, line charts display the full time range, making trend analysis more intuitive. 

### Further implement
1. Input added: country dropdown, which allows users to select specific countries (not just continents) for deeper analysis. 
2. Output added: 
- Country-level line chart: shows metri trends over time for specific countries. 
- Percentage in cards: displays key metrics with year-over-year percentage changes. 

## Intentional deviations from visualization practices

1. **Using a world map as a primary visualization**: Maps are typically supplementary tools, but we believe the choropleth map enhances intuitiveness, making geographic trends clearer.
2. **High color density in the scatter plot**: WSelecting all continents results in a cluttered view, but filtering by continent improves clarity. 
3. **Overlapping lines in the line charts**: With multiple countries or continents selected, the charts can become crowded, but filtering refines visualization.

## Dashboard Strengths

Our dashboard remains highly interactive and flexible, closely aligning with our Milestone 1 proposal.

- Multiple filtering options allow users to explore data from different perspectives.
- Both continent-level and country-level insights allow detailed trend analysis.
- The two line charts—one for country-level and one for continent-level data—effectively highlight long-term trends.

## Limitations and potential future improvements

1. **Map lacks automatic zooming**: When selecting a continent, the map does not zoom in, making country identification difficult. We are working on this. 
2. **Limited customization of the scatter plot**: Currently, GDP per capita is the only available x-axis variable. In future milestones, users will be able to select any metric for the x-axis and bubble size, to visualize the relationship between life expectancy and any other metrics. Due to complexity, this feature is planned for a future version. 
