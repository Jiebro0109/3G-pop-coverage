# 3G-pop-coverage
This is a replication of the 3G network covered population rate calculation following the instructions of Guriev et al. (QJE, 2021)


## Calculation Method

### Compute Population Weight Raster
- For region \( m \), the proportion (weight) of the population in the \( i \)-th grid cell relative to the total population of the region is calculated as follows:

\[
population\ weight_i = \cfrac{number\ of\ people_i}{\sum number\ of\ people_i} = \cfrac{population\ density_i \times 1km^2}{\sum (population\ density_i \times 1km^2)}
\]

### Compute Population-Weighted 3G Coverage Raster
- Compute the population-weighted 3G coverage:

\[
population\ weighted\ 3G\ coverage = population\ weight_i \times 3G\ coverage_i
\]

\[
= \cfrac{population\ density_i \times 1km^2}{\sum (population\ density_i \times 1km^2)} \times 3G\ coverage_i
\]

\[
= \cfrac{population\ density_i}{\sum population\ density_i} \times 3G\ coverage_i
\]

### Compute the 3G-Covered Population Proportion within a Region
- Finally, sum all grids within a region to obtain the proportion of the population covered by 3G:

\[
3G\ covered\ rate = \sum_{i=1}^{n} (population\ weight_i \times 3G\ coverage_i)
\]

\[
= \sum_{i=1}^{n} \left( \cfrac{population\ density_i}{\sum population\ density_i} \times 3G\ coverage_i \right)
\]
