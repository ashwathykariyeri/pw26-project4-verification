# Who Controls the Deployment Stack of Open-Weight AI Models?

**PW26 Project 4 · Verification archive and replication code**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24139183.svg)]
https://zenodo.org/records/24139183

Target journal: *Telecommunications Policy* (Elsevier)
Course: Interdisciplinary Elective "AI, Power & Responsibility: Governing Intelligence"
Supervisor: Prof. Dr. Raja Hashim Ali
Team: **Team ChatGPT** — Aswathy Kariyeri and Anish Dadaji Khobragade

---

## Overview

Publishing model weights widens the options for reuse, but actually *deploying* a model can still depend on upstream checkpoints, the rights granted by a licence, compatible runtimes and hardware, and a hosting operator. This project asks whether the apparent abundance of open-weight models on Hugging Face corresponds to genuinely independent, feasible deployment options.

The study applies the "AI as distributed computing" perspective of Mueller (2025) to repository-level evidence. It joins Hugging Face repository metadata (declared lineage, licence tags, gating, provider listings) to revision-pinned evidence, and keeps what is *observed* separate from what is *verified* and from what is *unknown*.

> **Anchor paper:** Mueller, M. L. (2025). It's just distributed computing: Rethinking AI governance. *Telecommunications Policy, 49*(3), 102917. https://doi.org/10.1016/j.telpol.2025.102917

### Research questions

| | Question |
|---|---|
| **RQ1** | How concentrated are developer and hosting dependencies in the sampled repositories? |
| **RQ2** | How often do models with downloadable weights face restrictive licence terms or unusually demanding deployment resources? |
| **RQ3** | Does apparent diversity shrink after accounting for shared base-model lineage and verified corporate ownership? |
| **RQ4** | Which interoperability or portability measures could reduce the dependencies observed in the sample? |

---

## Status and scope (please read first)

This archive supports a **descriptive analysis of repository metadata and provider visibility**. It is **not** a finished empirical study.

- The **automated stage is complete and reproducible**: catalogue capture, sampling, revision-level observation of all 300 repositories, and the descriptive tables below.
- The **manual deployment-evidence review is exploratory and small** (14 repositories with a verified developer, 3 with verified corporate ownership, 3 with a documented route, 0 with verified weight evidence). Results for RQ1–RQ4 that depend on this review **should not be interpreted as sample-level findings**.
- The run manifest records `"publication_ready": false`. Independent evidence review, double-coding and a complete manuscript are still required.
- The numbers in the original proposal document and slides are **synthetic ("dummy") values** that illustrate reporting format only. None of them are results.

---

## Data and method

| Item | Value |
|---|---|
| Source | Hugging Face Hub API, exact `text-generation` filter |
| Frame captured | 10 Nov 2026, 16:33–16:36 UTC (437 pages) |
| Eligible repositories in frame | **436,004** (0 dropped or duplicate rows) |
| Ranking | Downloads (descending), stable tie-break on repository ID |
| Cohort A — *stratified* | 150 repositories, 4 download-rank quartiles (38, 38, 37, 37), simple random sampling within each quartile, **seed 42** |
| Cohort B — *top downloads* | The 150 most downloaded repositories (sensitivity cohort) |
| Cohort overlap | 0 repositories (300 unique) |
| Observations per repository | Commit SHA, metadata, model card at that commit, provider listing, one revision-pinned anonymous HEAD probe of a candidate weight file |

Design notes:

1. **Sample before checking access**, so gating, missing artifacts and failed observations stay visible.
2. **Lineage is a declaration.** `base_model:` tags are model-card claims, not verified ancestry.
3. **A weight probe shows reachability of one artifact only.** It does not establish complete, usable weights (shards, adapters and external base weights need review).
4. **Provider listings are leads**, not verified routes. A missing listing does not imply exclusivity.
5. **Download counts measure platform activity**, not use or importance.
6. Concentration is measured with the Herfindahl–Hirschman Index (HHI) using **fractional incidence**: a repository with several bases or providers contributes one unit split equally across them.

---

## Repository contents

```
.
├── README.md
├── Project4_Final_Executed.ipynb   # executed notebook (offline replay of the frozen sample)
├── analyze_snapshot.py             # reproduces the repository-level descriptive tables
├── reproducibility/
│   ├── sample.csv                  # the 300 sampled repositories and their cohort
│   ├── review_models.csv           # manual evidence review: developer, parent, weights, licence, VRAM
│   ├── review_routes.csv           # manual evidence review: documented deployment routes
│   ├── review_lineage.csv          # manual evidence review: verified lineage
│   ├── raw/
│   │   ├── catalogue.json          # frozen catalogue (436,004 eligible repositories)
│   │   ├── run_model_observations.json
│   │   └── <hash>.json             # raw per-repository API captures
│   └── outputs/                    # notebook outputs (graph, summaries, run_manifest.json)
└── tables/                         # created by analyze_snapshot.py
    ├── cohort_summary.csv
    ├── repository_observations.csv
    ├── licence_tags.csv
    └── provider_listings.csv
```

---

## Reproducing the results

Both the notebook and the script use only the **Python standard library**, and the replay runs **offline** from the frozen archive (no Hugging Face access needed).

**1. Get the code and data**

```bash
git clone https://github.com/ashwathykariyeri/pw26-project4-verification.git
cd pw26-project4-verification
```

**2. Reproduce the descriptive tables**

```bash
python analyze_snapshot.py
```

The script first **asserts** that the archive is internally consistent: the frame holds 436,004 eligible repositories, the sample has 300 repositories, the top-download cohort equals the first 150 ranked repositories, and the stratified cohort is regenerated exactly from seed 42. It then writes the four CSV files to `tables/` and prints the cohort summary.

**3. Replay the full notebook**

Open `Project4_Final_Executed.ipynb` from the repository root and run all cells. The notebook builds the multilayer dependency graph (CSV and GraphML), computes the RQ1–RQ4 outputs, runs consistency checks, and writes `reproducibility/outputs/run_manifest.json`, which includes SHA-256 hashes of the raw inputs and review files.

> The notebook has a `MODE` switch (`"live"` or `"fixture"`) and a `REPLAY` flag. For replay keep `REPLAY = True`; it will refuse to fetch anything and will fail loudly if archived inputs are missing. `"fixture"` mode runs the pipeline on synthetic data as a software test only.

---

## Results from the frozen sample

Output of `analyze_snapshot.py` (150 repositories per cohort):

| Measure | Stratified | Top downloads |
|---|---:|---:|
| Model card retrieved (HTTP 200) | 137 | 149 |
| Has a licence tag | 86 | 145 |
| Declares a direct base model | 75 | 84 |
| Distinct declared base models | 80 | 68 |
| Direct-base HHI | 0.0146 | 0.0181 |
| Distinct namespaces | 145 | 55 |
| Namespace HHI | 0.0072 | 0.0899 |
| Access-gated | 2 | 5 |
| Weight probe observed / returned HTTP 2xx | 142 / 140 | 150 / 145 |
| Provider listing retrieved | 150 | 149 |
| Has ≥1 listed live provider | 3 | 51 |
| Has ≥2 listed live providers | 0 | 14 |
| Distinct listed live providers | 1 | 12 |
| Listed-provider HHI | 1.00* | 0.531 |
| Manually reviewed: developer / corporate parent / licence | 2 / 0 / 2 | 12 / 3 / 14 |

\* Based on only 3 repositories and a single provider, so this value is not informative about concentration.

**How to read these numbers**

- The top-download cohort is far more concentrated by **namespace** (55 distinct vs. 145) and is much more likely to be visible through provider listings (51 vs. 3 repositories).
- Declared-base HHI is low in both cohorts, but this reflects **declared** lineage only, and only about half of each cohort declares a base model.
- Provider figures describe **listed** options on one platform at capture time. They do not show who actually serves a model or that a model depends on any provider.
- The manual review covers 14 of 300 repositories, so no verified-ownership, verified-weights, licence-restriction or route-loss rate is reported as a finding.

---

## Reviewing evidence

Every affirmative manual finding must carry an official HTTPS URL, an observation date, a reviewer and a short evidence note, checked against the recorded commit. Unknown values are left blank or coded `unknown`.

| File | One row per | Key fields |
|---|---|---|
| `review_models.csv` | model | `developer`, `corporate_parent`, `weights` (`downloadable`/`gated`/`unavailable`/`unknown`), `licence` (`permissive`/`restrictive`/`unknown`), `min_vram_gib` |
| `review_routes.csv` | model × route × runtime | `route` (`independent_host`/`developer_host`/`self_host`), `operator`, `runtime`, `url` |
| `review_lineage.csv` | child–parent link | `relationship`, `parent`, `parent_set_complete` |

Analytical choices: more than 24 GiB aggregate VRAM (batch 1, 2,048-token context, lowest documented compatible precision) is the illustrative resource threshold, with 16 and 48 GiB as sensitivity thresholds. For RQ4, operators are removed one at a time and models that lose every documented route are counted; local routes count as fallbacks.

---

## Limitations

- Results describe this frozen sample (captured 10 Nov 2026) and are not claims about the whole Hub.
- Model-card declarations, licence tags and provider listings are unverified platform metadata.
- Deployment evidence coverage is currently very low; missing evidence is reported as unknown, never as absence.
- A reachable weight file does not prove complete weights; documented portability does not prove tested interoperability.
- Double-coding, agreement statistics (raw agreement and Cohen's kappa on a 30-record subset) and the capped portability pilot described in the proposal have **not** been completed.

---

## Citation

If you use this archive, please cite the Zenodo record:

> Kariyeri, A., & Khobragade, A. D. (2026). *Who controls the deployment stack of open-weight AI models? PW26 Project 4 verification archive* [Data set and code]. Zenodo. https://doi.org/10.5281/zenodo.24139183

```bibtex
@misc{kariyeri_khobragade_2026_project4,
  author    = {Kariyeri, Aswathy and Khobragade, Anish Dadaji},
  title     = {Who controls the deployment stack of open-weight AI models?
               PW26 Project 4 verification archive},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24139183},
  url       = {https://doi.org/10.5281/zenodo.24139183}
}
```

## References

1. Mueller, M. L. (2025). It's just distributed computing: Rethinking AI governance. *Telecommunications Policy, 49*(3), 102917. https://doi.org/10.1016/j.telpol.2025.102917
2. Laufer, B., Oderinwale, H., & Kleinberg, J. (2025). Anatomy of a Machine Learning Ecosystem: 2 Million Models on Hugging Face. https://arxiv.org/abs/2508.06811
3. Stalnaker, T., et al. (2025). An Empirical Analysis of Machine Learning Model and Dataset Documentation, Supply Chain, and Licensing Challenges on Hugging Face. https://arxiv.org/abs/2502.04484
4. Longpre, S., et al. (2025). Economies of Open Intelligence: Tracing Power & Participation in the Model Ecosystem. https://arxiv.org/abs/2512.03073
5. Suryani, M. A., et al. (2025). Hugging Face Model Cards Metadata Dataset (v4). Zenodo. https://doi.org/10.5281/zenodo.15125488

The full reference list is in the project proposal.

## Licence

*Add a licence before making the repository public* (for example MIT for the code and CC BY 4.0 for the data and documentation), and make sure it matches the licence selected on the Zenodo record.

## Contact

Aswathy Kariyeri — [github.com/ashwathykariyeri](https://github.com/ashwathykariyeri)
