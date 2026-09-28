# Bright Data Dataset Sampler

Profile a filtered random sample from Bright Data's Marketplace Dataset Search API before building a downstream workflow. It helps a data buyer or marketing-ops analyst decide whether the returned fields are useful enough to justify a larger query or integration. It is a schema-fit check, not lead generation or dataset-quality certification.

## Synthetic Example -> Decision

The invented `sample.json` has three records. Its field coverage report shows `name` in all records, `industry` in two, and `employees` in two. An analyst can decide to test a downstream segmentation using `name` and `country`, while treating `industry` and `employees` as incomplete in this sample. No account or actual person data is included.

## Workflow

1. Choose a Marketplace dataset currently supported by the Search endpoint.
2. Apply a narrow filter, randomize the returned sample, and cap the requested size.
3. Inspect per-field coverage and the price estimate for returned records.
4. Decide whether a larger integration test is warranted; do not generalize sample coverage to the whole dataset.

## Setup

Python 3.10+; standard library only.

```bash
cp .env.example .env
export BRIGHT_DATA_API_KEY="your-key"
```

Official documentation: [Marketplace Dataset API overview](https://docs.brightdata.com/api-reference/marketplace-dataset-api/overview) and [Search endpoint](https://docs.brightdata.com/api-reference/marketplace-dataset-api/search-dataset). Search is currently documented for three LinkedIn datasets; this demo uses the people-profile dataset `gd_l1viktl72bvl7bjuj0` and a filtered random sample. Dataset Search costs are currently documented at $2.5 CPM; rates may change, so verify before use.

## Run

```bash
python3 tool.py sample.json
BRIGHT_DATA_API_KEY="your-key" python3 tool.py --live "marketing"
python3 -m unittest -v
```

Live mode filters people-profile records by the supplied name fragment, requests up to 20 (or a hard-bounded maximum of 1,000) with `sort: random`, then profiles only fields present in those returned records. The profile is of the filtered sample, not the whole dataset. It may incur charges. No credentials are stored. The programmatic method accepts an injected API key.

## Outputs

JSON contains sample record count, per-field present/missing counts and coverage ratio, and a caveat. The live output additionally includes `total_hits` and a cost estimate based on current documented Marketplace pricing. The estimate is informational, not billing data.

## Differentiation

Bright Data repos already cover collection pipelines, general scrapers, lead/outreach generation, SERP research, and social analytics. This project sits before those workflows: it samples a supported Marketplace dataset and reports observed field completeness so an operator can make a dataset-fit decision. It does not collect URLs, export a prospect list, score people, or analyze marketing performance. It uses Marketplace Dataset Search, rather than Web Scraper API scraping or SERP API.

## FAQ

**Can Search sample any of the 250+ datasets?** No. The docs currently list three supported LinkedIn datasets for Search. Use the Filter endpoint for other datasets or bulk/file-driven jobs; this demo intentionally does not silently switch APIs.

**Does this report schema completeness for the entire dataset?** No. It reports the fields and missing values in one random sample only.

**Is the price estimate guaranteed?** No. It multiplies returned sample records by the currently documented CPM. Check the account and current pricing.

## Compliance and limitations

Use only authorized datasets and account access. Random results can be biased by index coverage and field availability. The sample fixture is synthetic. Minimize retained data and follow applicable data-protection obligations; do not treat a sampled absence as proof that a field is absent across a dataset.

## Bright Data

Powered by [Bright Data Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/overview). MIT licensed.
