Understood. Conceptually, you are solving a **minimum enclosing square (axis-aligned)** problem under **non-overlap constraints** for **rigid polygons** (your ChristmasTree instances), where the decision variables are each polygon’s translation ((x_i,y_i)) and rotation (\theta_i).

Below is a clear blueprint for how to build this (code + tests) without getting lost.

---

## 1) Formalize the optimization problem

Given:

* A fixed polygon template (P) (your tree shape in local coordinates)
* (n) copies (P_i), each with pose ((x_i,y_i,\theta_i))
* An axis-aligned square container of side length (L)

Find:
[
\min_{(x_i,y_i,\theta_i),,L} ; L
]
subject to:

1. **Containment**: each transformed polygon lies inside the square
   [
   P_i(x_i,y_i,\theta_i) \subseteq [-L/2, L/2]^2
   ]
2. **No overlap**: for all (i\neq j),
   [
   \text{interior}(P_i)\cap \text{interior}(P_j)=\emptyset
   ]
   Touching on boundaries is allowed (consistent with your Kaggle check).

This is a hard nonconvex packing problem, so we solve heuristically.

---

## 2) Recommended algorithmic framing

Use a **two-level approach**:

### Level A — Feasibility solver at fixed (L)

Given (L), try to find placements ((x_i,y_i,\theta_i)) that satisfy constraints.

You can do this with:

* Metropolis–Hastings / simulated annealing on an energy
* or local search + collision resolution
* or CMA-ES, etc.

But MH is fine as your baseline.

### Level B — Outer search on (L)

Find the smallest feasible (L) by:

* bracketing + binary search, or
* decreasing schedule (start large, shrink L, re-optimize).

Binary search works if feasibility is “approximately monotone” in practice.

---

## 3) What “energy” should be for MH (polygons)

For a fixed (L), define an energy:

[
E = \lambda_{\text{overlap}} \cdot \sum_{i<j} \text{penalty_overlap}(P_i,P_j)
;+;
\lambda_{\text{out}} \cdot \sum_i \text{penalty_outside}(P_i, L)
;+;
\lambda_{\text{compact}} \cdot \text{compactness}(P_1,\dots,P_n)
]

Where:

### A) Overlap penalty (fast + stable)

For feasibility, the clean boolean constraint is:

* overlap iff `intersects` and not `touches`

But for energy you want a **continuous-ish** penalty. Options:

1. **Intersection area** (best signal; slower):

* `polyA.intersection(polyB).area`

2. **Binary overlap count** (fast; coarse):

* `1.0 if overlap else 0.0`

Start with (2) for correctness; upgrade to (1) once pipeline works.

### B) Outside penalty (containment)

Fast approximation:

* use bounds violation: if `poly.bounds` exceed square bounds, penalize by squared distance outside.
  This is conservative but usually fine for axis-aligned square.

### C) Compactness term (optional but helps mixing)

Even at fixed (L), you want to encourage clustering rather than drifting.
Example:

* penalize bounding square side of current placement, or
* penalize centroid distance to origin.

This improves search even before you tighten L.

---

## 4) Proposal moves (state space)

State is ((x_i,y_i,\theta_i)_{i=1}^n).

Proposals:

1. pick random polygon (i)
2. propose:

   * (x_i' = x_i + \mathcal{N}(0,\sigma_x))
   * (y_i' = y_i + \mathcal{N}(0,\sigma_y))
   * (\theta_i' = \theta_i + \mathcal{N}(0,\sigma_\theta)) (wrap mod 360)

Add occasional “global jitter” moves later.

---

## 5) Outer search strategy for (L)

### Step 1 — Find an initial feasible upper bound (L_\text{hi})

* Place polygons on a grid with huge spacing and compute bounding side.
* Or start with your current Kaggle placements and compute bounding side.

### Step 2 — Lower bound (L_\text{lo}) (cheap)

Use area:
[
L_{\text{area}} = \sqrt{\frac{n \cdot \text{area}(P)}{\phi}}
]
with (\phi \approx 0.6)–0.85 as a rough achievable packing fraction.
Also use diameter lower bound:
[
L \ge 2 \cdot r_{\text{circum}}
]
where (r_{\text{circum}}) is bounding circle radius of the polygon.

Then:
[
L_\text{lo} = \max(L_{\text{area}}, 2r_{\text{circum}})
]

### Step 3 — Binary search

Repeat:

* (L = (L_\text{lo}+L_\text{hi})/2)
* run feasibility solver at L (warm-start from previous best)
* if feasible: set (L_\text{hi}=L)
* else: set (L_\text{lo}=L)

Stop after fixed iterations or when ((L_\text{hi}-L_\text{lo})) small.

---

## 6) How to build this incrementally (so you code it)

### Phase 1: Deterministic geometry + constraints (no MH yet)

Implement:

* `tree_base_polygon()`
* `pose_to_polygon(x,y,deg)` (rotate+translate)
* `bounds_violation(poly, L)`
* `overlap(polyA, polyB)` with “touch allowed”
* `bounding_square_side(polys)` without unary_union

Write tests for these. Get them green.

### Phase 2: Feasibility check for a full configuration

Implement:

* `is_feasible(state, L, tol)`:

  * boundary violation <= tol
  * no overlaps (using STRtree)

Write tests on small handcrafted cases:

* two shapes far apart => feasible
* overlapping => infeasible
* touching exactly => feasible

### Phase 3: Energy function

Implement a first energy:

* overlap_count penalty + bounds violation penalty + mild compactness

Write tests:

* energy increases when you move a shape outside
* energy decreases when you separate overlapping pair

### Phase 4: MH kernel + seed reproducibility

Implement:

* `propose_move`
* `mh_step`
* `run_chain(L, steps, seed)`

Tests:

* reproducibility with fixed seed
* guaranteed acceptance when energy decreases (inject proposer)

### Phase 5: Outer L search

Implement:

* `find_min_L(n, ...)` with warm-starting

Test:

* N=1: minimal L equals tree’s own bounding side (for chosen rotation) or at least >= that.
* N=2: should reduce compared to naive huge upper bound.

---

## 7) Testing plan (exactly what to test)

### Unit tests (fast, deterministic)

1. **Touching vs overlap** using rectangles (simplest)
2. **Bounds violation** for known polygon position
3. **Bounding side** aggregation correctness (min/max over bounds)
4. **STRtree vs brute force** pair detection agreement on small random set

### MH kernel tests (controlled)

5. **Acceptance logic**: with injected proposer returning lower energy, always accept.
6. **Seed reproducibility**: same seed => same final energy (after 50–200 steps).

### Integration smoke tests (stochastic)

7. For n=3 with large L, chain should reach feasibility within K steps (use generous K but small n).

---

## 8) Key performance design choices (you should plan for now)

* Do not rebuild `ChristmasTree` polygons from scratch for every proposal if you can avoid it.

  * Keep a base polygon.
  * Only transform the moved shape in a proposal.
* Incremental collision checking:

  * If you move only shape i, only check i against neighbors, not all pairs.
* Use bounding boxes / bounding circles to skip expensive intersection calls.

These are later optimizations; correctness first.

---

If you confirm one detail—**is the square axis-aligned and not allowed to rotate** (as in your current metric)?—then I can translate this plan into a clean function API you can implement, and a pytest suite skeleton that matches your exact “touch allowed” rule and scaling scheme.
