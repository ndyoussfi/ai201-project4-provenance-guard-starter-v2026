# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 22:22
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `155124da-f477-4016-9019-ccd9955207ea` | unsure | 0.423 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `bba50b35-fe00-45fa-8c66-73815cc26cd2` | unsure | 0.455 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `23c12fc6-fef8-4d66-a141-647a32a14ffd` | unsure | 0.588 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ccb1101a-fe55-45b6-bbfb-eb275a3237c1` | unsure | 0.637 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `14b8783e-11e6-4f90-bb4d-261ed18bf512` | human | 0.345 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a2022801-bca3-4361-9064-e5c24323e164` | human | 0.395 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `43b6f9af-8697-453a-95bf-a06a3137e169` | unsure | 0.616 |  |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f2b3da1a-915a-4f06-8717-5959bf6836df` | unsure | 0.600 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `fba93f56-d197-4196-a260-ff05a00cee1b` | ai | 0.839 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f65e3105-442d-492d-bfe6-232579b9ea50` | unsure | 0.591 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `92fc3d04-dd91-4933-b8e6-748881aa22a7` | unsure | 0.720 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d8006277-e816-4974-97c6-551f767d9f41` | unsure | 0.732 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `40d11ec7-d0a1-4418-93fa-b75905febe87` | unsure | 0.718 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `27fd89d2-d7c8-4165-864c-d8f50c923ca8` | unsure | 0.744 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `a50eb421-68a8-48b9-8862-1a5feda38317` | unsure | 0.704 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `6a1336b8-4bce-4e92-aefe-4b8c29137436` | unsure | 0.659 |  |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `e6990b99-4520-490c-8eba-fd4b7ef49796` | unsure | 0.439 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `466b08c8-ee2f-43e1-85e4-2c023a4b7d95` | human | 0.289 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `67204e75-e2c2-4f05-812e-5c2e0fedc3a1` | unsure | 0.576 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `484bd887-e94b-482d-b3e5-fdf29fa5df90` | unsure | 0.505 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1b3d16da-7329-4443-90f7-163aeac62b3a` | unsure | 0.482 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `109b5242-6873-4d01-b8af-0fe90aed3de1` | unsure | 0.566 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "155124da-f477-4016-9019-ccd9955207ea",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4229,
  "model_score": 0.1635,
  "style_score": 0.6824,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "bba50b35-fe00-45fa-8c66-73815cc26cd2",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4545,
  "model_score": 0.5943,
  "style_score": 0.3146,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "23c12fc6-fef8-4d66-a141-647a32a14ffd",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5878,
  "model_score": 0.6662,
  "style_score": 0.5094,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ccb1101a-fe55-45b6-bbfb-eb275a3237c1",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6373,
  "model_score": 0.6114,
  "style_score": 0.6631,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "14b8783e-11e6-4f90-bb4d-261ed18bf512",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3446,
  "model_score": 0.3212,
  "style_score": 0.368,
  "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "a2022801-bca3-4361-9064-e5c24323e164",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.3951,
  "model_score": 0.5727,
  "style_score": 0.2174,
  "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "43b6f9af-8697-453a-95bf-a06a3137e169",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6158,
  "model_score": 0.5862,
  "style_score": 0.6454,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "f2b3da1a-915a-4f06-8717-5959bf6836df",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6001,
  "model_score": 0.7042,
  "style_score": 0.496,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "fba93f56-d197-4196-a260-ff05a00cee1b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8394,
  "model_score": 0.9792,
  "style_score": 0.6996,
  "label": "Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f65e3105-442d-492d-bfe6-232579b9ea50",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.591,
  "model_score": 0.6175,
  "style_score": 0.5644,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "92fc3d04-dd91-4933-b8e6-748881aa22a7",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7196,
  "model_score": 0.7387,
  "style_score": 0.7005,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "d8006277-e816-4974-97c6-551f767d9f41",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7318,
  "model_score": 0.8051,
  "style_score": 0.6585,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "40d11ec7-d0a1-4418-93fa-b75905febe87",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7182,
  "model_score": 0.8329,
  "style_score": 0.6035,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "27fd89d2-d7c8-4165-864c-d8f50c923ca8",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7443,
  "model_score": 0.8005,
  "style_score": 0.6881,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "a50eb421-68a8-48b9-8862-1a5feda38317",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7037,
  "model_score": 0.8814,
  "style_score": 0.526,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "6a1336b8-4bce-4e92-aefe-4b8c29137436",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6588,
  "model_score": 0.8816,
  "style_score": 0.436,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "e6990b99-4520-490c-8eba-fd4b7ef49796",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4391,
  "model_score": 0.4625,
  "style_score": 0.4157,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "466b08c8-ee2f-43e1-85e4-2c023a4b7d95",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2889,
  "model_score": 0.2044,
  "style_score": 0.3734,
  "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "67204e75-e2c2-4f05-812e-5c2e0fedc3a1",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.576,
  "model_score": 0.5943,
  "style_score": 0.5578,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "484bd887-e94b-482d-b3e5-fdf29fa5df90",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5054,
  "model_score": 0.4998,
  "style_score": 0.511,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "1b3d16da-7329-4443-90f7-163aeac62b3a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4819,
  "model_score": 0.6401,
  "style_score": 0.3238,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "109b5242-6873-4d01-b8af-0fe90aed3de1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5659,
  "model_score": 0.5583,
  "style_score": 0.5735,
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
