# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. A writing site sends a JSON request to POST /submit with two fields: text (the poem) and creator_id (who submitted it).
Adds: the input: the writing to judge, and who it belongs to, so the decision can be logged against that person and they can appeal it later.

2. The route checks that text and creator_id are present, and that the text isn't empty, too long, or extremely short.
Adds: a gate. If the input is bad, the route stops and sends back an error message, so bad input never reaches the signals and never gets saved in the log as a decision about someone.

3. Signal one (detector.py): GPT-2 reads the text word by word and measures how surprising it is (perplexity).
Adds: the first piece of evidence: the perplexity converted to a score from 0 to 1 (model_score). Low perplexity means a higher score, which is more AI-like.

4. Signal two (stylometry.py) measures the text's style without reading its meaning: how much sentence lengths vary, how varied the vocabulary is, and how much punctuation it uses.
Adds: a second, independent piece of evidence: a score from 0 to 1 (style_score). Even, uniform writing scores higher, which is more AI-like.

5. scoring.py (combine_signals) combines the two signals with a weighted average. Right now they count equally (0.5 each, set in config.py).
Adds: one combined score from 0 to 1 (combined_score), so there's a single number to compare against the thresholds.


6. scoring.py (score_to_label) turns the combined score into one of three labels (human, unsure, or likely AI) using two thresholds (0.40 and 0.70 in config.py).
Adds: the plain-English message a writer actually reads. It says how sure the system is in words, says what happens next, and doesn't accuse them.

7. The decision is written to logs/audit.jsonl through audit.py, and the response goes back with the content_id, guess, confidence score, and label text.
Adds: a permanent record of the decision (both signal scores, the combined score, the label, and status "decided"), so a reviewer can later see what was decided and why, and the content_id, which the writer needs to appeal the decision.

### When it gets it wrong

Amina, a second-language writer, submits a short, plain poem she wrote herself. Because she uses simple words, GPT-2 finds it predictable, so I expect signal one to score it high (around 0.75). Because her lines are even with little punctuation, I expect signal two to score it high too (around 0.75). Both signals share the same blind spot, so the combined score would be about 0.75, above the 0.70 AI threshold, and she gets the "likely AI" label.

She reads that on a poem she wrote, and feels accused. If the label doesn't say why or what to do next, she may not know she can push back.

What she can do: send POST /appeal with the content_id from her /submit response and her reasoning. The appeal is logged next to the original decision, and the status moves from "decided" to "under_review".

### The two endpoints

```
POST /submit
  In:    text (the writing), creator_id (who submitted it)
  Out:   content_id, guess, confidence, label
  Error: missing/empty/too short/too long text, or missing creator_id
         → 400 with an error message (not scored, not logged as a decision)

POST /appeal
  In:    content_id, reasoning (the writer's explanation)
  Out:   content_id, status ("under_review"), a short confirmation message
  Note:  creator_id is looked up from the original log entry
         (audit.entries_for), so the writer doesn't resend it.
  Error: unknown content_id → 404 with an error message
         missing content_id or reasoning → 400
```


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** GPT-2 reads the text word by word and measures how surprising it is (perplexity). `detector.py` converts that to a score from 0 to 1 (model_score). Low perplexity means a higher score, which is more AI-like.

**Why that might differ between human and AI writing:** AI tends to pick the most likely next word, so its text surprises GPT-2 less.

**What it can't see:** It can't tell plain, predictable human writing from AI writing. Famous or quoted text, and simple writing from second-language or younger writers, look predictable, so they score AI-like even when a human wrote them. And AI text that uses rare words can score human-like.

### Signal two — the style signal

**What it measures:** the text's style without reading its meaning: how much sentence lengths vary, how varied the vocabulary is, and how much punctuation it uses. It becomes a score from 0 to 1 (style_score). Even, uniform writing scores higher, which is more AI-like.

**Why that might differ between human and AI writing:** Humans tend to write unevenly: short and long sentences, more varied punctuation. AI is more even.

**What it can't see:** It never reads meaning, only shape. Human writing that is naturally even (recipes, rhythmic poems, careful formal writing) scores AI-like, and AI text can be edited to look human just by changing sentence lengths and adding punctuation.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average of the two signals. If the two signals differ by more than 0.3, the score is capped just below the AI threshold, so the result is "unsure" instead of "likely AI". Both signals have to agree before the system accuses someone. If they disagree on the human side, nothing changes, because nobody is harmed.

**The numbers:** model weight 0.5, style weight 0.5, disagreement limit 0.3 (all in config.py). I kept the weights equal because neither signal earned more trust in my tests: signal one put both of my own texts above 0.65, and two of the three style measures pointed the wrong way. Inside the style signal (`stylometry.py::style_signal`): sentence-length spread 0.6, type-token ratio 0.2, punctuation 0.2. Spread gets the most weight because it was the only measure that separated my AI and human test texts in the expected direction.

My four test inputs, sent through POST /submit:

| Input | Model | Style | Combined |
|---|---|---|---|
| Clearly AI (exercise paragraph) | 0.9188 | 0.6338 | 0.7763 |
| Formal human (my prayer paragraph) | 0.8034 | 0.4791 | 0.6412 |
| Lightly-edited AI (exercise, my edits) | 0.4972 | 0.5358 | 0.5165 |
| Clearly human (my casual message) | 0.342 | 0.3626 | 0.3523 |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
My prayer paragraph: model 0.8034, style 0.4791, a difference of 0.32, which is over my 0.3 limit. Signal one says AI-like and signal two says human-like. The rule caps the score just below the AI threshold (at 0.69), so this text can never get "likely AI" while the signals disagree this much. Its plain average is 0.6412, already below the cap, so it lands in "unsure" either way. When I was still using a 0.65 AI threshold, the cap was 0.64 and it moved the score slightly (0.641 to 0.64), but not the label. The rule matters most for a case like model 0.98 and style 0.45: the plain average is 0.715, which would be "likely AI", but the signals differ by 0.53, so the cap brings it down to 0.69 and it lands in "unsure" instead of an accusation.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 to 0.40 | Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed. |
| unsure | 0.40 to 0.70 | Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it. |
| high-confidence AI | 0.70 to 1.00 | Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it. |

A score of exactly 0.40 counts as human, and exactly 0.70 counts as likely AI (`scoring.py::score_to_label`). The thresholds are `HUMAN_THRESHOLD` and `AI_THRESHOLD` in config.py.

**Why I moved the thresholds from 0.35 / 0.65 to 0.40 / 0.70:** At 0.65, a shortened version of my own Morocco travel message scored 0.6683 and would have been labeled "likely AI". At 0.35, my casual message to a friend scored 0.3523 and could not reach "human", even with typos and "!!!!". At 0.40 / 0.70, every one of my test texts lands where it should, and my clearly-AI example (0.7763) still gets caught. The trade-off is that some AI text scoring between 0.65 and 0.70 now gets "unsure" instead of "likely AI". I accept more misses so that fewer real writers get accused.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says the check couldn't tell, instead of giving a number, so the reader doesn't have to guess what 0.55 means. It says the post stays up, because the first worry is whether anything happened to their work. It says "this isn't a judgment about you", because my own writing landed in "unsure" during testing, and someone like Amina may have written every word. It ends with a way to reach a person, so the writer is never stuck with a machine's guess.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

My own prayer paragraph, written by me:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Prayer is one of the 5 pillars of Islam. It is an obligatory ritual that every muslim is supposed to perform 5 times a day. Each of these 5 times has a specific time for prayer every single day, including dawn, noon, mid afternoon, sunset, and after dark.", "creator_id": "u1"}'
```

```json
{
  "confidence": 0.6412,
  "content_id": "5be9f0a1-8633-436d-9c75-5a252734a81d",
  "guess": "unsure",
  "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
  "model_score": 0.8034,
  "style_score": 0.4791
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "5be9f0a1-8633-436d-9c75-5a252734a81d", "reasoning": "I wrote this myself. It is plain because I was explaining a basic fact about my religion."}'
```

```json
{
  "content_id": "5be9f0a1-8633-436d-9c75-5a252734a81d",
  "message": "Thanks. Your appeal was received and a person will review it.",
  "status": "under_review"
}
```

An appeal with a content_id that doesn't exist:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "not-a-real-id", "reasoning": "test"}'
```

```json
{
  "error": "not_found",
  "message": "No submission with that content_id."
}
```

**What the log shows afterwards**

The original decision stays in the log unchanged, and the appeal is added right after it with the same content_id.

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.3523,
      "content_id": "53f30962-8041-45a9-bb98-d0eeaefc208c",
      "creator_id": "u1",
      "guess": "human",
      "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.",
      "model_score": 0.342,
      "status": "decided",
      "style_score": 0.3626,
      "timestamp": "2026-11-04T06:35:16+00:00"
    },
    {
      "combined_score": 0.6412,
      "content_id": "5be9f0a1-8633-436d-9c75-5a252734a81d",
      "creator_id": "u1",
      "guess": "unsure",
      "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
      "model_score": 0.8034,
      "status": "decided",
      "style_score": 0.4791,
      "timestamp": "2026-11-04T06:39:30+00:00"
    },
    {
      "content_id": "5be9f0a1-8633-436d-9c75-5a252734a81d",
      "creator_id": "u1",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is plain because I was explaining a basic fact about my religion.",
      "status": "under_review",
      "timestamp": "2026-11-04T06:40:22+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1: weighting the style signal**

- *What I asked for:* I had built the three style measures (sentence-length spread, type-token ratio, punctuation density) and was stuck on how to combine them into one score.
- *What came back:* A suggestion to weight them 0.6 spread, 0.2 type-token ratio, 0.2 punctuation, because on my test texts spread was the only measure that separated AI from human in the expected direction. The other two pointed the wrong way: the AI paragraph had more varied vocabulary and more commas than my human text.
- *What I changed:* I kept the weights, because when I ran them the clearly-AI paragraph scored 0.63 on style and my human text scored 0.18. Using the code was not smooth. I first pasted the spread code into the wrong function (`punctuation_density`), and the test output showed the spread number on the punctuation line, so I moved it. Then in `/submit` I called `sentence_length_spread` instead of `style_signal`. That measure runs backwards (higher means more human) and isn't on a 0 to 1 scale, so it would have pushed human writing toward AI. I switched it to `style_signal`.

**Moment 2: moving the thresholds**

- *What I asked for:* Whether to keep the starter thresholds of 0.35 / 0.65 or change them before writing my labels.
- *What came back:* A suggestion to move them to 0.40 / 0.70, with a table showing where each of my test texts would land under both settings.
- *What I changed:* I moved them because of two results from my own writing. A shortened version of my Morocco travel message scored 0.6683, so at 0.65 it would have been labeled "likely AI". My casual message to a friend scored 0.3523, so at 0.35 it couldn't reach "human", even with typos. To check the change, I ran `label_ranges()` to make sure there were no gaps, and I curled three texts that came back ai, unsure and human. I also wrote down the trade-off: some AI text between 0.65 and 0.70 now gets "unsure" instead of "likely AI".

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 120 per day (`RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_DAY` in config.py)

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

I took these numbers from the instructor's demo in lecture, then checked whether they hold up for the two kinds of caller, and kept them because they do.

- **6 per minute:** a real writer submits a piece, maybe fixes a typo and resubmits, so 2 or 3 tries in a minute. 6 leaves room for that. Each submission also runs GPT-2 for about a second, so 6 a minute keeps one caller from tying up the service.
- **120 per day:** without a daily limit, a script staying just under the minute limit (5 a minute) could send about 7,200 requests a day. 120 is enough for a writer revising many times, but too few to map my thresholds precisely by sending variations.
- **The trade-off:** a writer who revises and resubmits quickly might hit the 6 a minute limit and have to wait. And a script that uses a different creator_id for every request isn't stopped at all, because I have no server-wide limit, only a per-caller one.

**What a caller counts as:** per creator_id. If a request has no usable creator_id, it counts against the caller's address instead (`rate_limit_key` in app.py). This is why only the flood rows can trip it: one script sending many creator_ids looks like many different writers.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

From `results/flood_2026-11-04_1528.md`, 15 submissions as one creator_id:

```
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
```

The first 6 are accepted and the other 9 get 429 with the message "Too many submissions. Try again shortly." Each 429 is logged as a rejection by the starter's 429 handler.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Run with `python run_attacks.py --set attack_set` against the system I submitted in unit 7 (thresholds 0.40 / 0.70). Full output: `results/attack_run_2026-11-09_1941.md`.

An honest note: my first run, `results/attack_run_2026-11-09_1932.md`, was made by mistake with different thresholds (0.35 / 0.78) that I had changed while following the lecture demo. I put config.py back to my committed 0.40 / 0.70 and re-ran. The 1941 run is my real "before".

**How I marked them**

- **evasion and prompt_injection:** BROKE only if AI or attack text got "human". "Unsure" means my system said it couldn't tell, which is what it is designed to do when in doubt, so I marked it HELD, but I list those as "unsure, not caught" so it's clear they weren't caught either.
- **false_positive:** BROKE if a human-written text got "likely AI", because that accuses a real writer.
- **malformed and flood:** HELD if the service answered with a 4xx (400 or 429), BROKE if it crashed (500).

**Counts**

| Family | Total | BROKE | HELD | Which broke |
|---|---|---|---|---|
| evasion | 10 | 2 | 8 (6 of them "unsure, not caught") | EV05, EV06 |
| false_positive | 8 | 4 | 4 | FP02, FP03, FP04, FP05 |
| prompt_injection | 6 | 1 | 5 (all 5 "unsure, not caught") | PI02 |
| malformed | 20 | 1 | 19 | RQ07 |
| flood_same_creator | 12 | 0 | 12 | |
| **Total** | **56** | **8** | **48** | |

**Every attack**

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.423 | HELD (unsure, not caught) |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.455 | HELD (unsure, not caught) |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.588 | HELD (unsure, not caught) |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.637 | HELD (unsure, not caught) |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.345 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | human | 0.395 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.616 | HELD (unsure, not caught) |
| EV08 | evasion | signal one: text below the token window | 400 |  |  | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.600 | HELD (unsure, not caught) |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.839 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.591 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.720 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.732 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.718 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.744 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.690 | HELD (disagreement cap) |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.659 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 |  |  | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.439 | HELD (unsure, not caught) |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.289 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.576 | HELD (unsure, not caught) |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.505 | HELD (unsure, not caught) |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.482 | HELD (unsure, not caught) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.566 | HELD (unsure, not caught) |
| MF01 | malformed | text is only whitespace | 400 |  |  | HELD |
| MF02 | malformed | text is a single character | 400 |  |  | HELD |
| MF03 | malformed | text is control characters | 400 |  |  | HELD |
| MF04 | malformed | text is only punctuation | 400 |  |  | HELD |
| MF05 | malformed | text is a very long single word | 400 |  |  | HELD |
| MF06 | malformed | text is emoji only | 400 |  |  | HELD |
| MF07 | malformed | text is right-to-left script | 400 |  |  | HELD |
| MF08 | malformed | text is 60,000 characters | 400 |  |  | HELD |
| RQ01 | malformed | no text field at all | 400 |  |  | HELD |
| RQ02 | malformed | no creator_id | 400 |  |  | HELD |
| RQ03 | malformed | text is a number | 400 |  |  | HELD |
| RQ04 | malformed | text is a list | 400 |  |  | HELD |
| RQ05 | malformed | text is null | 400 |  |  | HELD |
| RQ06 | malformed | creator_id is an object | 400 |  |  | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 500 |  |  | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 |  |  | HELD |
| RQ09 | malformed | body is empty | 400 |  |  | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 |  |  | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 |  |  | HELD (429 before my route, untested) |
| RQ12 | malformed | deeply nested JSON | 400 |  |  | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 |  |  | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 |  |  | HELD |

What stood out:

- **4 of 8 false positives labeled a real writer "likely AI"**, all between 0.718 and 0.744, just above my 0.70 line. They are piled, not scattered.
- **FP06 was saved by my disagreement cap.** Model 0.8814 and style 0.526 differ by 0.355, more than my 0.3 limit. The plain average was 0.7037 (likely AI), and the cap brought it to 0.69 (unsure).
- **RQ07 crashed the route (500).** The body was a JSON array. `request.get_json(silent=True) or {}` keeps a non-empty list, and `payload.get` fails on a list.
- **Flood rows:** the first 6 got 400 because each text was under 20 words, then the limiter returned 429 for the other 6. Both layers worked.
- **RQ11** came back 429 because it had no usable creator_id, so it counted against my own address after earlier malformed rows. It never reached my route, so it went untested.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-10T03:41:54+00:00", "content_id": "b06661ba-d7c1-462d-91e2-0895d55a806c", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6585, "combined_score": 0.7318, "label": "Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:54+00:00", "content_id": "e19090a5-f114-46eb-83bf-955ea8685131", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6881, "combined_score": 0.7443, "label": "Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:54+00:00", "content_id": "c86a1072-0316-445a-a206-0c599e5b8535", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.7005, "combined_score": 0.7196, "label": "Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:54+00:00", "content_id": "cdb5ff87-8df3-4cdc-89d4-31ceff9b168b", "creator_id": "attacker_FP06", "guess": "unsure", "model_score": 0.8814, "style_score": 0.526, "combined_score": 0.69, "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:53+00:00", "content_id": "3e5921fb-da5c-46d2-9f8a-76a7e06c99e9", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.368, "combined_score": 0.3446, "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:53+00:00", "content_id": "c4f7838d-c6e2-44f1-9a3d-a62f41a56434", "creator_id": "attacker_EV06", "guess": "human", "model_score": 0.5727, "style_score": 0.2174, "combined_score": 0.3951, "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:55+00:00", "content_id": "dae8c7c9-2e42-4adf-a13e-dc1133f0874d", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3734, "combined_score": 0.2889, "label": "Our automated check thinks this was probably written by a person. Automated checks aren't perfect, but we didn't find signs of AI help. Nothing changes: your post stays up as normal. No action is needed.", "status": "decided"}
{"timestamp": "2026-11-10T03:41:54+00:00", "creator_id": "attacker_FP08", "event": "rejected", "status": "rejected", "reason": "This is too short to check fairly. Send at least 20 words."}
{"timestamp": "2026-11-10T03:41:55+00:00", "creator_id": {"id": "x"}, "event": "rejected", "status": "rejected", "reason": "Send a creator_id."}
{"timestamp": "2026-11-10T03:41:55+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "6 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03, a non-native English speaker writing carefully:** labeled "likely AI" with a combined score of 0.7318 (model 0.8051, style 0.6585). This is the Amina case from my unit 7 trace, happening for real. The writer was careful, so the sentences are even, and wrote in a second language, so the words are common and predictable. Both signals read that as machine-like and agreed, so my disagreement cap didn't help. The label tells this writer an automated check found AI patterns in work they wrote themselves.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

How I ran it: `python run_eval.py --label before` sent my scenarios from `scenarios.py` to `POST /submit` 3 times. `run_eval.py` can't send appeals, so I extended the test with `eval_extra.py`, which reads the run report for the criterion 1, 3 and 4 numbers, sends the appeals for criterion 2 (30 real and 9 fake across 3 trials), feeds the exact scores from criterion 4 into `scoring.py::score_to_label`, and checks the log and `/ping` for criterion 5. Results: `results/run_2026-11-10_2034_before.md` and `results/extra_2026-11-10_2035_before.md`.

Inputs: criterion 1 is 10 pieces I wrote myself (5 casual, 5 plain). Criterion 3 uses 5 pieces written by a chatbot (Claude) and pasted in unedited, compared with my 5 casual pieces. Criterion 4 counts labels across all 15 of those pieces.

The scores were identical in all 3 trials. GPT-2 gives the same text the same score every time, so the trials repeat rather than vary.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My writing flagged | At most 1 of 10 gets "likely AI" | 1 of 10 (piece 7) | 1 of 10 (piece 7) | 1 of 10 (piece 7) | **MET** |
| 2. Appeals | 10 of 10 real pass; 3 of 3 fake return 404 and log nothing | 10 of 10; 3 of 3, 0 logged | 10 of 10; 3 of 3, 0 logged | 10 of 10; 3 of 3, 0 logged | **MET** |
| 3. AI vs human gap | AI average at least 0.3 above human average | AI 0.6791, human 0.5948, gap 0.0843 | gap 0.0843 | gap 0.0843 | **MISSED** |
| 4. Label coverage | At least 2 in each label; every exact score gets one label | human 1, unsure 12, likely AI 2; exact scores: 10 of 10 got one label | human 1, unsure 12, likely AI 2 | human 1, unsure 12, likely AI 2 | **MISSED** |
| 5. Bad input | 6 of 6 return 400, 0 logged as decisions, /ping answers | 6 of 6 got 400; 0 decisions; /ping 200 | 6 of 6 got 400 | 6 of 6 got 400 | **MET** |

Note on criterion 4: the exact scores in the criterion (0.34, 0.35, 0.36, 0.64, 0.65, 0.66) sit on my old thresholds of 0.35 and 0.65. I moved the thresholds to 0.40 and 0.70 before this run, so I also tested 0.40 (human) and 0.70 (likely AI). All 10 scores returned exactly one label with no error. The exact-score test doesn't use the model, so it doesn't vary across trials.

**Real output from trial 1**, produced by `run_eval.py::main` sending to `app.py::submit` (scored by `scoring.py::combine_signals`, labeled by `scoring.py::score_to_label`). Three entries: my flagged piece 7 (criterion 1), the first AI piece (criterion 3), and the first bad request (criterion 5):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7951,
    "model_score": 0.8732,
    "style_score": 0.7169,
    "label": "Our automated check found patterns that often appear in AI-assisted writing. Automated checks can be wrong, especially on clear or simple writing. This is an estimate, not proof. Your post stays up, with a note that it may be AI-assisted. If you wrote this yourself, tell us about your writing and a person will review it.",
    "sent": "I called an old friend of mine today. I haven't talked to him for over"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.69,
    "model_score": 0.909,
    "style_score": 0.5624,
    "label": "Our automated check couldn't tell whether this was written by a person or with AI help. Nothing changes: your post stays up as normal. This isn't a judgment about you or your work. If you think we got this wrong, you can tell us why and a person will review it.",
    "sent": "Regular physical activity offers a wide range of benefits for both the"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing_text\"}"
  }
]
```

**Real output for criterion 2**, produced by `eval_extra.py::appeals` sending to `app.py::appeal`. The response, then the log entries for that content_id afterward (from `GET /log`):

```json
{
  "content_id": "c0b12f6a-e44b-4ff1-b905-a81aeb88b1f7",
  "message": "Thanks. Your appeal was received and a person will review it.",
  "status": "under_review"
}
```

```json
[
  {
    "combined_score": 0.6191,
    "content_id": "c0b12f6a-e44b-4ff1-b905-a81aeb88b1f7",
    "creator_id": "eval_c3 clearly A_5",
    "guess": "unsure",
    "model_score": 0.7087,
    "status": "decided",
    "style_score": 0.5295,
    "timestamp": "2026-11-11T04:34:24+00:00"
  },
  {
    "content_id": "c0b12f6a-e44b-4ff1-b905-a81aeb88b1f7",
    "creator_id": "eval_c3 clearly A_5",
    "event": "appeal",
    "reasoning": "Trial 1, appeal 1: I wrote this myself.",
    "status": "under_review",
    "timestamp": "2026-11-11T04:35:10+00:00"
  }
]
```

(The `label` text in the decision entry is left out here because it's the same unsure label shown above.)

**Scores for every piece, trial 1** (identical in trials 2 and 3):

| Piece | Type | Model | Style | Combined | Label |
|---|---|---|---|---|---|
| 1. Prayer | casual | 0.8034 | 0.4791 | 0.6412 | unsure |
| 2. Morocco | casual | 0.7337 | 0.6028 | 0.6683 | unsure |
| 3. Allah bless you | casual | 0.342 | 0.3626 | 0.3523 | human |
| 4. Morning routine | casual | 0.5644 | 0.7133 | 0.6389 | unsure |
| 5. Car battery | casual | 0.6675 | 0.679 | 0.6733 | unsure |
| 6. Missed prayers | plain | 0.206 | 0.7417 | 0.4738 | unsure |
| 7. Old friend | plain | 0.8732 | 0.7169 | 0.7951 | likely AI |
| 8. Thanksgiving | plain | 0.5427 | 0.6449 | 0.5938 | unsure |
| 9. Gym | plain | 0.5084 | 0.3779 | 0.4431 | unsure |
| 10. MacBook | plain | 0.3839 | 0.6488 | 0.5164 | unsure |
| AI 1. Exercise | chatbot | 0.909 | 0.5624 | 0.69 (capped) | unsure |
| AI 2. Time management | chatbot | 0.7446 | 0.6832 | 0.7139 | likely AI |
| AI 3. Climate | chatbot | 0.9316 | 0.5626 | 0.69 (capped) | unsure |
| AI 4. Language | chatbot | 0.8392 | 0.5263 | 0.6827 | unsure |
| AI 5. Artificial intelligence | chatbot | 0.7087 | 0.5295 | 0.6191 | unsure |

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

Two misses from my criteria and eight broken attacks. They group into seven diagnoses, and most of them come back to the same two causes: signal one reads clear writing as AI, and the combining rule only guards one side.

**Criterion 3 (MISSED, gap 0.0843 vs 0.3).** Three stages each shrank the gap. **The combining rule:** on AI pieces 1 and 3, signal one (0.909, 0.9316) and signal two (0.5624, 0.5626) disagree by more than 0.3, so the cap set both to 0.69. That pulled the AI average down to 0.6791. **Signal one:** GPT-2 finds my clear, correct writing predictable, so 4 of my 5 casual pieces scored 0.56 to 0.80 on it, which pushed the human average up to 0.5948. **Signal two:** style scored the AI pieces 0.53 to 0.68 and my casual pieces 0.36 to 0.71. The ranges overlap, so it added almost nothing to the gap. Together, the cap lowers the AI side and signal one raises the human side.

**Criterion 4 (MISSED, 1 piece reached "human" vs 2).** **The combining rule:** the score is an average, so a piece only reaches "human" (0.40 or lower) when both signals are low at the same time. Only piece 3 managed that (model 0.342, style 0.3626). Piece 6 had model 0.206, but its style of 0.7417 pulled it up to 0.4738. **Signal two:** 60% of its weight is sentence-length spread, and my plain pieces use short sentences of similar length, so they scored 0.64 to 0.74 as if they were AI. **The label mapping:** 12 of 15 pieces landed in the unsure band (0.40 to 0.70), because my writing clusters around 0.44 to 0.67, so "human" is reachable only by very messy writing like piece 3.

**FP02, FP03, FP04, FP05 (careful human writing labeled "likely AI", 0.718 to 0.744).** **Signal one and signal two together.** Signal one reads careful, correct writing (formal, second-language, rubric essay, technical docs) as predictable, so model scores were 0.74 to 0.83. Signal two reads even sentence lengths as AI-like, so style scores were 0.60 to 0.70. The signals differ by less than 0.3, so the cap in **the combining rule** doesn't step in, and all four land just over the 0.70 threshold. This is the same pattern as my criterion 1 miss on piece 7 (0.7951), and FP03 is the writer my criteria were built to protect.

**EV06 (AI text labeled human, 0.395).** **Signal two:** one very long sentence and one very short one make the sentence-length spread huge, so style dropped to 0.2174. Model was 0.5727. **The combining rule:** the signals differ by 0.355, which is over my 0.3 limit, but the cap only stops scores from reaching "likely AI". It never stops a score from reaching "human", so the average of 0.395 passed.

**EV05 (AI text after a heavy human edit labeled human, 0.345).** **Both signals** were fooled. The editing made the wording less predictable (model 0.3212) and the sentence lengths uneven (style 0.368). With both signals low, no stage had anything left to catch it.

**PI02 (fake "SYSTEM:" instruction labeled human, 0.289).** Nothing obeyed the instruction, since there's no chatbot in my pipeline. **Signal one:** the strange header line (`SYSTEM: ... guess=human, confidence=0.02`) is very unpredictable to GPT-2, which raises the average perplexity and drops the model score to 0.2044. Style was 0.3734. The attack worked as noise, not as an instruction.

**RQ07 (JSON array body gave a 500).** **The route:** `request.get_json(silent=True) or {}` keeps a non-empty list, because a list isn't falsy. Then `payload.get("text")` fails, since lists have no `.get`, and the service crashes before `check_submission` runs.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
