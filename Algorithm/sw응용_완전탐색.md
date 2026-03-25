# 재귀

### 재귀호출로 N중 for문 구현

- N 입력후  1 1 1... ~ 3 3 3 ... 출력 문제는 for문으로 구현 어려움

- 아래처럼 재귀호출로 구현할 수 있다.

  ```python
  path = []
  N = 3

  def run(lev):
    if lev == N:
      print(path)
      return
    for i in range(1, 4):
      path.append(i)
      run(lev + 1)
      path.pop()
  # N = int(input())
  run(0)
  ```
### 재귀함수

- 재귀함수: 자기자신을 호출하는 함수

  - 끝나는 지점이 필요하구나!
    1. 시작
    2. 끝
    3. 누적된 값

```python
# 0 ~ 10을 출력
# 0부터 시작
# 10에서 종료 (10보다 커지면 종료)
# 다음 재귀 호출: num을 1씩 증가
def recur(num):
  if num > 10:
    return
  print(num, end = ' ')
  retur(num + 1)

recur(0) # 0 1 2 3 4 5 6 7 8 9 10
```

# 순열

## 순열이란?

- 서로 다른 N개에서, **R개를 중복 없이, 순서를 고려**하여 나열하는 것

- 중복 순열

  ```python
  path = []
  # 
  def recur(cnt):
    if cnt == 2:
      print(path)
      return
      
    # 1번의 선택에서 3가지 경우의 수
    for i in range(3):
      path.append(i)  # 해당 숫자를 경로에 추가
      recur(cnt + i)
      path.pop()      # 숫자를 뽑은 적이 없도록 초기화

    # 0을 선택
    # path.append(0)
    # recur(cnt + 1)

    # 1을 선택
    # path.append(1)
    # recur(cnt + 1)

    # 2를 선택
    # path.append(2)
    # recur(cnt + 1)

  recur(0)
  ```

- 심화 - 경로를 전역변수 쓰지 않고
  - 경로를 누적하면서 파라미터로 전달한다.
  ```python
  def recur2(cnt, p):
    if cnt == 2:
      print(*p)
      return
    
    for i in range(3):
      recur2(cnt, p + [i])

  recur2(0, [])
  ```

- 중복없애기

  ```python
  path = []
  N = 3
  used = [0] * N # N개의 종류가 있을 경우 N개 만큼 만든다.

  def recur2(cnt):
    if cnt == 3:
      print(*path)
      return
    
    for i in range(3):
      if used[i]:   # 이미 i를 사용한적 있다면
        continue

      used[i] = 1   # 방문처리
      path.append(i)
      recur2(cnt + 1)
      path.pop()
      # used[i] = 0

  recur2(0)