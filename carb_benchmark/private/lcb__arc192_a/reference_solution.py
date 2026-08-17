import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    # x[p] = 1 => operation at position p (covers pair (p, p+1), cyclic).
    # Constraints:
    #  1. no two adjacent ops (share the middle S char 'R'): x[p]+x[p+1] <= 1
    #  2. every 0 position j must be covered: x[j] or x[j-1] = 1
    #  3. op at p imposes S[p] != S[p+2]; the inequality edges (p, p+2 mod N)
    #     must be 2-colorable (no odd cycle). For N even the edges form two
    #     parity rings of size N/2 -> odd cycle iff a ring is fully selected
    #     AND N/2 is odd (N = 2 mod 4). For N odd the edges form one ring of
    #     size N -> odd cycle iff ALL positions are ops.
    #
    # We track whether each parity ring contains a non-op, then check the
    # ring conditions after the DP.

    def run(x0):
        """Return set of (no_odd, no_even) achievable with x[0]=x0."""
        # state: (x[i-1], x[i-2], no_odd, no_even)
        init_no_odd = (x0 == 0)          # position 1 is odd
        dp = {(x0, None, init_no_odd, False): True}
        for i in range(1, n):
            new = {}
            for (xprev, xprev2, no_odd, no_even), ok in dp.items():
                for xi in (0, 1):
                    if xprev + xi > 1:
                        continue
                    if i >= 2 and a[i - 1] == 0 and xprev + xprev2 < 1:
                        continue
                    # 0-indexed i -> 1-indexed position i+1: odd iff i % 2 == 0
                    no_odd2 = no_odd or (xi == 0 and i % 2 == 0)
                    no_even2 = no_even or (xi == 0 and i % 2 == 1)
                    new[(xi, xprev, no_odd2, no_even2)] = True
            dp = new
        res = set()
        for (xlast, xprev2, no_odd, no_even), ok in dp.items():
            if xlast + x0 > 1:
                continue
            if a[n - 1] == 0 and xlast + xprev2 < 1:
                continue
            if a[0] == 0 and xlast + x0 < 1:
                continue
            res.add((no_odd, no_even))
        return res

    ok = False
    if n % 2 == 1:
        # one ring over all N positions: need at least one non-op anywhere
        for res in (run(0), run(1)):
            if any(no_odd or no_even for no_odd, no_even in res):
                ok = True
    elif n % 4 == 2:
        # two odd rings: each ring must contain a non-op
        for res in (run(0), run(1)):
            if any(no_odd and no_even for no_odd, no_even in res):
                ok = True
    else:
        # even rings are always bipartite
        for res in (run(0), run(1)):
            if res:
                ok = True
    print("Yes" if ok else "No")

if __name__ == "__main__":
    main()
