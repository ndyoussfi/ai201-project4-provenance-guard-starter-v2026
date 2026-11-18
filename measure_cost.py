"""Capstone M3: measure what one /submit run costs, in seconds of compute.

Start the app fresh first (so run 0 is a real cold start), with rate limiting off:
    AI201_RATE_LIMITS=0 gunicorn app:app --bind 127.0.0.1:5000 --workers 1
Then, in another terminal:
    python measure_cost.py
"""
import json
import statistics
import sys
import time
from pathlib import Path

import requests

URL = "http://127.0.0.1:5000/submit"
LOG = Path("logs/audit.jsonl")
OUT = Path("results/capstone_cost_m3.txt")
RUNS = 10
CREATOR = "m3-cost"
TEXT = (
    "The committee reviewed the proposal over several weeks and raised concerns "
    "about the budget. After a long discussion they agreed to fund a smaller pilot "
    "first and revisit the full plan next spring."
)


def main():
    sent = []
    for i in range(RUNS + 1):  # run 0 is the cold start, reported on its own
        start = time.perf_counter()
        r = requests.post(URL, json={"text": TEXT, "creator_id": CREATOR}, timeout=120)
        client_ms = round((time.perf_counter() - start) * 1000, 1)
        if r.status_code != 200:
            sys.exit(f"run {i}: HTTP {r.status_code} {r.text[:200]}")
        sent.append((i, r.json()["content_id"], client_ms))

    logged = {}
    for line in LOG.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        if entry.get("creator_id") == CREATOR:
            logged[entry.get("content_id")] = entry

    lines = ["run  server_ms  model_ms  client_ms"]
    warm_server, warm_client = [], []
    for i, content_id, client_ms in sent:
        entry = logged[content_id]
        server_ms = entry["duration_ms"]
        model_ms = entry["stages_ms"]["model_ms"]
        lines.append(f"{i:>3}  {server_ms:>9}  {model_ms:>8}  {client_ms:>9}")
        if i > 0:
            warm_server.append(server_ms)
            warm_client.append(client_ms)

    lines += [
        "",
        f"cold start (run 0): server {logged[sent[0][1]]['duration_ms']} ms",
        f"warm average over runs 1-{RUNS}: server {statistics.mean(warm_server):.1f} ms, "
        f"client {statistics.mean(warm_client):.1f} ms",
        f"warm range: server {min(warm_server)}-{max(warm_server)} ms",
        f"text: {len(TEXT)} chars, same text every run",
        "API spend: $0, no tokens. GPT-2 runs on the local CPU (Intel Mac, x86_64).",
    ]
    report = "\n".join(lines)
    OUT.write_text(report + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()