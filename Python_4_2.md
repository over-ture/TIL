# 제어문(Control Statement)

- **코드의 실행 흐름을 제어하는 데 사용되는 구문**

- **조건에 따라 코드블록을 실행하거나 반복적으로 코드를 실행**

## 조건문
  ```python
  if score >= 90:
    message = '축하합니다! 최고입니다!'
  elif score >= 70:
    print('멋져요! 잘하셨어요!')
  else:
    print('조금 더 노력해 보세요!')
  ```

**if / elif / else**

-**조건문의 기본 구조**
  - `if` 문
    - 조건문의 기본 형태
    - `if` 문에 작성된 조건을 만족할 때 내부 코드 실행
    - 작성되는 조건은 표현식으로 작성

  - `elif` 문
    - 이전의 조건을 만족하지 못하고 추가로 다른 조건이 필요할 때 사용
    - 여러 개의 `elif` 문을 사용할 수 있음

  - `else` 문
    - 모든 조건들을 만족하지 않으면 실행됨



## 반복문
- for 반복
  ```python
  for i in range(N):
    twinkle(message)
  ```
- while 반복
- 반복문 제어 키워드
    - `break`, `continue`
  ```python
  while True:
    print('Continue? (y/n)')
    answer = input()
    if answer == 'y':
        play()
    else:
        print('Closing Game.')
        break
  ```

### for문

- 반복 가능(iterable)한 객체의 요소들을 반복하는데 주로 사용
  - 시퀀스 자료형 `(list, tuple, str)` 뿐만 아니라 비 시퀀스 자료형 `(dict, set)`등도 반복 가능한 객체

- 주로 반복 가능(iterable)한 객체 요소의 개수만큼 반복
- 특징: 반복 횟수가 정해져 있음

#### for문 작동 원리

- 리스트 내 첫 항목이 반복 변수(item)에 할당되고 코드블록이 실행
- 다음으로 반복 변수에 리스트의 2번째 항목이 할당되고 코드블록이 다시 실행
- ...마지막으로 반복 변수에 리스트의 마지막 요소가 할당되고 코드블록이 실행
- 더 이상 반복 변수에 할당할 값이 없으면 반복 종료
    ```python
    # for문 작동 원리
    item_list = ['apple', 'banana', 'coconut']

    for item in item_list:  # item: 반복 변수
        print(item)
    ```
##### 문자열 순회

- 문자열은 문자로 구성된 시퀀스 자료형
- 문자열 반복시 문자가 반복 변수에 할당되어 반복 수행
  ```python
  country = 'Korea'

  for char in country:
    print(char)
    ```
##### range 순회

- 특정 숫자 범위만큼 반복을 하고 싶을 때 `range`함수를 사용
  ```python
  for i in range(5):
    print(i)
    ```
##### 딕셔너리 순회

- dict 자료형은 비시퀀스 자료형
  ```python
  my_dict = {
    'x': 10,
    'y': 20,
    'z': 30,
  }
  
  for key in my_dict:
    print(key)
    print(my_dict[key])
    ```

##### 인덱스로 리스트 순회

- 리스트의 요소가 아닌 인덱스로 접근하여 해당 요소들을 변경하기
- 인덱스를 사용하면 리스트의 원하는 위치에 있는 값을 읽거나 변경할 수 있음
  ```python
  numbers = [4, 6, 10, -8, 5]

  for i in range(len(numbers)):
    numbers[i] = numbers[i] * 2

  print(numbers) # [8, 12, 20, -16, 10]
  ```

##### 중첩된 반복문 (1/2)

- 중첩된 반복문에서의 출력 예상해보기
  ```python
  outers = ['A', 'B']
  inners = ['c', 'd']

  for outer in outers:
    for inner in inners:
        print(outer, inner)
  ```

##### 중첩된 반복문 (2/2)

- 중첩된 반복문에서의 출력 예상해보기
  ```python
    # 중첩 반복문
    outers = ['A', 'B']
    inners = ['c', 'd']

    for outer in outers:
        for inner in inners:
            print(outer, inner)
    ```

### while문

- while 조건이 참(True)인 동안 반복 == 조건식이 거짓(False)이 될 때까지 반복해서 실행
- 반복 횟수가 정해지지 않은 경우 주로 사용

#### while문의 반복 원리

- while의 조건식 확인

  - 조건식이 참(True)면 코드 블록 실행
  - 조건식이 거짓(False)면 반복 종료
  - **코드 블록 실행이 마무리되면 다시 while 조건식 확인**
  ```python
    a = 0

    while a < 3:
        print(a)
        a += 1
    print('End')
    ```

##### 사용자 입력에 따른 반복

- while문을 사용한 특정 입력 값에 대한 종료 조건 활용하기
  ```python
    # while문 사용자 입력에 따른 반복
    number = int(input('양의 정수를 입력해주세요.: '))

    while number <= 0:
        if number < 0:
            print('음수를 입력했습니다.')
        else:
            print('0은 양의 정수가 아닙니다.')

        number = int(input('양의 정수를 입력해주세요.: '))

    print('잘했습니다!')
    ```

##### while문의 특징

- **반드시 종료 조건이 필요**
  - 종료 조건이 없는 경우 무한 반복에 빠지게 되어 원하는 동작을 하지 않게 되므로 반드시 종료 조건을 설정해야 함

### 이론

#### for 반복문

- iterable 요소를 하나씩 순회하며 반복
- 반복 횟수가 명확하게 정해져 있는 경우 유용
  - 리스트, 튜플, 문자열 등과 같은 시퀀스 형식 처리할 경우
  - range() 함수를 사용해 일정 횟수만큼 반복 작업을 수행할 경우

#### while 반복문

- 주어진 조건식이 참(True)인 동안 반복
- 반복 횟수가 불명확하거나 조건에 따라 반복을 종료해야 할 때 유용
  - 사용자의 입력을 받아서 특정 조건이 충족될 때까지 반복하는 경우
  - 반복 횟수가 미리 정해져 있지 않고, 특정 조건이 만족될 때까지 반복해야 하는 경우

#### 반복 제어

- 때때로 일부만 실행하는 것이 필요할 때가 있다

#### 반복 제어 키워드

##### break
  - 해당 키워드를 만나게 되면 남은 코드를 무시하고 반복 즉시 증료
  - 반복을 끝내야 할 명확한 조건이 있을 때 사용
    ```python
    # break 키워드 기본
    for i in range(10):
        if i == 5:
            break
        print(i)  # 0 1 2 3 4
        ```
###### break 예시 (1/2)

- 리스트에서 첫 번째 짝수만 찾은 후 반복 종료하기
  ```python
    # break 키워드 예시 (for문)
    # 리스트에서 첫번째 짝수만 찾은 후 반복 종료하기
    numbers = [1, 3, 5, 6, 7, 9, 10, 11]
    found_even = False

    for num in numbers:
        if num % 2 == 0:
            print('첫 번째 짝수를 찾았습니다:', num)
            found_even = True
            break

    if not found_even:
        print('짝수를 찾지 못했습니다')
    ```

###### break 예시 (2/2)

- 프로그램 종료 조건 만들기
    ```python
    # break 키워드 예시 (while문)
    # 프로그램 종료 조건 만들기
    number = int(input('양의 정수를 입력해주세요.: '))

    while number <= 0:
        if number == -9999:
            print('프로그램을 종료합니다.')
            break

        if number < 0:
            print('음수를 입력했습니다.')
        else:
            print('0은 양의 정수가 아닙니다.')

        number = int(input('양의 정수를 입력해주세요.: '))
    print('잘했습니다!')
    ```
    
##### continue
- 해당 키워드를 만나게 되면 다음 코드는 무시하고 다음 반복을 수행
  
###### continue 예시
- 리스트에서 홀수만 출력하기
  ```python
    # continue 키워드 예시
    # 리스트에서 홀수만 출력하기
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for num in numbers:
        if num % 2 == 0:
            continue
        print(num)
    ```

##### 빈 코드 블록 키워드
- `pass`
  - '아무 동작도 하지 않음'을 명시적으로 나타내는 키워드
  - 반복 제어가 아닌 코드의 틀을 유지하거나 나중에 내용을 채우기 위한 용도로 사용
  - 코드를 비워두면 오류가 발생하기 때문에 `pass` 키워드를 사용함
  - 반복문 뿐만 아니라 함수, 조건문에서도 사용 가능


## 유용한 내장 함수 map & zip

### map 함수

**map(function, iterable)**
  - 반복 가능한 데이터구조(iterable)의 모든 요소에 function을 적용하고, 그 결과 값들을 map object로 묶어서 반환
    ```python
        # map 함수 사용 기본
    numbers = [1, 2, 3]
    result = map(str, numbers)

    print(result)  # <map object at 0x00000239C915D760>
    print(list(result))  # ['1', '2', '3']
    ```

#### map 함수 활용 1

- SWEA 문제의 input처럼 문자열 '1 2 3'이 입력 되었을 때 활용 예시
  ```python
  numbers1 = input().split()
  print(numbers1) # ['1', '2', '3']

  numbers2 = list(map(int, input().split()))
  print(numbers2) # [1, 2, 3]
  ```

#### map 함수 활용 2 (with 람다 활용식)

```python
# map 함수 활용 2 - lambda와 함께 사용
numbers = [1, 2, 3, 4, 5]


def square(x):
    return x**2


# lambda 미사용
squared1 = list(map(square, numbers))
print(squared1)  # [1, 4, 9, 16, 25]

# lambda 사용
squared2 = list(map(lambda x: x**2, numbers))
print(squared2)  # [1, 4, 9, 16, 25]
```

### zip 함수

**zip(`*iterables`)**
  - zip 함수는 여러 개의 반복 가능한 데이터 구조를 묶어서, 같은 위치에 있는 값들을 하나의 tuple로 만든 뒤 그것들을 모아 zip object로 반환

#### zip 함수 활용 1
  - 여러 개의 리스트를 동시에 조회할 때
  ```python
    # zip 함수 활용
    kr_scores = [10, 20, 30, 50]
    math_scores = [20, 40, 50, 70]
    en_scores = [40, 20, 30, 50]

    for student_scores in zip(kr_scores, math_scores, en_scores):
        print(student_scores)
  ```
#### zip 함수 활용 2
  - 2차원 리스트의 같은 컬럼(열) 요소를 동시에 조회할 때
  - 실행 결과과 전치 행렬과 동일함
  ```python
    # zip 함수 활용 (전치 행렬)
    scores = [
        [10, 20, 30],
        [40, 50, 39],
        [20, 40, 50],
    ]

    for score in zip(*scores):
        print(score)
  ```