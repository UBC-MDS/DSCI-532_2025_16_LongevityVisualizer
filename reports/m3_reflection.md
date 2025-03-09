# Longevity Visualizer App Reflection

## Implemented Features

### App Refinements

The widgets are functional with no obvious bugs.

We updated our map and bubble charts to Altair, improving interactivity and visual appeal. With this update, the map now automatically zooms into a selected continent, providing a more focused view. Additionally, users can click on the map to dynamically update other visualizations. Previously, we used Plotly Express, but it lacked the seamless zooming and interactive capabilities Altair offers. This change in visualization library is reflected on the bubble chart too.

Our updated dashboard now contains

1)  A clickable chloropleth map displaying life expectancy worldwide. The map can be used for filtering our scatter plot and line chart.
2)  A scatter plot linking a selected metric to life expectancy, with bubble size representing CO₂ emissions.
3)  A line chart showing the historical trend of a selected metric for a specific country.
4)  A second line chart showing the selected metric’s average trend across multiple selected continents over time.

### From Joel's Feedback

Joel suggested multiple changes to make.

The first major change suggested was to make the x-axis variable in the bubble chart selectable. This was suggested in order to allow users to visualize life expectancy versus different metrics on the bubble chart.

The second major change was to make the map clickable so that it updates the bottom line chart, bubble chart, and the dropdown. This was implemented as suggested.

The first minor change was to change our colour scheme. We had an orange and white colour scheme and we decided to go with a cyan colour instead.

The second minor change was adjusting the y-axis minimum in the bubble chart to start at the minimum life expectancy, improving resolution.

### Peer Inspiration (Challenging Part)

For the challenging part of this project, we were inspired by the summary cards [Group 17](https://dsci-532-2025-17-pharma-spend-dashboard.onrender.com) had. They implemented a system where an increase from previous years turned the text green, while a decrease turned it red. We changed our cards to do something similar so that the card footers would turn red if there was a decrease in any of the metrics compared to the previous year and turn green if there's an increase in the metric compared to the previous year.

## Deviations from Best Practices

1)  The colour theme across charts is not unified. For example, in the bubble chart green corresponds to Europe, while red corresponds to Europe in another chart. This will be addressed in future milestones.

2)  Previously listed deviations can be found in the [Milestone 2 Reflection](https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer/blob/main/reports/m2_reflection.md).

## Deviations from the Proposal

1)  The metrics selected by the bottom drop-down menu no longer only control the bottom two visualizations. Our bubble chart will now be modified depending on the selection of metrics in the drop-down menu.

2)  Summary cards now show a percentage change compared to previous years.

3)  Clicking on the map now changes the country dropdown menu and changes the two line charts and bubble charts to correspond to the selected country.

4)  Changes previously mentioned in [m2_reflection.md](https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer/blob/main/reports/m2_reflection.md).

These changes were all implemented as they make the dashboard more intuitive and increase interactivity.

## Dashboard Strengths

Our dashboard allows us to visualize multiple metrics across different continents and countries.

1)  Map shows detailed information on discrepancies between continents in terms of life expectancy.

2)  Bubble chart allows exploration of trends for certain metrics.

3)  Line charts convey long term trend information.

4)  Continent and country level insights are provided.

## Limitations and potential future improvements / corner cases

1)  We need to make it more clear if we can, as to which drop-down menus correspond to which charts. We will look into this for Milestone 4.

2)  Some countries contain missing data and hence do not show up on the map. For example, Venezuela. We will look into other Gapminder datasets to see if the country is contained in the dataset. If no data exists, we could introduce a placeholder row to ensure the country remains visible on the map, even if specific metrics are unavailable.

3)  Currently clicking on our map only allows us to select one country at a time. We would like to implement the ability to select multiple countries.