import json
import math
from pathlib import Path

import pandas as pd


DATA_DIR = Path("/root/data")
RESULTS_DIR = Path("/root/results")


def calculate_fatigue_life(stress_amplitude, mean_stress, fatigue_strength,
                           fatigue_exponent, stress_concentration_factor):
    local_amplitude = stress_amplitude * stress_concentration_factor

    # Goodman correction for mean stress
    corrected_amplitude = local_amplitude / (
        1.0 - mean_stress / fatigue_strength
    )

    if corrected_amplitude <= 0:
        raise ValueError("Invalid corrected stress amplitude.")

    # Basquin-type relationship:
    # Sa = Sf * (2N)^b
    cycles_to_failure = 0.5 * (
        corrected_amplitude / fatigue_strength
    ) ** (1.0 / fatigue_exponent)

    return local_amplitude, corrected_amplitude, cycles_to_failure


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    material_file = DATA_DIR / "material_properties.csv"
    loading_file = DATA_DIR / "loading_history.csv"
    geometry_file = DATA_DIR / "component_geometry.json"

    material = pd.read_csv(material_file)
    loading = pd.read_csv(loading_file)

    with open(geometry_file, "r", encoding="utf-8") as f:
        geometry = json.load(f)

    required_material = {
        "yield_strength_mpa",
        "ultimate_strength_mpa",
        "elastic_modulus_gpa",
        "fatigue_strength_mpa",
        "fatigue_exponent",
    }

    required_loading = {
        "cycle_block",
        "stress_amplitude_mpa",
        "mean_stress_mpa",
        "cycles",
    }

    if not required_material.issubset(material.columns):
        raise ValueError("Material data is missing required columns.")

    if not required_loading.issubset(loading.columns):
        raise ValueError("Loading data is missing required columns.")

    if "stress_concentration_factor" not in geometry:
        raise ValueError("Stress concentration factor is missing.")

    kt = float(geometry["stress_concentration_factor"])

    if kt <= 0:
        raise ValueError("Stress concentration factor must be positive.")

    fatigue_strength = float(material.iloc[0]["fatigue_strength_mpa"])
    fatigue_exponent = float(material.iloc[0]["fatigue_exponent"])

    results = []

    for _, row in loading.iterrows():
        nominal_amplitude = float(row["stress_amplitude_mpa"])
        mean_stress = float(row["mean_stress_mpa"])
        applied_cycles = float(row["cycles"])

        if nominal_amplitude <= 0:
            raise ValueError("Stress amplitude must be positive.")

        if applied_cycles <= 0:
            raise ValueError("Cycle count must be positive.")

        local_amplitude, corrected_amplitude, life = calculate_fatigue_life(
            nominal_amplitude,
            mean_stress,
            fatigue_strength,
            fatigue_exponent,
            kt,
        )

        results.append(
            {
                "cycle_block": int(row["cycle_block"]),
                "nominal_stress_amplitude_mpa": nominal_amplitude,
                "mean_stress_mpa": mean_stress,
                "local_stress_amplitude_mpa": local_amplitude,
                "corrected_stress_amplitude_mpa": corrected_amplitude,
                "available_cycles": applied_cycles,
                "predicted_cycles_to_failure": life,
            }
        )

    result_df = pd.DataFrame(results)

    # The most critical block is the one with the smallest predicted life.
    critical_index = result_df["predicted_cycles_to_failure"].idxmin()
    critical = result_df.loc[critical_index]

    result_df["critical_block"] = int(critical["cycle_block"])

    output_csv = RESULTS_DIR / "fatigue_analysis.csv"
    result_df.to_csv(output_csv, index=False)

    report = f"""# Engineering Fatigue Assessment

## Component

Component: {geometry.get("component", "not specified")}

Stress concentration factor: {kt:.3f}

## Critical Condition

Critical loading block: {int(critical["cycle_block"])}

Nominal stress amplitude: {critical["nominal_stress_amplitude_mpa"]:.3f} MPa

Local stress amplitude: {critical["local_stress_amplitude_mpa"]:.3f} MPa

Corrected stress amplitude: {critical["corrected_stress_amplitude_mpa"]:.3f} MPa

Predicted cycles to failure:
{critical["predicted_cycles_to_failure"]:.3f}

## Assessment

The fatigue assessment compares the predicted fatigue life across
the supplied cyclic loading blocks. The loading block with the
smallest predicted cycles to failure is identified as the critical
condition.

The calculation accounts for the supplied stress concentration
factor and mean-stress correction. Results are generated directly
from the supplied material, loading, and geometry data.
"""

    output_report = RESULTS_DIR / "engineering_report.md"
    output_report.write_text(report, encoding="utf-8")

    print(f"Results written to: {output_csv}")
    print(f"Report written to: {output_report}")
    print(
        "Critical block:",
        int(critical["cycle_block"]),
        "Predicted life:",
        float(critical["predicted_cycles_to_failure"]),
    )


if __name__ == "__main__":
    main()