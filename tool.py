"""Randomly sample supported Marketplace Search records and profile fit."""
import json
import os
import sys
from urllib.request import Request, urlopen


def profile_records(records):
    fields = sorted({key for row in records for key in row})
    coverage = {}
    for field in fields:
        present = sum(row.get(field) not in (None, "", [], {}) for row in records)
        coverage[field] = {"present": present, "missing": len(records) - present, "coverage": round(present / len(records), 3) if records else 0}
    return {"record_count": len(records), "field_coverage": coverage, "decision_note": "Coverage describes only this returned sample; it is not a guarantee about the full dataset."}


def estimate_dataset_cost(records, dollars_per_thousand=2.5):
    if records < 0 or dollars_per_thousand < 0:
        raise ValueError("records and rate must be non-negative")
    return round(records * dollars_per_thousand / 1000, 6)


def sample_linkedin_people(api_key, query, size=20):
    # Dataset Search currently supports three LinkedIn datasets; people profiles is documented.
    if not 1 <= size <= 1000:
        raise ValueError("size must be between 1 and 1000")
    payload = {"size": size, "sort": "random", "filter": {"name": "name", "operator": "includes", "value": query}}
    request = Request("https://api.brightdata.com/datasets/search/gd_l1viktl72bvl7bjuj0", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urlopen(request, timeout=45) as response:
        return json.load(response)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 tool.py SAMPLE.json | --live NAME_FRAGMENT")
    if sys.argv[1] == "--live":
        if len(sys.argv) != 3 or not os.getenv("BRIGHT_DATA_API_KEY"):
            raise SystemExit("Set BRIGHT_DATA_API_KEY and provide a name fragment")
        response = sample_linkedin_people(os.environ["BRIGHT_DATA_API_KEY"], sys.argv[2])
        result = profile_records(response.get("hits", []))
        result["total_hits"] = response.get("total_hits")
        result["sample_cost_estimate_usd"] = estimate_dataset_cost(result["record_count"])
    else:
        with open(sys.argv[1], encoding="utf-8") as source:
            records = json.load(source)
        result = profile_records(records)
        result["sample_cost_estimate_usd"] = estimate_dataset_cost(result["record_count"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
