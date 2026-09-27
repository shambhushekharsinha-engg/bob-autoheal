# Bob AutoHeal — Automated Testing & Validation Hub

> **IBM Bob 2.0 Hackathon Submission**
> Theme: *Build with purpose using IBM Bob 2.0*
> Category: Automated Testing & Validation Hub

---

## Problem Statement

Software teams waste **30–45 minutes per bug** in a slow, manual loop:

```
Write code → Push → CI fails → Read logs → Guess cause → Fix → Repeat
```

This cycle is:
- **Slow** — each iteration requires a human to read logs and reason about the code
- **Error-prone** — devs often fix symptoms, not root causes
- **Unscalable** — as codebases grow, the number of bugs outpaces the team

**Bob AutoHeal solves this** by using IBM Bob 2.0 to fully automate the
*detect → diagnose → fix → verify* loop using Agent mode, subagents, and parallel tasks.

---

## Solution: AutoHeal Workflow

```
┌─────────────────────────────────────────────────────────┐
│              IBM Bob 2.0 — Agent Mode                   │
│                                                         │
│  AutoHealer Skill (Orchestrator)                        │
│       │                                                 │
│       ├──[Step 1]── run_validation.py ───────────────►  │
│       │             (pytest + coverage)                 │
│       │                                                 │
│       ├──[Step 2]── Research Subagent ──────────────►   │
│       │             (reads code + stack traces)         │
│       │                                                 │
│       ├──[Step 3]── Parallel Coder Subagents ────────►  │
│       │             ├── Subagent 1: Fix BUG-001        │
│       │             ├── Subagent 2: Fix BUG-002        │
│       │             └── Subagent 3: Fix BUG-003/004    │
│       │                                                 │
│       └──[Step 4]── run_validation.py ───────────────►  │
│                     (all tests green)                   │
└─────────────────────────────────────────────────────────┘
```

### IBM Bob 2.0 Features Used

| Feature | How It's Used |
|---|---|
| **Agent Mode** | Orchestrates the full validate → research → fix → validate loop autonomously |
| **Subagents** | Research Subagent analyses stack traces; 3 Coder Subagents apply targeted fixes |
| **Parallel Tasks** | All Coder Subagents run **simultaneously**, cutting fix time by ~3× |
| **Document Understanding** | Reads `coverage.xml`, pytest stack traces, and source files |

---

## Project Structure

```
bob-autoheal/
├── README.md                          # This file
├── .gitignore
│
├── demo_ecommerce_api/                # The sample application
│   ├── app.py                         # BUGGY version (starting state)
│   ├── app_healed.py                  # HEALED version (what Bob produces)
│   ├── requirements.txt
│   └── tests/
│       └── test_app.py                # Full test suite (exposes all 4 bugs)
│
├── scripts/
│   └── run_validation.py              # Validation Hub orchestrator
│
├── bob_skills/
│   └── AutoHealer_Skill.md            # IBM Bob skill instructions
│
├── docs/
│   ├── architecture.md                # System design docs
│   └── autoheal_impact_report.md      # Before/after impact metrics
│
└── bob_sessions/                      # IBM Bob task session screenshots (required)
    └── teamalpha_task01_autoheal_flow_summary.png
```

---

## The Demo Application

The `demo_ecommerce_api` is a realistic FastAPI app with **4 intentional bugs** that
represent common real-world mistakes:

| Bug ID | Location | Issue | Expected | Actual |
|---|---|---|---|---|
| **BUG-001** | `app.py:35` | Missing item existence check | HTTP 404 | HTTP 500 (KeyError) |
| **BUG-002** | `app.py:Order` | No negative quantity validation | HTTP 422 | HTTP 200 (accepted!) |
| **BUG-003** | `app.py:40` | Out-of-stock logic error | HTTP 400 | HTTP 500 |
| **BUG-004** | `app.py:40` | Wrong HTTP status code | HTTP 400 | HTTP 500 |

The test suite in `tests/test_app.py` exposes all 4 bugs. Running it against the
**buggy** `app.py` produces **3 failing tests**. The IBM Bob AutoHeal Agent then
fixes them, and re-running the suite produces **all green**.

---

## Getting Started

### Prerequisites

- Python 3.10+
- IBM Bob IDE (installed and signed in)

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/bob-autoheal.git
cd bob-autoheal
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # Mac/Linux
pip install -r demo_ecommerce_api/requirements.txt
```

### 2. Run Baseline Validation (Observe Failing Tests)

```bash
python scripts/run_validation.py
```

You will see **3 tests fail**, proving the bugs exist:

```
FAILED tests/test_app.py::TestOrderBugs::test_order_unknown_item_returns_404
FAILED tests/test_app.py::TestOrderBugs::test_order_negative_quantity_rejected
FAILED tests/test_app.py::TestOrderBugs::test_order_out_of_stock_returns_400

3 failed, 5 passed
```

### 3. Trigger the IBM Bob AutoHeal Agent

1. Open **IBM Bob IDE** and open the `bob-autoheal` workspace
2. Go to **Tasks** → **New Task**
3. Load the skill: reference `bob_skills/AutoHealer_Skill.md`
4. Type: `Heal the application using the AutoHeal workflow`
5. Watch Bob spawn subagents and fix bugs in parallel!

### 4. Verify the Fixes

After Bob heals the app, run validation again:

```bash
python scripts/run_validation.py
```

Expected output:

```
All tests passed! Application is healthy.
8 passed, 0 failed, coverage: 95%
```

---

## Impact Metrics

| Metric | Manual Debugging | Bob AutoHeal |
|---|---|---|
| Time to identify all 4 bugs | ~20 min | ~30 sec |
| Time to fix all 4 bugs | ~25 min | ~90 sec (parallel) |
| **Total cycle time** | **~45 min** | **~2 min** |
| Human effort required | High | Zero (after trigger) |
| Risk of incomplete fix | Medium | Low (test-driven verification) |

**Time savings: ~43 minutes per bug-fix cycle.**

---

## Data Compliance

All data used in this project is:
- Synthetically generated (no real customer data)
- No personal information (PI)
- No confidential company data
- No social media data
- No client data

---

## Submission Checklist

- [x] Working prototype built with IBM Bob IDE
- [x] Clearly defined problem: manual debugging waste
- [x] IBM Bob IDE used as a core component (Agent mode, subagents, parallel tasks)
- [x] Leverages: Agent mode, parallel tasks, subagents, document understanding
- [x] Demonstrates measurable impact (before/after metrics)
- [x] `bob_sessions/` folder with IBM Bob task session summary screenshots
- [x] All data is compliant (synthetic only)

---

## Team

**Team Name:** DevPulse AI  
**Member:** Shambhu Shekhar Sinha

---

*Built for the IBM Bob 2.0 Hackathon — "Build with purpose using IBM Bob 2.0"*
