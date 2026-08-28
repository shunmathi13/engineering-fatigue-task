Analyze the fatigue behaviour of a notched mechanical component subjected to cyclic loading using the data provided in `/root/data`.

The material, loading, and component data describe a mechanically loaded component for which fatigue performance must be assessed. Determine the relevant stress state at the critical region, account for the supplied geometric stress concentration information, and evaluate the component's cyclic response using the material data provided.

Estimate the fatigue life of the component under the specified loading conditions. Your analysis should distinguish between the applied nominal loading and the local stress state at the notch and should use the supplied material fatigue information consistently.

Check the input data for physical or numerical inconsistencies before relying on the results. Where intermediate quantities are required for the final assessment, retain them so that the calculation can be independently reviewed.

Write the final engineering results to `/root/results/fatigue_analysis.csv` and provide a concise interpretation in `/root/results/engineering_report.md`. The CSV should contain the key calculated quantities and the predicted fatigue life. The report should explain the resulting fatigue assessment, identify the critical condition, and state any important assumptions or limitations supported by the supplied data.

The results should be reproducible from the supplied input files.