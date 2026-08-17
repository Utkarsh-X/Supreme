import sys


def solve(n, W, L, R, queries):
    """
    Graph: edge (i,j) iff [L_i,R_i] and [L_j,R_j] are disjoint.
    Path weight = sum of W over vertices on the path (endpoints included).
    For each query (s,t): min path weight, or -1.
    """
    INF = float('inf')
    maxc = 2 * n + 2  # coordinates go up to 2N

    # a[i] = min W over vertices with R_v <= i   (prefix min)
    # b[i] = min W over vertices with L_v >= i   (suffix min)
    a = [INF] * (maxc + 2)
    b = [INF] * (maxc + 2)
    for i in range(n):
        if W[i] < a[R[i]]:
            a[R[i]] = W[i]
        if W[i] < b[L[i]]:
            b[L[i]] = W[i]
    for i in range(1, maxc + 2):
        if a[i - 1] < a[i]:
            a[i] = a[i - 1]
    for i in range(maxc, -1, -1):
        if b[i + 1] < b[i]:
            b[i] = b[i + 1]

    out = []
    for (s, t) in queries:
        # direct edge?
        if R[s] < L[t] or R[t] < L[s]:
            out.append(str(W[s] + W[t]))
            continue
        # A_s and A_t intersect -> A_s ∪ A_t = [LL, RR]
        LL = min(L[s], L[t])
        RR = max(R[s], R[t])
        # case 1: s -> v -> t with v disjoint from A_s ∪ A_t
        best1 = min(a[LL - 1], b[RR + 1])
        # case 2: s -> u -> v -> t with L_u > R_{argminL} and R_v < L_{argmaxL}
        if L[s] < L[t] or (L[s] == L[t] and R[s] < R[t]):
            s2, t2 = s, t
        else:
            s2, t2 = t, s
        best2 = b[R[s2] + 1] + a[L[t2] - 1]
        res = min(best1, best2)
        if res >= INF:
            out.append("-1")
        else:
            out.append(str(W[s] + W[t] + res))
    return out


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    W = [0] * n
    for i in range(n):
        W[i] = int(data[idx]); idx += 1
    L = [0] * n
    R = [0] * n
    for i in range(n):
        L[i] = int(data[idx]); R[i] = int(data[idx + 1]); idx += 2
    q = int(data[idx]); idx += 1
    queries = []
    for _ in range(q):
        s = int(data[idx]) - 1; t = int(data[idx + 1]) - 1; idx += 2
        queries.append((s, t))
    print('\n'.join(solve(n, W, L, R, queries)))


if __name__ == "__main__":
    main()
