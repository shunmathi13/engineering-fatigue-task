import json
import math
from pathlib import Path

import pandas as pd


DATA_DIR = Path("/root/data")
RESULTS_DIR = Path("/root/results")


def expected_life(stress_amplitude, mean_stress, fatigue_strength,
                  fatigue_exponent, kt):
    local_amplitude = stress_amplitude * kt
    corrected_amplitude = local_amplitude / (
        1.0 - mean_stress / fatigue_strength
    )

    return 0.5 * (
        corrected_amplitude / fatigue_strength
    ) ** (1.0 / fatigue_exponent)


def test_outputs_exist():
    assert (RESULTS_DIR / "fatigue_analysis.csv").exists()
    assert (RESULTS_DIR / "engineering_report.md").exists()


def test_results_schema_and_values():
    material = pd.read_csv(DATA_DIR / "material_properties.csv")
    loading = pd.read_csv(DATA_DIR / "loading_history.csv")

    with open(DATA_DIR / "component_geometry.json", "r") as f:
        geometry = json.load(f)

    results = pd.read_csv(RESULTS_DIR / "fatigue_analysis.csv")

    required_columns = {
        "cycle_block",
        "nominal_stress_amplitude_mpa",
        "mean_stress_mpa",
        "local_stress_amplitude_mpa",
        "corrected_stress_amplitude_mpa",
        "available_cycles",
        "predicted_cycles_to_failure",
        "critical_block",
    }

    assert required_columns.issubset(results.columns)
    assert len(results) == len(loading)

    fatigue_strength = float(material.iloc[0]["fatigue_strength_mpa"])
    fatigue_exponent = float(material.iloc[0]["fatigue_exponent"])
    kt = float(geometry["stress_concentration_factor"])

    for _, row in loading.iterrows():
        block = int(row["cycle_block"])
        result = results[results["cycle_block"] == block]

        assert len(result) == 1

        result = result.iloc[0]

        nominal = float(row["stress_amplitude_mpa"])
        mean = float(row["mean_stress_mpa"])

        expected_local = nominal * kt
        expected_corrected = expected_local / (
            1.0 - mean / fatigue_strength
        )

        expected = expected_life(
            nominal,
            mean,
            fatigue_strength,
            fatigue_exponent,
            kt,
        )

        assert math.isclose(
            result["local_stress_amplitude_mpa"],
            expected_local,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

        assert math.isclose(
            result["corrected_stress_amplitude_mpa"],
            expected_corrected,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

        assert math.isclose(
            result["predicted_cycles_to_failure"],
            expected,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )


def test_critical_block():
    results = pd.read_csv(RESULTS_DIR / "fatigue_analysis.csv")

    expected_critical = int(
        results.loc[
            results["predicted_cycles_to_failure"].idxmin(),
            "cycle_block",
        ]
    )

    actual_critical = int(results["critical_block"].iloc[0])

    assert actual_critical == expected_critical