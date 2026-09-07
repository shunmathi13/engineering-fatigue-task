# Author Notes

The solution looks at how the notched mechanical component behaves under repeated loading. It checks for signs of fatigue over time.

It starts by reading in the material properties loading conditions and details about the component. Then it calculates the stress using the stress concentration factor. After that it applies a mean-stress correction to get accurate results.

For each loading block the solution estimates how long the component will last before failing due to fatigue. The block, with the predicted life is considered the most critical one.

Finally all results are saved into CSV files and an engineering report. The solution is built to handle whatever input data is provided. It does not rely on hardcoded values. Expect specific test outcomes.
