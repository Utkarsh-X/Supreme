import sys


def solve(n, m, L, R):
    """Return (K, ops) or (None, None) if impossible. K is min total cost."""
    ops = [0] * m

    # ---- cost 1: an operation whose interval is the whole [1, n] (type 1) ----
    for i in range(m):
        if L[i] == 1 and R[i] == n:
            ops[i] = 1
            return 1, ops

    # ---- cost 2 ----
    # (a) two type-1 ops whose intervals union to [1, n]:
    #     one op must contain 1 (L=1), one must contain n (R=n).
    #     Best pair: max R among L=1 ops, min L among R=n ops; no gap iff R* >= L* - 1.
    a_idx = -1
    maxr = -1
    for i in range(m):
        if L[i] == 1 and R[i] > maxr:
            maxr = R[i]
            a_idx = i
    b_idx = -1
    minl = n + 1
    for i in range(m):
        if R[i] == n and L[i] < minl:
            minl = L[i]
            b_idx = i
    if a_idx != -1 and b_idx != -1 and maxr >= minl - 1:
        ops[a_idx] = 1
        ops[b_idx] = 1
        return 2, ops

    # (b) inclusion: exists distinct i,j with I_j subset of I_i
    #     (op i type 1 covers I_i, op j type 2 covers everything outside I_j).
    #     Detect by sorting by (L asc, R desc) and sweeping max R.
    order = sorted(range(m), key=lambda i: (L[i], -R[i]))
    maxr = -1
    contain_idx = -1
    for j in order:
        if R[j] <= maxr:
            contain_idx = j
            break
        if R[j] > maxr:
            maxr = R[j]
    if contain_idx != -1:
        j = contain_idx
        for i in range(m):
            if i != j and L[i] <= L[j] and R[i] >= R[j]:
                ops[i] = 1
                ops[j] = 2
                return 2, ops

    # (c) disjoint pair: two type-2 ops cover everything iff I_i ∩ I_j = ∅.
    minr_i = min(range(m), key=lambda i: R[i])
    maxl_i = max(range(m), key=lambda i: L[i])
    if minr_i != maxl_i and R[minr_i] < L[maxl_i]:
        ops[minr_i] = 2
        ops[maxl_i] = 2
        return 2, ops

    # ---- cost 3 ----
    # When cost <= 2 is impossible: no inclusions, no disjoint pairs.
    # Sort by (L, R) -> strictly increasing; all pairs intersect -> L3 <= R1.
    # Type 1 on I1, type 2 on I2, type 1 on I3 covers everything (I2 ⊆ I1 ∪ I3).
    if m >= 3:
        order3 = sorted(range(m), key=lambda i: (L[i], R[i]))
        i1, i2, i3 = order3[0], order3[1], order3[2]
        ops[i1] = 1
        ops[i2] = 2
        ops[i3] = 1
        return 3, ops

    return None, None


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    L = [0] * m
    R = [0] * m
    idx = 2
    for i in range(m):
        L[i] = int(data[idx])
        R[i] = int(data[idx + 1])
        idx += 2
    k, ops = solve(n, m, L, R)
    if k is None:
        print(-1)
    else:
        print(k)
        print(' '.join(map(str, ops)))


if __name__ == "__main__":
    main()
