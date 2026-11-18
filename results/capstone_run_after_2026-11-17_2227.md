# Capstone run log (after)

- Produced by: `run_capstone.py::main` · 2026-11-17_2227
- Each trial is a fresh `gunicorn app:app --workers 1` start, rate limiting off
- Criterion 4 baseline: `results/run_2026-11-10_2222_after.md` (Trial 1)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Outage gets a clear 503, never a 500 | 5 of 5, 0 500s | 5/5, 0 500s | 5/5, 0 500s | 5/5, 0 500s | MET |
| 2. Every outage leaves exactly one trace | 5 of 5, 0 decided | 5/5 records, 0 decided | 5/5 records, 0 decided | 5/5 records, 0 decided | MET |
| 3. Outage answer comes back fast | median < 1 s, max < 5 s | median 0.1 ms, max 3245.2 ms | median 0.1 ms, max 2236.0 ms | median 0.1 ms, max 2209.1 ms | MET |
| 4. Guard didn't change normal decisions | all identical to Unit 8 | 15/15 identical | 15/15 identical | 15/15 identical | MET |
| 5. Latency breakdown adds up | 100%, gap <= 1 ms | 15/15, max gap 0.1 ms | 15/15, max gap 0.1 ms | 15/15, max gap 0.1 ms | MET |

## Real output

### Criteria 1 and 2: outage responses and their log records (trial 1)

```json
[
  {
    "status": 503,
    "error": "detector_unavailable",
    "message": "The AI-writing check is temporarily unavailable, so nothing was decided about your post. Please try again later."
  },
  {
    "status": 503,
    "error": "detector_unavailable",
    "message": "The AI-writing check is temporarily unavailable, so nothing was decided about your post. Please try again later."
  },
  {
    "status": 503,
    "error": "detector_unavailable",
    "message": "The AI-writing check is temporarily unavailable, so nothing was decided about your post. Please try again later."
  },
  {
    "status": 503,
    "error": "detector_unavailable",
    "message": "The AI-writing check is temporarily unavailable, so nothing was decided about your post. Please try again later."
  },
  {
    "status": 503,
    "error": "detector_unavailable",
    "message": "The AI-writing check is temporarily unavailable, so nothing was decided about your post. Please try again later."
  }
]
```

```
{"timestamp": "2026-11-18T06:26:36+00:00", "content_id": "07e7963b-0f12-450b-b22e-6b1a8599e1f4", "creator_id": "cap-outage-t1-1", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 3245.2, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:26:36+00:00", "content_id": "f0910674-d71b-4fd9-98f1-949a8954c959", "creator_id": "cap-outage-t1-2", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 0.1, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:26:36+00:00", "content_id": "17ce2bc6-c74b-4b5d-854c-7577fac15486", "creator_id": "cap-outage-t1-3", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 0.1, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:26:36+00:00", "content_id": "b067e950-95b9-4bf3-97ba-fb2879fa8577", "creator_id": "cap-outage-t1-4", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 0.1, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:26:36+00:00", "content_id": "57cd9361-8ec2-428a-9d45-53da23282fce", "creator_id": "cap-outage-t1-5", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 0.1, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
```

### Criterion 3: outage durations in ms, every trial

- trial 1: [3245.2, 0.1, 0.1, 0.1, 0.1]
- trial 2: [2236.0, 0.1, 0.1, 0.1, 0.1]
- trial 3: [2209.1, 0.1, 0.1, 0.1, 0.1]

### Criterion 4: differences from Unit 8 (empty means none)

```json
[
  [],
  [],
  []
]
```

### Criterion 5: first three decision records (trial 1)

```
{"timestamp": "2026-11-18T06:26:44+00:00", "content_id": "f863afee-0a17-45b6-a111-a53c9b4fafb6", "creator_id": "eval_c1 my writin_1", "guess": "unsure", "model_score": 0.8034, "style_score": 0.4791, "combined_score": 0.6412, "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.", "status": "decided", "duration_ms": 6870.5, "stages_ms": {"validate_ms": 0.1, "model_ms": 6870.0, "style_ms": 0.4, "score_ms": 0.0}, "text_chars": 255, "text_preview": "Prayer is one of the 5 pillars of Islam. It is an obligatory ritual that every m"}
{"timestamp": "2026-11-18T06:26:44+00:00", "content_id": "9bb4406f-a48a-4c26-ba04-46fb67de5680", "creator_id": "eval_c1 my writin_2", "guess": "unsure", "model_score": 0.7337, "style_score": 0.6028, "combined_score": 0.6683, "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.", "status": "decided", "duration_ms": 48.8, "stages_ms": {"validate_ms": 0.1, "model_ms": 48.6, "style_ms": 0.2, "score_ms": 0.0}, "text_chars": 195, "text_preview": "I am going to Morocco in March for a week to attend my nephews wedding. I am fly"}
{"timestamp": "2026-11-18T06:26:44+00:00", "content_id": "db2b6fd4-7d6f-4540-9bb1-78ddc949ac22", "creator_id": "eval_c1 my writin_3", "guess": "human", "model_score": 0.342, "style_score": 0.3626, "combined_score": 0.3523, "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.", "status": "decided", "duration_ms": 91.3, "stages_ms": {"validate_ms": 0.1, "model_ms": 91.0, "style_ms": 0.2, "score_ms": 0.0}, "text_chars": 261, "text_preview": "Allah bless you!!!! Let me write to you tomorrow or the next day, and let  you k"}
```
