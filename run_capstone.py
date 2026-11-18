#!/usr/bin/env python3
"""
Capstone Milestone 5: run the five capstone criteria (criteria.md) three times each.

    python run_capstone.py

Stop any app you have running first. This starts and stops its own gunicorn
server on port 5055 for every trial, so each trial is a fresh start:

  - outage trials (criteria 1, 2, 3): AI201_DETECTOR_MODEL=does-not-exist,
    then 5 valid /submit requests
  - normal trials (criteria 4, 5): the real gpt2 model, then every input in
    scenarios.py, compared to the Unit 8 after-run

Rate limiting is off in both (AI201_RATE_LIMITS=0) so a 429 can't hide a result.
Writes results/capstone_run_<label>_<timestamp>.md and prints the run log table.
"""

import argparse
import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

import requests

import scenarios
from run_eval import bodies_for

PORT = 5055
URL = f"http://127.0.0.1:{PORT}"
LOG = Path("logs/audit.jsonl")
BASELINE = Path("results/run_2026-11-10_2222_after.md")
TRIALS = 3
OUTAGE_REQUESTS = 5
COMPARED = ("guess", "confidence", "model_score", "style_score")
STAGES = ("validate_ms", "model_ms", "style_ms", "score_ms")
TEXT = (
    "The committee reviewed the proposal over several weeks and raised concerns "
    "about the budget. After a long discussion they agreed to fund a smaller pilot "
    "first and revisit the full plan next spring."
)


# ── server and log helpers ───────────────────────────────────────────────────

def start_server(model):
    env = dict(os.environ, AI201_DETECTOR_MODEL=model, AI201_RATE_LIMITS="0")
    proc = subprocess.Popen(
        [sys.executable, "-m", "gunicorn", "app:app",
         "--bind", f"127.0.0.1:{PORT}", "--workers", "1", "--timeout", "120"],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(150):
        try:
            requests.get(f"{URL}/health", timeout=1)
            return proc
        except requests.RequestException:
            time.sleep(0.2)
    proc.kill()
    sys.exit(f"gunicorn didn't answer on port {PORT}. Is something else using it?")


def stop_server(proc):
    proc.terminate()
    proc.wait(timeout=15)


def log_length():
    if not LOG.exists():
        return 0
    return len(LOG.read_text(encoding="utf-8").splitlines())


def log_since(start):
    lines = LOG.read_text(encoding="utf-8").splitlines()[start:]
    return [json.loads(line) for line in lines]


def post(body):
    response = requests.post(f"{URL}/submit", json=body, timeout=120)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:200]}
    return response.status_code, payload


# ── the two kinds of trial ───────────────────────────────────────────────────

def outage_trial(trial):
    """Criteria 1, 2, 3: fresh server with a model that doesn't exist."""
    proc = start_server("does-not-exist")
    try:
        start = log_length()
        responses = [post({"text": TEXT, "creator_id": f"cap-outage-t{trial}-{i}"})
                     for i in range(1, OUTAGE_REQUESTS + 1)]
        entries = log_since(start)
    finally:
        stop_server(proc)

    clear = [s == 503 and p.get("error") == "detector_unavailable"
             and "nothing was decided" in p.get("message", "")
             for s, p in responses]
    crashes = sum(s == 500 for s, _ in responses)
    c1 = {"passed": sum(clear), "of": len(responses), "crashes": crashes}
    c1["ok"] = c1["passed"] == c1["of"] and crashes == 0

    unavailable = [e for e in entries if e.get("status") == "unavailable"]
    decided = [e for e in entries if e.get("status") == "decided"]
    complete = [e for e in unavailable
                if all(e.get(k) is not None
                       for k in ("creator_id", "error", "duration_ms", "text_chars"))]
    n503 = sum(s == 503 for s, _ in responses)
    c2 = {"records": len(unavailable), "complete": len(complete), "of": n503,
          "decided": len(decided)}
    c2["ok"] = (len(unavailable) == n503 == len(complete) == OUTAGE_REQUESTS
                and not decided)

    durations = [e["duration_ms"] for e in unavailable]
    c3 = {"durations": durations,
          "median": statistics.median(durations) if durations else None,
          "max": max(durations) if durations else None}
    c3["ok"] = bool(durations) and c3["median"] < 1000 and c3["max"] < 5000

    return {"c1": c1, "c2": c2, "c3": c3, "responses": responses, "entries": entries}


def normal_trial(baseline):
    """Criteria 4, 5: fresh server with gpt2, every scenario input."""
    proc = start_server("gpt2")
    try:
        start = log_length()
        results = {}
        for scenario in scenarios.SCENARIOS:
            results[scenario["name"]] = [post(body) for body in bodies_for(scenario)]
        entries = log_since(start)
    finally:
        stop_server(proc)

    same, compared, diffs = 0, 0, []
    for name, base_rows in baseline.items():
        for i, base in enumerate(base_rows):
            if base.get("status") != 200:
                continue  # bad input in Unit 8: nothing was scored
            compared += 1
            status, now = results[name][i]
            if status == 200 and all(now.get(k) == base.get(k) for k in COMPARED):
                same += 1
            else:
                diffs.append({"scenario": name, "input": i + 1, "status": status,
                              "now": {k: now.get(k) for k in COMPARED},
                              "unit8": {k: base.get(k) for k in COMPARED}})
    c4 = {"same": same, "of": compared, "diffs": diffs, "ok": same == compared > 0}

    decided = [e for e in entries if e.get("status") == "decided"]
    good, gaps = 0, []
    for e in decided:
        stages = e.get("stages_ms") or {}
        has_fields = (all(e.get(k) is not None
                          for k in ("duration_ms", "text_chars", "text_preview"))
                      and all(k in stages for k in STAGES))
        gap = round(e["duration_ms"] - sum(stages.get(k, 0) for k in STAGES), 1) \
            if has_fields else None
        gaps.append(gap)
        if has_fields and abs(gap) <= 1.0:
            good += 1
    c5 = {"good": good, "of": len(decided),
          "max_gap": max((abs(g) for g in gaps if g is not None), default=None),
          "ok": good == len(decided) > 0}

    return {"c4": c4, "c5": c5, "entries": decided}


def load_baseline():
    """Trial 1 of each scenario in the Unit 8 after-run (all three trials matched)."""
    text = BASELINE.read_text(encoding="utf-8")
    baseline = {}
    for section in re.split(r"^### ", text, flags=re.M)[1:]:
        name = section.splitlines()[0].strip()
        match = re.search(r"\*\*Trial 1\*\*\s*```json\s*(.*?)```", section, re.S)
        if match:
            baseline[name] = json.loads(match.group(1))
    return baseline


# ── report ───────────────────────────────────────────────────────────────────

def cells(trials, key, fmt):
    return [fmt(t[key]) for t in trials]


def verdict(trials, key):
    return "MET" if all(t[key]["ok"] for t in trials) else "MISSED"


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", default="before")
    args = parser.parse_args()

    baseline = load_baseline()
    outage, normal = [], []
    for trial in range(1, TRIALS + 1):
        print(f"trial {trial}: outage...", flush=True)
        outage.append(outage_trial(trial))
        print(f"trial {trial}: normal...", flush=True)
        normal.append(normal_trial(baseline))

    rows = [
        ("1. Outage gets a clear 503, never a 500", "5 of 5, 0 500s",
         cells(outage, "c1", lambda c: f"{c['passed']}/{c['of']}, {c['crashes']} 500s"),
         verdict(outage, "c1")),
        ("2. Every outage leaves exactly one trace", "5 of 5, 0 decided",
         cells(outage, "c2", lambda c: f"{c['complete']}/{c['of']} records, {c['decided']} decided"),
         verdict(outage, "c2")),
        ("3. Outage answer comes back fast", "median < 1 s, max < 5 s",
         cells(outage, "c3", lambda c: f"median {c['median']} ms, max {c['max']} ms"),
         verdict(outage, "c3")),
        ("4. Guard didn't change normal decisions", "all identical to Unit 8",
         cells(normal, "c4", lambda c: f"{c['same']}/{c['of']} identical"),
         verdict(normal, "c4")),
        ("5. Latency breakdown adds up", "100%, gap <= 1 ms",
         cells(normal, "c5", lambda c: f"{c['good']}/{c['of']}, max gap {c['max_gap']} ms"),
         verdict(normal, "c5")),
    ]
    table = ["| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
             "|---|---|---|---|---|---|"]
    table += [f"| {name} | {target} | {' | '.join(runs)} | {v} |"
              for name, target, runs, v in rows]

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out = Path(f"results/capstone_run_{args.label}_{stamp}.md")
    report = [
        f"# Capstone run log ({args.label})",
        "",
        f"- Produced by: `run_capstone.py::main` · {stamp}",
        "- Each trial is a fresh `gunicorn app:app --workers 1` start, rate limiting off",
        f"- Criterion 4 baseline: `{BASELINE}` (Trial 1)",
        "",
        *table,
        "",
        "## Real output",
        "",
        "### Criteria 1 and 2: outage responses and their log records (trial 1)",
        "",
        "```json",
        json.dumps([{"status": s, **p} for s, p in outage[0]["responses"]], indent=2),
        "```",
        "",
        "```",
        *[json.dumps(e, ensure_ascii=False) for e in outage[0]["entries"]],
        "```",
        "",
        "### Criterion 3: outage durations in ms, every trial",
        "",
        *[f"- trial {i}: {t['c3']['durations']}" for i, t in enumerate(outage, 1)],
        "",
        "### Criterion 4: differences from Unit 8 (empty means none)",
        "",
        "```json",
        json.dumps([t["c4"]["diffs"] for t in normal], indent=2),
        "```",
        "",
        "### Criterion 5: first three decision records (trial 1)",
        "",
        "```",
        *[json.dumps(e, ensure_ascii=False) for e in normal[0]["entries"][:3]],
        "```",
        "",
    ]
    out.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(table))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
