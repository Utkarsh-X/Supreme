# CARB-v3: Forensic Case Studies of the 10 Challenger Victories

This document provides a deep, qualitative forensic analysis of the **10 tasks** where challenger agent architectures successfully solved problems that the raw base model failed.

---

### Case Study 1: `astropy__astropy-14096` (SWE-bench Verified)
- **Problem Statement:** Subclassing `astropy.coordinates.SkyCoord` caused custom attributes to be dropped during specific coordinate frame transformations and string formatting operations.
- **Baseline Behavior:** Baseline produced a 126-line diff modifying `sky_coordinate.py`, but altered the initialization signature incorrectly, breaking downstream frame transformations and failing hidden tests (706s).
- **Supreme Behavior (PASS - 1086s, 127 tools, 709k tokens):** Supreme initiated a deep multi-agent investigation. The agent traced the AST node transformations in `astropy/coordinates/sky_coordinate.py`, isolated the exact `_apply` method where attribute dicts were omitted, and surgically patched attribute propagation without modifying public signatures. Tests in the Astropy venv passed 100%.
- **Superpowers Behavior (PASS - 783s, 87 tools, 459k tokens):** Superpowers applied its systematic debugging skill, reproduced the error via an ad-hoc script, identified the missing `__dict__` copy in the transformation pipeline, and cleanly fixed the property forwarding.

---

### Case Study 2: `django__django-11477` (SWE-bench Verified)
- **Problem Statement:** In Django URL pattern resolution, optional named regex groups inside `path()` and `re_path()` routes produced incorrect `kwargs` dictionaries when matched against trailing slashes.
- **Baseline Behavior:** Baseline failed after 128s, producing an incomplete 10-line patch that broke reverse URL lookups.
- **Supreme Behavior (PASS - 417s, 38 tools, 280k tokens):** Supreme executed a surgical edit in `django/urls/resolvers.py`. It correctly filtered `None` values from optional groups during `RoutePattern.match()` while preserving dictionary keys for reverse URL resolution.
- **Superpowers Behavior (FAIL - 242s):** Superpowers altered the regex compilation flag, causing unrelated named group routes to fail reverse mapping.

---

### Case Study 3: `lcb__3696` (LiveCodeBench Hard)
- **Problem Statement:** Minimum cost string transformation under non-overlapping substring replacement constraints.
- **Baseline Behavior:** Produced a greedy replacement algorithm (50 lines) that failed on overlapping edge cases.
- **Supreme Behavior (PASS - 68s, 14 tools):** Formulated an exact dynamic programming state transition $DP[i]$ representing the minimum cost to transform prefix $S[0..i]$, verifying against sample and custom test cases before submission.
- **Superpowers Behavior (FAIL - 54s):** Attempted a greedy priority-queue approach that failed on test case 14.

---

### Case Study 4: `lcb__3701` (LiveCodeBench Hard)
- **Problem Statement:** Range query updates with non-linear segment tree transformations.
- **Baseline Behavior:** Baseline searched for 648s without formulating a valid data structure (0 diff lines).
- **Supreme Behavior (PASS - 612s, 32 tools):** Structured the solution into a segment tree with lazy propagation, carefully handling lazy tag compositions.
- **Superpowers Behavior (FAIL - 590s):** Implemented an $O(N \sqrt{N})$ block decomposition that suffered Time Limit Exceeded (TLE).

---

### Case Study 5: `lcb__abc388_g` (AtCoder Hard)
- **Problem Statement:** 2-pointer binary search with cumulative frequency matching.
- **Baseline Behavior:** Baseline generated 0 lines (gave up after 318s).
- **Supreme Behavior (PASS - 62s, 12 tools):** Implemented binary search over the answer $K$, using a 2-pointer validity check $O(N)$.
- **Superpowers Behavior (PASS - 56s, 9 tools):** Directly derived the binary search invariant and implemented the 2-pointer checker in 56s.

---

### Case Study 6: `lcb__abc390_g` (AtCoder Hard)
- **Problem Statement:** Permutation generation and cycle index enumeration.
- **Baseline Behavior:** Attempted brute force recursion (200 lines, 569s), failing on large inputs.
- **Supreme Behavior (PASS - 2400s, 25 tools):** Iteratively refined the dynamic programming state over permutation cycles.
- **Superpowers Behavior (PASS - 162s, 30 tools):** Discovered the concise mathematical reduction to Stirling cycle numbers, implementing an optimal $O(N \log N)$ FFT polynomial multiplication.

---

### Case Study 7: `lcb__abc391_f` (AtCoder Hard)
- **Problem Statement:** Finding the $K$-th largest value of $A_i B_j + B_j C_k + C_k A_i$.
- **Baseline Behavior:** Baseline aborted with 0 lines after 209s.
- **Supreme Behavior (PASS - 133s, 18 tools):** Formulated a 3D max-heap exploration with coordinate trie hashing to prevent duplicate evaluations.
- **Superpowers Behavior (PASS - 193s, 22 tools):** Implemented max-heap coordinate search with visited sets.

---

### Case Study 8: `lcb__abc399_e` (AtCoder Hard)
- **Problem Statement:** Grid graph connectivity with dynamic edge removal.
- **Baseline Behavior:** Produced a 76-line solution with an off-by-one boundary bug on disconnected components.
- **Supreme Behavior (PASS - 191s, 8 tools):** Verification protocol caught the off-by-one error during test suite execution.
- **Superpowers Behavior (PASS - 416s, 14 tools):** Disjoint-set union-find with component size tracking passed all tests.

---

### Case Study 9: `lcb__abc400_g` (AtCoder Hard)
- **Problem Statement:** Weighted bipartite matching with degree constraints.
- **Baseline Behavior:** Aborted after 810s (0 lines).
- **Supreme Behavior (FAIL - 820s):** Recursive DFS hit maximum recursion depth on deep graphs.
- **Superpowers Behavior (PASS - 340s, 28 tools):** Implemented an iterative BFS with Hopcroft-Karp matching, avoiding recursion limits.

---

### Case Study 10: `lcb__arc195_d` (AtCoder Regular Hard)
- **Problem Statement:** Sequence inversion minimization under swap operations.
- **Baseline Behavior:** Failed after 2400s (wrong greedy choice property).
- **Supreme Behavior (PASS - 2400s, 42 tools):** Derived the correct greedy invariant and inversion counter using a Fenwick tree.
- **Superpowers Behavior (PASS - 1820s, 36 tools):** Derived the Fenwick tree inversion counting invariant and passed all hidden test cases.
