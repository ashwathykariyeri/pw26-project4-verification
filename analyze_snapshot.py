"""Reproduce the repository-level descriptive analysis from the frozen archive."""
from collections import Counter
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "reproducibility"
OUT = ROOT / "tables"
OUT.mkdir(exist_ok=True)

def load_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def save_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

sample = load_csv(DATA / "sample.csv")
obs = json.loads((DATA / "raw/run_model_observations.json").read_text(encoding="utf-8"))
reviews = {r["repo"]:r for r in load_csv(DATA / "review_models.csv")}
frame = json.loads((DATA / "raw/catalogue.json").read_text(encoding="utf-8"))
rank = {}
for item in frame["models"]:
    if isinstance(item["id"], str) and item["id"] and type(item["downloads"]) is int and item["downloads"] >= 0:
        rank.setdefault(item["id"], item["downloads"])
ranked = sorted(rank, key=lambda key: (-rank[key], key.casefold(), key))
assert len(rank) == 436004 and len(sample) == len(obs) == 300
assert set(obs) == {r["repo"] for r in sample}
assert set(ranked[:150]) == {r["repo"] for r in sample if r["cohort"] == "top_downloads"}
rng = random.Random(42)
bands = [ranked[i * len(ranked) // 4:(i + 1) * len(ranked) // 4] for i in range(4)]
stratified = {repo for i, band in enumerate(bands) for repo in rng.sample(band, 37 + (i < 2))}
assert stratified == {r["repo"] for r in sample if r["cohort"] == "stratified"}


detail = []
for r in sample:
    repo = r["repo"]
    o, review = obs[repo], reviews[repo]
    assert o.get("revision", "") == review["revision"]
    meta = o.get("metadata", {})
    tags = [tag for tag in meta.get("tags", []) if isinstance(tag, str)]
    card_status = o.get("card_status")
    probe = o.get("weight_probe_status")
    provider_payload = o.get("provider_listing") or {}
    mapping = provider_payload.get("inferenceProviderMapping")
    provider_state = ("observed" if isinstance(mapping, dict) else "unavailable")
    if not isinstance(mapping, dict):
        mapping = {}
    live = sorted(k for k, v in mapping.items() if isinstance(v, dict) and v.get("status") == "live")
    base = sorted({tag.rsplit(":", 1)[1].casefold() for tag in tags if tag.startswith("base_model:")
                   and "/" in tag.rsplit(":", 1)[1]})
    detail.append(dict(**r, revision=o.get("revision", ""), card_status=card_status,
        licence_tags="|".join(sorted({t[8:] for t in tags if t.startswith("license:")})),
        declared_direct_bases="|".join(base), namespace=repo.split("/", 1)[0].casefold(),
        access_gate=meta.get("gated"), weight_probe_status=probe, provider_mapping=provider_state,
        listed_live_providers="|".join(live), reviewed_developer=review["developer"],
        reviewed_parent=review["corporate_parent"], reviewed_licence=review["licence"]))

def shares_summary(counts):
    total = sum(counts.values())
    return (len(counts), sum((v/total)**2 for v in counts.values()) if total else None)

summaries, licence_counts, provider_counts = [], [], []
for cohort in ("stratified", "top_downloads"):
    rows = [row for row in detail if row["cohort"] == cohort]
    assert len(rows) == 150
    bases, providers = Counter(), Counter()
    for row in rows:
        for value, counter in ((row["declared_direct_bases"], bases), (row["listed_live_providers"], providers)):
            if value:
                labels=value.split("|")
                for label in labels:
                    counter[label] += 1/len(labels)
    namespace_n, namespace_hhi = shares_summary(Counter(row["namespace"] for row in rows))
    parent_n, parent_hhi = shares_summary(bases)
    provider_n, provider_hhi = shares_summary(providers)
    summaries.append(dict(cohort=cohort,n=len(rows),card_ok=sum(r["card_status"]==200 for r in rows),
      license_tag_n=sum(bool(r["licence_tags"]) for r in rows),
      declared_base_n=sum(bool(r["declared_direct_bases"]) for r in rows),
      distinct_declared_bases=parent_n, direct_base_hhi=parent_hhi,
      namespaces=namespace_n, namespace_hhi=namespace_hhi,
      gated_n=sum(r["access_gate"] in {"auto","manual",True} for r in rows),
      weight_http_2xx_n=sum(200<= (r["weight_probe_status"] or 0)<300 for r in rows),
      weight_probe_observed_n=sum(r["weight_probe_status"] is not None for r in rows),
      provider_mapping_n=sum(r["provider_mapping"]=="observed" for r in rows),
      listed_live_provider_n=sum(bool(r["listed_live_providers"]) for r in rows),
      multiple_listed_live_provider_n=sum("|" in r["listed_live_providers"] for r in rows),
      distinct_listed_live_providers=provider_n, listed_provider_hhi=provider_hhi,
      reviewed_developer_n=sum(bool(r["reviewed_developer"]) for r in rows),
      reviewed_parent_n=sum(bool(r["reviewed_parent"]) for r in rows),
      reviewed_licence_n=sum(bool(r["reviewed_licence"]) for r in rows)))
    for tag, n in sorted(Counter(r["licence_tags"] or "(missing)" for r in rows).items()):
        licence_counts.append(dict(cohort=cohort,tag=tag,n=n))
    for name, weight in sorted(providers.items()):
        provider_counts.append(dict(cohort=cohort,provider=name,fractional_count=weight))

save_csv(OUT/"cohort_summary.csv",summaries)
save_csv(OUT/"repository_observations.csv",detail)
save_csv(OUT/"licence_tags.csv",licence_counts)
save_csv(OUT/"provider_listings.csv",provider_counts)
print(json.dumps(summaries,indent=2))
