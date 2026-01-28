import sys

H, M = list(map(int, sys.stdin.readline().split()))

if M >= 45:
    M -= 45
elif M < 45:
    if H == 0:
        H = 23
        M += 15
    else:
        H -= 1
        M += 15

print(H, M)