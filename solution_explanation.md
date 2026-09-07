# Solution Explanation

The solution reads the supplied material properties, loading history, and component geometry data.

It determines the local stress amplitude at the notch by applying the supplied stress concentration factor to the nominal stress amplitude.

The solution then applies the mean-stress correction and uses the supplied fatigue relationship to estimate the predicted cycles to failure for each loading block.

The calculations are performed for all supplied loading blocks. The block with the smallest predicted fatigue life is identified as the critical loading condition.

The calculated results are written to `results/fatigue_analysis.csv`, and the engineering interpretation is written to `results/engineering_report.md`.

The implementation also checks that the required input data and stress concentration information are available and that the supplied stress and cycle values are valid.
