# Bob AutoHeal — Architecture & Design

## System Architecture

The AutoHeal system consists of 4 layers:

```
+-------------------------------------------------------+
|                   IBM Bob IDE (Agent Mode)             |
|                                                       |
|  +------------------+    +-------------------------+  |
|  | AutoHealer Skill |    |   Bob 2.0 Agent Engine  |  |
|  | (Orchestrator)   |<-->|   - Subagent spawning   |  |
|  +------------------+    |   - Parallel task exec  |  |
|         |                |   - Document understanding| |
|         |                +-------------------------+  |
+---------|--------------------------------------------|
          |
          v (controls)
+-------------------------------------------------------+
|               Validation Hub                          |
|         scripts/run_validation.py                     |
|                                                       |
|   Runs pytest -> Generates coverage.xml -> Reports    |
+------------------+------------------------------------+
                   |
          +--------+--------+
          |                 |
          v                 v
+------------------+  +---------------------+
|  demo_ecommerce_api/ |  |  Healed Output      |
|  app.py (BUGGY)  |  |  app_healed.py       |
|  tests/          |  |  docs/impact_report  |
+------------------+  +---------------------+
```

## Data Flow

1. **Trigger:** Developer runs `python scripts/run_validation.py`
2. **Detection:** pytest reports failing tests + coverage gaps
3. **Analysis:** IBM Bob's Research Subagent parses stack traces and source code
4. **Repair:** 3 parallel Coder Subagents each fix one bug concurrently
5. **Verification:** Validation hub re-runs, confirms all tests pass
6. **Reporting:** Agent generates `docs/autoheal_impact_report.md`

## Bug Categories Addressed

| Bug ID | Category | Severity | Fix Strategy |
|---|---|---|---|
| BUG-001 | Missing guard clause | High | Add item-existence check → 404 |
| BUG-002 | Missing input validation | High | Pydantic `Field(gt=0)` |
| BUG-003 | Business logic error | Medium | Correct out-of-stock handling |
| BUG-004 | Wrong HTTP status code | Medium | Change 500 → 400 |

## Why This Matters

In real codebases, these patterns appear constantly:
- **KeyError/AttributeError** without guards — causes silent 500s in production
- **Missing input validation** — enables data corruption or abuse
- **Wrong HTTP status codes** — breaks client retry logic and monitoring

The AutoHeal Agent catches all of these at CI/CD time, before they reach production.
