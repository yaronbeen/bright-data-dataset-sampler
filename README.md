# Bright Data Dataset Sampler

Profile a filtered random sample from Bright Data's Marketplace Dataset Search API before building a downstream workflow. It helps a data buyer or marketing-ops analyst assess whether the returned fields may be useful enough to justify a larger query or integration. It is an exploratory schema-fit check, not lead generation or dataset-quality certification, and its sample is not statistically representative of the dataset.

## Synthetic Example -> Decision

The invented `sample.json` has three records. Its field coverage report shows `name` in all records, `industry` in two, and `employees` in two. An analyst can decide to test a downstream segmentation using `name` and `country`, while treating `industry` and `employees` as incomplete in this sample. No account or actual person data is included.

## Workflow

1. Choose a Marketplace dataset currently supported by the Search endpoint.
2. Apply a narrow filter, request a random-sort sample, and cap the requested size. This is an exploratory API sample, not a statistically designed sample.
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

Live mode filters people-profile records by the supplied name fragment, requests up to 20 (or a hard-bounded maximum of 1,000) with `sort: random`, then profiles only fields present in those returned records. This random-sort response is exploratory and must not be treated as statistically representative of dataset-wide quality, field prevalence, or completeness. The profile is of the filtered sample, not the whole dataset. It may incur charges. No credentials are stored. The programmatic method accepts an injected API key.

## Outputs

JSON contains sample record count, per-field present/missing counts and coverage ratio, and a caveat. The live output additionally includes `total_hits` and a cost estimate based on current documented Marketplace pricing. The estimate is informational, not billing data.

## Differentiation

Bright Data repos already cover collection pipelines, general scrapers, lead/outreach generation, SERP research, and social analytics. This project sits before those workflows: it samples a supported Marketplace dataset and reports observed field completeness so an operator can make a dataset-fit decision. It does not collect URLs, export a prospect list, score people, or analyze marketing performance. It uses Marketplace Dataset Search, rather than Web Scraper API scraping or SERP API.

## FAQ

**Can Search sample any of the 250+ datasets?** No. The docs currently list three supported LinkedIn datasets for Search. Use the Filter endpoint for other datasets or bulk/file-driven jobs; this demo intentionally does not silently switch APIs.

**Does this report schema completeness for the entire dataset?** No. It reports the fields and missing values in one random sample only.

**Is the price estimate guaranteed?** No. It multiplies returned sample records by the currently documented CPM. Check the account and current pricing.

## Compliance and limitations

This project is an independent demonstration and is not affiliated with, endorsed by, or an official product of Bright Data or LinkedIn.

The people-profile dataset contains identifiable personal data. Use it only for the narrow purpose described here: an exploratory assessment of whether the returned fields may fit a contemplated dataset integration. Having account access or generating a sample does not grant permission to use, contact, profile, enrich, export, or otherwise repurpose personal data. Before use, confirm that your use is authorized and complies with the applicable Bright Data Marketplace and dataset terms, LinkedIn/platform terms, and all applicable data-protection and privacy laws and obligations, including any required lawful basis, transparency, purpose limitation, data minimization, security, and retention/deletion requirements. This README is not legal advice.

Avoid retaining raw personal-data records. Prefer synthetic fixtures or aggregate field-presence counts; if raw data must be handled temporarily for an authorized assessment, restrict access and delete it promptly under your retention policy and applicable obligations. The sample fixture is synthetic. API `sort: random` results may reflect filtering, index coverage, field availability, and other selection effects. Treat observed field coverage as descriptive only of the returned response: it does not establish dataset-wide quality, completeness, or field prevalence, and a sampled absence is not proof that a field is absent across the dataset.

## Bright Data

Powered by [Bright Data Marketplace Dataset API](https://docs.brightdata.com/api-reference/marketplace-dataset-api/overview). MIT licensed.
