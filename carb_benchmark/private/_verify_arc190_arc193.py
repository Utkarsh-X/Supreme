import itertools
import random
import sys

import importlib.util


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r190 = _load("r190", "carb_benchmark/private/lcb__arc190_a/reference_solution.py")
r193 = _load("r193", "carb_benchmark/private/lcb__arc193_a/reference_solution.py")


# ---------------- arc190_a brute force ----------------

def brute190(n, m, L, R):
    """Exhaustive: try every assignment of op types, return min cost (or None)."""
    best = None
    best_ops = None
    for assign in itertools.product((0, 1, 2), repeat=m):
        covered = [False] * (n + 1)
        cost = 0
        for i, t in enumerate(assign):
            if t == 1:
                cost += 1
                for j in range(L[i], R[i] + 1):
                    covered[j] = True
            elif t == 2:
                cost += 1
                for j in range(1, n + 1):
                    if not (L[i] <= j <= R[i]):
                        covered[j] = True
        if all(covered[1:]):
            if best is None or cost < best:
                best = cost
                best_ops = assign
    return best, best_ops


def check_ops(n, m, L, R, ops):
    """Verify a given op assignment covers [1,n]; return cost or None."""
    covered = [False] * (n + 1)
    cost = 0
    for i, t in enumerate(ops):
        if t == 1:
            cost += 1
            for j in range(L[i], R[i] + 1):
                covered[j] = True
        elif t == 2:
            cost += 1
            for j in range(1, n + 1):
                if not (L[i] <= j <= R[i]):
                    covered[j] = True
    return cost if all(covered[1:]) else None


def test_190():
    rng = random.Random(190)
    bad = 0
    total = 0
    # exhaustive-ish: all pairs for tiny m, random for larger
    for n in range(1, 9):
        for m in range(1, 7):
            trials = 60 if m <= 4 else 25
            for _ in range(trials):
                total += 1
                L = [0] * m
                R = [0] * m
                for i in range(m):
                    l = rng.randint(1, n)
                    r = rng.randint(l, n)
                    L[i] = l
                    R[i] = r
                k, ops = r190.solve(n, m, L, R)
                bk, _ = brute190(n, m, L, R)
                if bk is None:
                    if k is not None:
                        bad += 1
                        print(f"FALSE POSITIVE n={n} m={m} L={L} R={R}: alg={k} brute=None")
                else:
                    if k != bk:
                        bad += 1
                        print(f"WRONG COST n={n} m={m} L={L} R={R}: alg={k} brute={bk}")
                    else:
                        # also verify the returned ops actually work at cost k
                        c = check_ops(n, m, L, R, ops)
                        if c != k:
                            bad += 1
                            print(f"INVALID OPS n={n} m={m} L={L} R={R}: claimed cost {k} but ops cost/cover={c}")
    print(f"arc190_a: {total} instances, {bad} failures")
    return bad


# ---------------- arc193_a brute force ----------------

def floyd(n, W, L, R):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and (R[i] < L[j] or R[j] < L[i]):
                dist[i][j] = W[i] + W[j]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                nd = dist[i][k] + dist[k][j] - W[k]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    return dist


def test_193():
    rng = random.Random(193)
    bad = 0
    total = 0
    for n in range(2, 9):
        for _ in range(60):
            total += 1
            W = [rng.randint(1, 20) for _ in range(n)]
            L = [0] * n
            R = [0] * n
            for i in range(n):
                l = rng.randint(1, 2 * n)
                r = rng.randint(l, 2 * n)
                L[i] = l
                R[i] = r
            queries = [(i, j) for i in range(n) for j in range(n) if i != j]
            got = r193.solve(n, W, L, R, queries)
            exp = floyd(n, W, L, R)
            for idx, (s, t) in enumerate(queries):
                e = exp[s][t]
                g = got[idx]
                if e == float('inf'):
                    if g != "-1":
                        bad += 1
                        print(f"CONN n={n} W={W} L={L} R={R} q=({s},{t}): alg={g} expect -1")
                else:
                    if g != str(e):
                        bad += 1
                        print(f"VAL n={n} W={W} L={L} R={R} q=({s},{t}): alg={g} expect {e}")
            if bad > 10:
                print("too many failures, stopping")
                return bad
    print(f"arc193_a: {total} instances, {bad} failures")
    return bad


if __name__ == "__main__":
    b1 = test_190()
    b2 = test_193()
    sys.exit(1 if (b1 or b2) else 0)
