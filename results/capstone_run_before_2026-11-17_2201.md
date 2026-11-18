# Capstone run log (before)

- Produced by: `run_capstone.py::main` · 2026-11-17_2201
- Each trial is a fresh `gunicorn app:app --workers 1` start, rate limiting off
- Criterion 4 baseline: `results/run_2026-11-10_2222_after.md` (Trial 1)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Outage gets a clear 503, never a 500 | 5 of 5, 0 500s | 5/5, 0 500s | 5/5, 0 500s | 5/5, 0 500s | MET |
| 2. Every outage leaves exactly one trace | 5 of 5, 0 decided | 5/5 records, 0 decided | 5/5 records, 0 decided | 5/5 records, 0 decided | MET |
| 3. Outage answer comes back fast | median < 1 s, max < 5 s | median 99.0 ms, max 2597.2 ms | median 100.6 ms, max 2216.7 ms | median 100.2 ms, max 2296.7 ms | MET |
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
{"timestamp": "2026-11-18T06:01:10+00:00", "content_id": "82a95753-77e3-41ac-8be4-fc4a46dd44e4", "creator_id": "cap-outage-t1-1", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 2597.2, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:01:10+00:00", "content_id": "539d5c6b-a21b-4c9e-84fd-aa0275b30670", "creator_id": "cap-outage-t1-2", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 95.3, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:01:10+00:00", "content_id": "7096ac2f-f1e3-40a0-92ce-f93ce3156110", "creator_id": "cap-outage-t1-3", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 90.4, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:01:10+00:00", "content_id": "39f64db9-4c25-479f-b556-aa4e258ed0a3", "creator_id": "cap-outage-t1-4", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 99.0, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
{"timestamp": "2026-11-18T06:01:11+00:00", "content_id": "cfc85ea6-0afe-49d0-8cf3-0070a60a4979", "creator_id": "cap-outage-t1-5", "guess": null, "model_score": null, "style_score": null, "combined_score": null, "label": null, "status": "unavailable", "event": "detector_unavailable", "error": "Couldn't load 'does-not-exist': does-not-exist is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'", "duration_ms": 106.5, "text_chars": 197, "text_preview": "The committee reviewed the proposal over several weeks and raised concerns about"}
```

### Criterion 3: outage durations in ms, every trial

- trial 1: [2597.2, 95.3, 90.4, 99.0, 106.5]
- trial 2: [2216.7, 100.6, 99.3, 106.5, 91.2]
- trial 3: [2296.7, 100.2, 94.0, 104.8, 91.4]

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
{"timestamp": "2026-11-18T06:01:15+00:00", "content_id": "a7090587-312f-4b11-b74f-e7d333d8ac49", "creator_id": "eval_c1 my writin_1", "guess": "unsure", "model_score": 0.8034, "style_score": 0.4791, "combined_score": 0.6412, "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.", "status": "decided", "duration_ms": 4172.6, "stages_ms": {"validate_ms": 0.1, "model_ms": 4171.9, "style_ms": 0.5, "score_ms": 0.0}, "text_chars": 255, "text_preview": "Prayer is one of the 5 pillars of Islam. It is an obligatory ritual that every m"}
{"timestamp": "2026-11-18T06:01:15+00:00", "content_id": "fb66cd34-ec70-4cb0-a680-d44b992931d5", "creator_id": "eval_c1 my writin_2", "guess": "unsure", "model_score": 0.7337, "style_score": 0.6028, "combined_score": 0.6683, "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.", "status": "decided", "duration_ms": 67.8, "stages_ms": {"validate_ms": 0.1, "model_ms": 67.5, "style_ms": 0.2, "score_ms": 0.0}, "text_chars": 195, "text_preview": "I am going to Morocco in March for a week to attend my nephews wedding. I am fly"}
{"timestamp": "2026-11-18T06:01:16+00:00", "content_id": "4f3eaf0c-fc28-4c71-b3d1-fa4cc1bedf49", "creator_id": "eval_c1 my writin_3", "guess": "human", "model_score": 0.342, "style_score": 0.3626, "combined_score": 0.3523, "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.", "status": "decided", "duration_ms": 75.7, "stages_ms": {"validate_ms": 0.1, "model_ms": 75.4, "style_ms": 0.2, "score_ms": 0.0}, "text_chars": 261, "text_preview": "Allah bless you!!!! Let me write to you tomorrow or the next day, and let  you k"}
```
