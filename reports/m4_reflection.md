# Longevity Visualizer App Reflection

## Implemented Features

### App Refinements

This week, we focused on improving the map, cards, and several small details to enhance usability and interactivity.

For the map, we addressed missing data by coloring countries with no available data in gray instead of leaving them blank. This makes it clear which regions lack information. We also updated the middle card, replacing average GDP per capita with average population to provide a broader view of the selected area. Additionally, we modified the third card to dynamically display the average value and growth percentage of the selected metric, making it more informative. To improve clarity, we added metric explanations when users select them from the dropdown.
Beyond these main changes, we refined various design elements. We standardized continent colors across charts to improve consistency and readability. Borders were removed from all charts to match the style of the map and scatter plot. We also fixed minor layout issues, such as zooming inconsistencies and aligning card titles with the dashboard title.

### From Joel's Feedback

Joel’s feedback led to several improvements:

1. Major changes:

- Missing countries are now colored gray instead of being removed from the map.
- The third card now updates dynamically to reflect the selected metric.

2. Minor changes:

- Cursor changes to a pointer when hovering over interactive elements.
- Removed excess white space above cards and aligned card titles with the dashboard title.
- Standardized legends across line charts.
- Removed redundant “USD” or dollar signs from chart labels.

All suggested changes were implemented, making the dashboard more intuitive and polished.

## Deviations from Best Practices

1. The country-level line charts use a similar color scheme with the continent's color in scatter and continent-level line charts, which may cause confusion.
2. Previously listed deviations can be found in the [Milestone 2 Reflection](https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer/blob/main/reports/m2_reflection.md).

## Deviations from the Proposal

1. The middle card now displays average population and growth percentage, while the third card dynamically updates based on the selected metric.
2. Clicking on the map now updates the country dropdown, reflecting the change in the two line charts and scatter plot.
3. Changes previously mentioned in [m3_reflection.md](https://github.com/UBC-MDS/DSCI-532_2025_16_LongevityVisualizer/blob/main/reports/m3_reflection.md).

These adjustments improved the dashboard’s usability and interactivity.

## Dashboard Strengths

Our dashboard effectively visualizes multiple metrics across different regions.

1. Interactive charts and summary cards allow users to explore data from different perspectives.
2. Both continent-level and country-level insights help with detailed trend analysis.
3. The clickable map provides a smooth user experience.

## Limitations and potential future improvements / corner cases

1. Currently, users can only select one country at a time by clicking on the map. Allowing multiple country selection would improve usability.

2. The map lacks zoom functionality, making it difficult to focus on small countries. Adding zoom controls would enhance navigation.

### Insights and feedback useful 

Peer feedback was extremely helpful in refining our dashboard, especially in improving chart readability, color consistency, and interactions. Their user perspective helped us catch small but important details we might have overlooked. More high-quality Dash examples and best practices would be valuable for future development. Additionally, guidance on handling large datasets efficiently would help improve responsiveness.
