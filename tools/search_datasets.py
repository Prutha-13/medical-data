import csv
import argparse
from pathlib import Path


def load_datasets(csv_path: Path):
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def filter_datasets(datasets, modality=None, task=None, disease=None, year_min=None, year_max=None):
    results = []
    for ds in datasets:
        if modality and ds["modality"].lower() != modality.lower():
            continue
        if task and ds["task"].lower() != task.lower():
            continue
        if disease and disease.lower() not in ds["disease"].lower():
            continue
        if year_min and ds["year"]:
            try:
                if int(ds["year"]) < year_min:
                    continue
            except ValueError:
                pass
        if year_max and ds["year"]:
            try:
                if int(ds["year"]) > year_max:
                    continue
            except ValueError:
                pass
        results.append(ds)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Search and filter medical datasets from datasets.csv"
    )
    parser.add_argument("--csv", default="data/datasets.csv", help="Path to datasets CSV")
    parser.add_argument("--modality", help="Filter by modality (image, text, tabular, time-series, etc.)")
    parser.add_argument("--task", help="Filter by task (classification, segmentation, etc.)")
    parser.add_argument("--disease", help="Filter by disease keyword (e.g., cancer, ICU, brain, etc.)")
    parser.add_argument("--year-min", type=int, help="Minimum year (e.g., 2016)")
    parser.add_argument("--year-max", type=int, help="Maximum year (e.g., 2024)")

    args = parser.parse_args()

    csv_path = Path(args.csv)
    datasets = load_datasets(csv_path)
    results = filter_datasets(
        datasets,
        modality=args.modality,
        task=args.task,
        disease=args.disease,
        year_min=args.year_min,
        year_max=args.year_max,
    )

    if not results:
        print("No datasets matched your filters.")
        return

    print(f"Found {len(results)} dataset(s):\n")
    for ds in results:
        print(f"- {ds['name']} ({ds['year']})")
        print(f"  Modality: {ds['modality']} | Task: {ds['task']} | Disease: {ds['disease']}")
        print(f"  Link: {ds['link']}")
        if ds.get("notes"):
            print(f"  Notes: {ds['notes']}")
        print()


if __name__ == "__main__":
    main()
