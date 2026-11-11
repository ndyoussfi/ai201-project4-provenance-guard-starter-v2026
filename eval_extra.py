#!/usr/bin/env python3
"""
The parts of my criteria that run_eval.py can't test by sending text to /submit.

    python app.py                               # in one terminal
    python run_eval.py --label before           # first
    python eval_extra.py --label before         # then this

It does four things, three trials each where a trial makes sense:

  1. Numbers for criteria 1, 3 and 4, read from the run_eval report with the
     same label (count of "likely AI", the two averages, label counts).
  2. Criterion 2: 10 appeals on real content_ids from that run, plus 3 made-up
     ids, checked against the response AND GET /log.
  3. Criterion 4: exact scores fed straight into scoring.score_to_label.
  4. Criterion 5: no bad-input request was logged as a decision, and /ping
     still answers.

It prints the numbers. It does not decide MET or MISSED; I do that.
"""

import argparse
import datetime as dt
import json
import re
import sys
import uuid

import config
import scenarios
import scoring

URL = f"http://{config.HOST}:{config.PORT}"
TRIALS = 3

# The exact scores from criterion 4. 0.40 and 0.70 are added because my
# thresholds moved there after the criterion was written.
BOUNDARY_SCORES = [0, 0.34, 0.35, 0.36, 0.64, 0.65, 0.66, 1, 0.40, 0.70]


def latest_run(label):
    runs = sorted(config.RESULTS_DIR.glob(f"run_*_{label}.md"))
    if not runs:
        sys.exit(f"No results/run_*_{label}.md. Run run_eval.py --label {label} first.")
    return runs[-1]


def read_trials(path):
    """Pull each scenario's per-trial JSON back out of a run_eval report."""
    text = path.read_text(encoding="utf-8")
    out = {}
    for section in re.split(r"^### ", text, flags=re.M)[1:]:
        name = section.splitlines()[0].strip()
        blocks = re.findall(r"```json\n(.*?)\n```", section, flags=re.S)
        out[name] = [json.loads(b) for b in blocks]
    return out


def summary(path):
    trials = read_trials(path)
    mine = trials["c1 my writing"]
    ai = trials["c3 clearly AI"]
    n_casual = len(scenarios.MY_CASUAL)
    lines = [f"Read from `{path.relative_to(config.ROOT)}`.", ""]

    lines += ["**Criterion 1:** how many of my 10 pieces got \"likely AI\" (target: at most 1)", ""]
    for t, results in enumerate(mine, 1):
        flagged = [i for i, r in enumerate(results, 1) if r.get("guess") == "ai"]
        lines.append(f"- Trial {t}: {len(flagged)} of {len(results)}"
                     + (f" (pieces {', '.join(map(str, flagged))})" if flagged else ""))

    lines += ["", "**Criterion 3:** average combined score, AI minus human (target: at least 0.3)", ""]
    for t in range(len(mine)):
        human = [r["confidence"] for r in mine[t][:n_casual]]
        bot = [r["confidence"] for r in ai[t]]
        h, a = sum(human) / len(human), sum(bot) / len(bot)
        lines.append(f"- Trial {t + 1}: AI {a:.4f}, human {h:.4f}, gap {a - h:.4f}")

    lines += ["", "**Criterion 4:** label counts across all 15 submitted pieces (target: at least 2 each)", ""]
    for t in range(len(mine)):
        counts = {"human": 0, "unsure": 0, "ai": 0}
        for r in mine[t] + ai[t]:
            if r.get("guess") in counts:
                counts[r["guess"]] += 1
        lines.append(f"- Trial {t + 1}: human {counts['human']}, unsure {counts['unsure']}, "
                     f"likely AI {counts['ai']}")
    return lines


def boundaries():
    lines = ["**Criterion 4:** exact scores into `scoring.py::score_to_label`", "",
             "| score | guess | error |", "|---|---|---|"]
    for score in BOUNDARY_SCORES:
        try:
            guess, label = scoring.score_to_label(score)
            ok = guess in ("human", "unsure", "ai") and bool(label)
            lines.append(f"| {score} | {guess} | {'' if ok else 'not one of the three'} |")
        except Exception as exc:  # noqa: BLE001
            lines.append(f"| {score} | | {type(exc).__name__}: {exc} |")
    return lines


def appeals(requests):
    log = requests.get(f"{URL}/log").json()["entries"]
    appealed = {e["content_id"] for e in log if e.get("event") == "appeal"}
    # Real content_ids from the eval run, newest first, never appealed before.
    real = [e for e in reversed(log)
            if e.get("status") == "decided"
            and str(e.get("creator_id", "")).startswith(("eval_c1", "eval_c3"))
            and e["content_id"] not in appealed]
    if len(real) < 10 * TRIALS:
        sys.exit(f"Only {len(real)} unappealed eval decisions in the log; need {10 * TRIALS}.")

    lines = ["**Criterion 2:** appeals (target: 10 of 10 real pass, 3 of 3 fake return 404 and log nothing)", ""]
    examples = []
    for t in range(TRIALS):
        batch = real[t * 10:(t + 1) * 10]
        passed, fails = 0, []
        for i, original in enumerate(batch, 1):
            cid = original["content_id"]
            reasoning = f"Trial {t + 1}, appeal {i}: I wrote this myself."
            r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": reasoning})
            body = r.json()
            after = requests.get(f"{URL}/log").json()["entries"]
            mine = [e for e in after if e.get("content_id") == cid]
            checks = {
                "200": r.status_code == 200,
                "returns content_id": body.get("content_id") == cid,
                "returns under_review": body.get("status") == "under_review",
                "appeal in log with reasoning": any(e.get("event") == "appeal"
                                                    and e.get("reasoning") == reasoning for e in mine),
                "original unchanged": original in mine,
                "status now under_review": mine[-1].get("status") == "under_review",
            }
            if all(checks.values()):
                passed += 1
            else:
                fails.append(f"{cid}: " + ", ".join(k for k, v in checks.items() if not v))
            if t == 0 and i == 1:
                examples += ["", "Example (trial 1, appeal 1). Response:", "", "```json",
                             json.dumps(body, indent=2), "```", "",
                             "Log entries for that content_id afterward:", "", "```json",
                             json.dumps(mine, indent=2), "```"]

        before = len(requests.get(f"{URL}/log").json()["entries"])
        fake_404 = 0
        for _ in range(3):
            r = requests.post(f"{URL}/appeal", json={"content_id": str(uuid.uuid4()),
                                                     "reasoning": "This id was made up."})
            fake_404 += r.status_code == 404
        after = len(requests.get(f"{URL}/log").json()["entries"])

        lines.append(f"- Trial {t + 1}: real {passed} of 10 passed; fake {fake_404} of 3 returned 404; "
                     f"log entries written by fakes: {after - before}")
        lines += [f"  - failed: {f}" for f in fails]
    return lines + examples


def bad_input(requests):
    # Only string ids. The attack run left one entry whose creator_id is a dict (RQ06).
    bad_ids = {b["creator_id"] for s in scenarios.SCENARIOS
               if s["name"] == "c5 bad input" for b in s["bodies"] if "creator_id" in b}
    log = requests.get(f"{URL}/log").json()["entries"]
    decisions = [e for e in log if e.get("status") == "decided"
                 and (e.get("creator_id") is None
                      or (isinstance(e.get("creator_id"), str) and e["creator_id"] in bad_ids))]
    rejections = [e for e in log if e.get("event") == "rejected"
                  and isinstance(e.get("creator_id"), str) and e["creator_id"] in bad_ids]
    ping = requests.post(f"{URL}/ping", json={"message": "still alive?"})
    return ["**Criterion 5:** after the bad requests (the 400s are in the run_eval report)", "",
            f"- Decisions logged for the bad-input requests: {len(decisions)}",
            f"- Rejections logged for them instead: {len(rejections)}",
            f"- /ping afterward: {ping.status_code} {json.dumps(ping.json())}"]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", default="before")
    args = parser.parse_args()
    import requests

    run = latest_run(args.label)
    lines = [f"# Extra checks: {args.label}", "",
             "- Produced by: `eval_extra.py::main`",
             f"- {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for part in (summary(run), boundaries(), bad_input(requests), appeals(requests)):
        lines += part + [""]

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"extra_{stamp}_{args.label}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
