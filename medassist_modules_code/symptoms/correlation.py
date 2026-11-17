
from pathlib import Path
import pandas as pd

DATASET_PATH = Path(__file__).resolve().parent / "data" / "sample_symptom_dataset.csv"


def _truthy(value):
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"1", "1.0", "yes", "true", "y"}


def analyse_symptoms(selected_names):
    """Calculate descriptive symptom frequencies and co-occurrence statistics."""

    if not DATASET_PATH.exists():
        return {
            "dataset_loaded": False,
            "message": "Dataset file is missing.",
            "symptom_frequency": {},
            "pairwise_associations": [],
            "matching_records": 0,
        }

    frame = pd.read_csv(DATASET_PATH)

    if "disease" not in frame.columns:
        raise ValueError("Dataset must contain a 'disease' column.")

    available = {
        column.lower(): column
        for column in frame.columns
        if column.lower() != "disease"
    }

    normalized = [
        name.lower().replace(" ", "_")
        for name in selected_names
    ]

    missing = [
        name for name in normalized
        if name not in available
    ]

    if missing:
        raise ValueError(
            "Selected symptom(s) are not present in the analysis dataset: "
            + ", ".join(missing)
        )

    selected_cols = [available[name] for name in normalized]

    binary = frame[selected_cols].apply(
        lambda column: column.map(_truthy)
    )

    frequencies = {
        name: int(binary[column].sum())
        for name, column in zip(selected_names, selected_cols)
    }

    pairs = []

    for i in range(len(selected_cols)):
        for j in range(i + 1, len(selected_cols)):
            a = selected_cols[i]
            b = selected_cols[j]

            both = int((binary[a] & binary[b]).sum())
            either = int((binary[a] | binary[b]).sum())

            jaccard = round(both / either, 3) if either else 0.0

            pairs.append({
                "symptom_1": selected_names[i],
                "symptom_2": selected_names[j],
                "co_occurrence_count": both,
                "jaccard_similarity": jaccard,
            })

    all_match_count = (
        int(binary.all(axis=1).sum())
        if selected_cols else 0
    )

    return {
        "dataset_loaded": True,
        "dataset_rows": int(len(frame)),
        "symptom_frequency": frequencies,
        "pairwise_associations": pairs,
        "matching_records": all_match_count,
        "note": (
            "Descriptive dataset associations only; "
            "not a diagnosis or disease prediction."
        ),
    }
