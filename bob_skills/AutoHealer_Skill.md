---
name: AutoHealer
description: >
  An IBM Bob 2.0 skill that acts as an autonomous Automated Testing & Validation Hub.
  It identifies failing tests, diagnoses root causes using subagents, and dispatches
  parallel Coder Subagents to fix multiple bugs simultaneously—demonstrating the
  full Agent mode, parallel tasks, and subagents feature set of IBM Bob 2.0.
version: 1.0.0
author: Bob AutoHeal Team
---

# AutoHealer Skill

## Purpose

This skill transforms IBM Bob into an **Automated Testing & Validation Hub**. When
triggered, it orchestrates a complete diagnosis-and-repair cycle without any manual
developer intervention.

**Hackathon Theme Addressed:** *Build with purpose using IBM Bob 2.0*
**Workflow Improved:** Automated Testing & Bug Resolution

---

## Workflow Overview

```
Developer pushes code
       |
       v
[Step 1] run_validation.py   ← Bob runs this first
       |
       | Tests FAIL?
       v
[Step 2] Research Subagent   ← Bob spawns this to read code + stack traces
       |
       | Root causes identified
       v
[Step 3] Parallel Coder Subagents (one per bug)   ← Bob spawns these in parallel
       |
       | All fixes applied
       v
[Step 4] run_validation.py again   ← Bob re-runs to verify
       |
       | All tests PASS?
       v
[Step 5] Generate Impact Report   ← Bob documents the improvement
```

---

## Invocation Instructions

When a user says **"Heal the application"** or **"Run the AutoHeal workflow"**, follow
these steps exactly in Agent mode.

### Step 1 — Baseline Validation

Run the validation script to capture the current state:

```bash
python scripts/run_validation.py
```

Parse the output:
- Count failing tests
- Extract stack traces and assertion errors
- Note which test names are failing

### Step 2 — Research Subagent (Document Understanding)

Spawn a **Research Subagent** with this prompt:

> "Read the file `demo_ecommerce_api/app.py` and the failing test file
> `demo_ecommerce_api/tests/test_app.py`. Cross-reference the pytest stack traces
> below with the application code. For each failing test, identify:
>   1. The exact line in app.py causing the failure
>   2. The root cause (missing check, wrong status code, missing validation, etc.)
>   3. The minimum code change required to fix it
>
> Stack traces: [PASTE STDOUT FROM STEP 1]"

Wait for the Research Subagent to return its analysis.

### Step 3 — Parallel Coder Subagents

Based on the Research Subagent's analysis, spawn **one Coder Subagent per bug**
using parallel tasks. Each subagent receives a targeted fix instruction:

**Coder Subagent 1 — Fix BUG-001 (KeyError / Missing item check):**
> "In `demo_ecommerce_api/app.py`, inside the `place_order` function, add a check
> before accessing `inventory[order.item]`. If the item is not in `inventory`,
> raise `HTTPException(status_code=404, detail=f\"Item '{order.item}' not found\")`.
> Do not change any other code."

**Coder Subagent 2 — Fix BUG-002 (Negative quantity):**
> "In `demo_ecommerce_api/app.py`, update the `Order` Pydantic model to add a
> `Field` constraint on `quantity`. Change `quantity: int` to
> `quantity: int = Field(..., gt=0, description='Must be >= 1')`.
> Also add `from pydantic import BaseModel, Field` to the imports.
> Do not change any other code."

**Coder Subagent 3 — Fix BUG-003/004 (Wrong HTTP status code):**
> "In `demo_ecommerce_api/app.py`, inside the `place_order` function, change the
> `raise HTTPException(status_code=500, ...)` for the out-of-stock case to
> `raise HTTPException(status_code=400, detail=f'Not enough stock. ...')`.
> Do not change any other code."

Wait for ALL three parallel subagents to complete before proceeding.

### Step 4 — Re-run Validation

After all Coder Subagents complete, run the validation script again:

```bash
python scripts/run_validation.py
```

**Expected result:** All 8 tests pass, coverage >= 80%.

If any tests still fail, repeat Steps 2–4 for the remaining failures.

### Step 5 — Generate Impact Report

Once all tests pass, generate a Markdown report summarising:
- Number of bugs found and fixed
- Test pass rate: before vs after
- Coverage: before vs after
- Estimated time saved (compare automated healing vs manual debugging)
- Which Bob 2.0 features were used (Agent mode, subagents, parallel tasks, document understanding)

Save the report to `docs/autoheal_impact_report.md`.

---

## Bob 2.0 Features Demonstrated

| Feature | How Used |
|---|---|
| **Agent Mode** | Orchestrates the entire validate → research → fix → validate loop autonomously |
| **Subagents** | Research Subagent analyses stack traces; Coder Subagents apply targeted fixes |
| **Parallel Tasks** | All Coder Subagents run simultaneously, cutting fix time by ~3x |
| **Document Understanding** | Reads `coverage.xml`, stack traces, and source files to reason about bugs |

---

## Example Prompt to Trigger This Skill

```
Heal the application using the AutoHeal workflow.
The failing tests are in demo_ecommerce_api/tests/test_app.py.
Run the validation script first, then fix all failing tests using parallel subagents.
```
