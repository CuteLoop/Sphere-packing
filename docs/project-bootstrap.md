Below is a **lean, PI-level documentation bootstrap** tailored to *your specific project*:
**optimizing the minimum enclosing square for multiple rigid polygons (Christmas trees) using stochastic optimization (Metropolis–Hastings / annealing)**, with an eye toward Kaggle-style benchmarks and eventual methodological publication.

Each section corresponds to a file. You can copy them verbatim into your repo.

---

# 1️⃣ `README.md`

```markdown
# Minimum Enclosing Square Packing for Rigid Polygons

This project investigates stochastic optimization methods for packing multiple rigid, non-overlapping polygons (e.g. “Christmas tree” shapes) into the smallest possible square container, allowing both polygon and container rotation. The primary goal is to develop a reproducible, extensible baseline using Metropolis–Hastings–style local search, suitable for experimental comparison, competition settings (e.g. Kaggle), and eventual methodological publication.

## Current Status

- ✅ Geometry primitives for polygon construction, rotation, translation, and collision checks exist
- 🚧 Feasibility checks and energy formulations are under active development
- 🚧 Metropolis–Hastings optimizer is being built incrementally
- ❌ No finalized “best solver” yet; results are exploratory
- ❌ No performance tuning or large-scale benchmarking yet

This repository is intentionally split between **stable core geometry** and **exploratory optimization code**.

## Repository Structure

```

packing/
geometry.py        # Polygon construction, transforms, bounds, collision predicates
constraints.py     # Feasibility checks (overlap, containment)
energy.py          # Soft penalties for MH
mh.py              # Metropolis–Hastings kernel (in progress)
search.py          # Outer optimization over container size (planned)

tests/
test_geometry_*.py
test_constraints_*.py
test_mh_*.py

docs/
pi/
weekly_dashboard.md
ROADMAP.md
PROJECT_GOAL.md

logs/
research_log.md

````

## Getting Started

```bash
pip install shapely pandas pytest
pytest -q
````

Run tests first; optimization code is expected to change frequently.

## Documentation Pointers

* Project goals: `PROJECT_GOAL.md`
* Phase roadmap: `ROADMAP.md`
* Weekly PI dashboard: `docs/pi/weekly_dashboard.md`
* Research log (append-only): `logs/research_log.md`

````

---

# 2️⃣ `PROJECT_GOAL.md`

```markdown
# Project Goal

## Primary Goal

Develop a reproducible, testable stochastic optimization framework to approximately solve the **minimum enclosing square packing problem for multiple rigid polygons**, allowing rotations, under strict non-overlap constraints.

## Secondary Goals

1. Establish a clean separation between geometry, constraints, energy modeling, and optimization.
2. Produce a strong, transparent baseline suitable for comparison with more advanced methods (CMA-ES, physics-based relaxation, MILP relaxations).
3. Enable controlled experiments on the effect of rotation, container rotation, and penalty formulations.
4. Prepare the groundwork for a methodological paper or technical report.

## Non-Goals (Explicit)

- Guaranteeing global optimality
- Industrial-grade performance tuning (GPU, massive parallelism)
- Solving arbitrary polygon packing in general containers
- Building a full competition submission system at this stage

## Success Criteria (“Done Means”)

- For a fixed number `n`, the system can reliably find a feasible configuration near the minimal square side length.
- Core geometry and constraint logic is covered by deterministic tests.
- Optimization behavior is reproducible under fixed seeds.
- Results and failure modes are well-documented in logs.
- Codebase is stable enough to serve as a baseline in a paper or competition.
````

---

# 3️⃣ `ROADMAP.md`

```markdown
# Project Roadmap

## Phase 1 — Concept & Geometry (Current)

**Objectives**
- Define rigid polygon model (trees)
- Implement rotation/translation correctly
- Define collision semantics (“touching allowed”)
- Axis-aligned containment via rotated container frame

**Exit Conditions**
- Geometry and collision tests are green
- No ambiguity about overlap vs touch
- Bounding square computation validated

---

## Phase 2 — Prototype Optimization

**Objectives**
- Implement feasibility checks for fixed container size
- Define soft energy function (overlap + boundary penalties)
- Implement Metropolis–Hastings kernel with reproducibility
- Demonstrate feasibility for small `n`

**Exit Conditions**
- MH reduces overlaps reliably
- Feasible packings found for small cases
- Tests cover acceptance logic and reproducibility

---

## Phase 3 — Stabilization & Search

**Objectives**
- Outer loop to minimize square side length
- Warm-start strategies across container sizes
- Container rotation optimization (φ)

**Exit Conditions**
- Stable API for `find_min_square(n)`
- Clear separation between stable and experimental code
- Documented performance characteristics

---

## Phase 4 — Synthesis & Publication

**Objectives**
- Experimental evaluation across `n`
- Comparison with simpler heuristics
- Write-up of algorithmic choices and limitations

**Exit Conditions**
- Reproducible figures and tables
- Clean narrative suitable for paper or report
```

---

# 4️⃣ `docs/pi/weekly_dashboard.md`

```markdown
# Weekly PI Dashboard

## Primary Uncertainty This Week
- Does allowing container rotation materially reduce minimal square size for this polygon class?

## Research Mode Allocation
- Exploration: 40%
- Prototyping: 40%
- Stabilization: 15%
- Synthesis: 5%

## Stable Components
- Polygon construction and transforms
- Collision semantics (intersects vs touches)
- Bounding square computation

## Risky / Experimental Components
- Energy formulation for polygon overlaps
- MH mixing behavior
- Feasibility monotonicity in container size

## Weekly Action Checklist
- [ ] Finalize feasibility check API
- [ ] Write MH kernel with injectable proposer
- [ ] Add reproducibility test for MH
- [ ] Log first successful packing experiment

## End-of-Week Retrospective
- What worked:
- What failed:
- What surprised me:
- What to change next week:
```

---

# 5️⃣ `logs/research_log.md`

```markdown
# Research Log (Append-Only)

> Keep entries short. This is not a lab notebook; it is a memory aid.

---

## YYYY-MM-DD

### Context
(e.g. working on feasibility checks, MH kernel, geometry)

### What I Tried
- Brief description of experiment / coding session

### Outcome
- What happened (worked, failed, inconclusive)

### Decisions Made
- Any design or parameter decisions

### Open Questions
- What is still unclear?

### Next Step
- Single concrete action for next session

---
```

---

## Closing Note

This documentation system is intentionally **minimal but structural**:

* It separates *thinking*, *doing*, and *remembering*
* It scales from solo grad student → small lab
* It supports both **exploration** and **publication**

If you want next, I can:

* Generate a **weekly update prompt** that fills the dashboard from the log
* Create a **“promote to stable code” checklist**
* Design a **paper outline mapped to this roadmap**
* Turn this into a reusable **project-init template**

Just say where you want to go next.
