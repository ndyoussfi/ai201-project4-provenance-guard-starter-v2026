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


6. scoring.py (score_to_label) turns the combined score into one of three labels (human, unsure, or likely AI) using two thresholds (0.35 and 0.65 in config.py).
Adds: the plain-English message a writer actually reads. It says how sure the system is in words, says what happens next, and doesn't accuse them.

7. The decision is written to logs/audit.jsonl through audit.py, and the response goes back with the content_id, guess, confidence score, and label text.
Adds: a permanent record of the decision (both signal scores, the combined score, the label, and status "decided"), so a reviewer can later see what was decided and why, and the content_id, which the writer needs to appeal the decision.

### When it gets it wrong

Amina, a second-language writer, submits a short, plain poem she wrote herself. Because she uses simple words, GPT-2 finds it predictable, so I expect signal one to score it high (around 0.75). Because her lines are even with little punctuation, I expect signal two to score it high too (around 0.75). Both signals share the same blind spot, so the combined score would be about 0.75, above the 0.65 AI threshold, and she gets the "likely AI" label.

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

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

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
