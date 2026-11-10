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



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

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
