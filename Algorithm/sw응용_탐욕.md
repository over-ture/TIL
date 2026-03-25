# 부분집합 (powerset)

**어떤 집합의 공집합과 자기자신을 포함한 모든 부분**

```python
def recur(idx, subset):
  if idx == 3:
    print(*subset)
    return

  # 포함하는 경우
  recur(idx+1, subset, [name[idx]])
  # 안하는 경우
  recur(idx+1, subset)
```

```python
def get_subset1(target):
  # 1. 0~부분 집합의 수 만큼 반복
  # - i: 부분집합의 번호
  for i in range(1 << n):
    # i를 이진수로 생각하고, 각 자리 수를 비교
    for idx in range(n):
      if i & (1 << idx):
        print(arr[i], end=' ')
  print()
```


# 그리ㅣ