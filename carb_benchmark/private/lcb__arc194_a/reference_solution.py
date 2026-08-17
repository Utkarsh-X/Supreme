import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    # The final stack is a subsequence K of kept elements such that every
    # maximal run of NON-kept positions has even length (each non-kept run is
    # realized as balanced push/pop pairs). This is equivalent to: kept
    # positions alternate parity, the first kept position is odd, and the last
    # kept position has the same parity as N.
    # Maximize the sum of kept elements.
    NEG = float("-inf")
    best_odd = NEG  # best sum of a valid kept subsequence ending at an odd position
    best_even = NEG
    ans = NEG
    for i in range(1, n + 1):
        v = a[i - 1]
        if i % 2 == 1:
            # can start here (first kept must be odd), or continue from an even
            cand = v  # start fresh
            if best_even != NEG:
                cand = max(cand, v + best_even)
            best_odd = max(best_odd, cand)
            if n % 2 == 1:
                ans = max(ans, cand)
        else:
            cand = NEG
            if best_odd != NEG:
                cand = v + best_odd
            best_even = max(best_even, cand)
            if n % 2 == 0:
                ans = max(ans, cand)
    if n % 2 == 0:
        ans = max(ans, 0)  # keep nothing (whole sequence = one even non-kept run)
    print(ans)

if __name__ == "__main__":
    main()
