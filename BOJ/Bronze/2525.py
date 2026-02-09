import sys

H, M = list(map(int, sys.stdin.readline().split()))
T = int(sys.stdin.readline())

H += T // 60
M += T % 60

if M >= 60:
    H += 1
    M -= 60
if H >= 24:
    H -= 24
    
print(H, M)
