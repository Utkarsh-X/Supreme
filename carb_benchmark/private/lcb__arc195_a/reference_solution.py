import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    a = list(map(int, data[2:2 + n]))
    b = list(map(int, data[2 + n:2 + n + m]))
    if m == 1:
        print("Yes" if a.count(b[0]) >= 2 else "No")
        return
    # leftmost embedding
    left = []
    pos = 0
    ok_l = True
    for val in b:
        while pos < n and a[pos] != val:
            pos += 1
        if pos == n:
            ok_l = False
            break
        left.append(pos)
        pos += 1
    # rightmost embedding
    right = []
    pos = n - 1
    ok_r = True
    for val in reversed(b):
        while pos >= 0 and a[pos] != val:
            pos -= 1
        if pos < 0:
            ok_r = False
            break
        right.append(pos)
        pos -= 1
    right.reverse()
    if not ok_l or not ok_r:
        print("No")
        return
    print("Yes" if left != right else "No")

if __name__ == "__main__":
    main()
