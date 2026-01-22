# Python - Module & Control of Flow

## 모듈

**한 파일로 묶인 변수와 함수의 모음**

**특정한 기능을 하는 코드가 작성된 파이썬 파일(.py)**

- **모듈 예시**
  - math 내장 모듈
    - 파이썬이 미리 작성해 둔 수학 관련 변수와 함수가 작성된 모듈
    ```python
    import math

    print(math.pi) # 3.141592653589793

    print(math.sqrt(4)) # 제곱근, 2.0
    ```

## 모듈 활용

**import 문 사용**
- 같은 이름의 함수가 여러 모듈에 있을 때 충돌 방지
  - `.(dot)` 연산자
    - '점의 왼쪽 객체에서 점의 오른쪽 이름을 찾아라' 라는 의미
    ```python
    import math

    print(math.pi) # 모듈명.변수명
    print(math.sqrt(4)) # 모듈명.함수명
    ```
- 단점
  - 자칫 코드가 길어질 수 있음

**from 절 사용**
- 코드가 짧고 간결해짐
  ```python
  from math import pi, sqrt

  print(pi)      # 변수명
  print(sqrt(4)) # 함수명
  ```

- 단점
  - 정의된 모듈의 위치를 알기 어려워 명시적이지 않을 수 있음
  
  - 사용자가 선언한 변수 또는 함수와 겹치게 되어 모듈에서 정의한 값이나 동작이 이루어 지지 않을 수 있음
    ```python
    from math import sqrt
    math_result = sqrt(16) # 실수형 4.0

    def sqrt(x):    # 사용자가 정의한 sqrt 함수
        return str(x ** 0.5)
    my_result = sqrt(16)   # 문자열 4.0
    ```

**from절 사용시 주의사항**

- 서로 다른 모듈에서 import된 변수나 함수의 이름이 같은 경우 이름 충돌 발생
  - 마지막에 import 된 것이 이전 것을 덮어쓰기 때문에, 나중에 import된 것만 유효함
     ```python
    # from 절 사용 주의 사항
    ## 같은 이름인 경우 덮어쓰기 주의
    from math import sqrt  # math.sqrt가 먼저 import됨
    from my_math import sqrt  # my_math.sqrt가 math.sqrt를 덮어씀

    result = sqrt(9)  # math.sqrt가 아닌 my_math.sqrt가 사용됨
    ```

- 모든 요소를 한번에 import 하는 * 표기는 권장하지 않음
  ```python
    # from 절 사용 주의 사항
    ## 모든 요소를 한 번에 import 하는 * 은 권장하지 않음
    from math import *
    from my_math import sqrt, tangent  # 어느 함수가 math 모듈과 중복되는지 모름

    # 아래는 사용자가 임의로 정의한 변수들
    a = 100
    c = 200
    e = 300  # math 모듈의 자연상수 e를 사용할 수 없게 됨
    ```

**`as` 키워드**

- as 키워드를 사용하여 별칭(alias)을 부여
  - 두 개 이상의 모듈에서 동일한 이름의 변수, 함수 클래스 등을 가져올 때 발생하는 이름 충돌 해결
  ```python
    ## as 키워드 사용 1
    from math import sqrt
    from my_math import sqrt as my_sqrt

    print(sqrt(4))  # 2.0
    print(my_sqrt(4))  # 2.0
    ```

- import되는 함수나 변수명이 너무 길거나 자주 사용해야 할 경우 `as` 키워드로 별칭을 정의해 쉽게 사용
```python
## as 키워드 사용 2
## (참고) pandas와 matplotlib 패키지 설치해야 정상 동작
import pandas as pd
import matplotlib.pyplot as plt

# 별칭을 부여하지 않으면 길고 불편함
df = pandas.DataFrame()
matplotlib.pyplot.plot(x, y)

# 별칭을 사용하면 짧고 편리
df = pd.DataFrame()
plt.plot(x, y)
```

**직접 정의한 모듈 사용하기**

- my_math.py 생성하여 두 수의 합을 구하는 add 함수 작성
    ```python
    # my_math.py
    def add(x, y):
        return x + y
    ```

- 같은 위치에 sample.py 파일을 생성하고 `my_math` 모듈의 `add` 함수 `import` 후 `add` 함수 호출
  ```python
  # sample.py
  import my_math

  print(my_math.add(10, 20)) # 30
  ```

## 파이썬 표준 라이브러리 (Python Standard Library)
**파이썬 언어와 함께 제공되는 다양한 모듈과 패키지의 모음**

**패키지(Package)**
- 연관된 모듈들을 하나의 디렉토리에 모아 놓은 것


**직접 패키지 만들어 보기**

- 다음과 같은 구조로 폴더와 파일을 생성
- sample.py 파일을 생성
- my_package 폴더를 생성
  - my_package 폴더 내부에 math 폴더와 statistics 폴더 생성
  - my_package / math 폴더 내부에 my_math.py 파일 생성 후 다음 코드 작성
    ```python
    # my_package/math/my_math.py
    def add(x, y):
        return x + y
    ```
  - my_package / statistics 폴더 내부에 tools.py 파일 생성 후 다음 코드 작성
    ```python
    # my_package/statistics/tools.py
    def mod(x, y):
        return x % y
    ```
**직접 만든 패키지 사용하기**

- sample.py에 다음 코드를 작성해서 실행 결과 확인
    ```python
    ## 사용자 정의 패키지
    from my_package.math import my_math
    from my_package.statistics import tools

    print(my_math.add(1, 2))
    print(tools.mod(1, 2))
    ```
**패키지의 종류**

- 파이썬 표준 라이브러리 (Python Standard Library)
  
  - 파이썬을 설치하면 자동으로 사용할 수 있는 기본 라이브러리
  
    - 다양한 기능이 내장디어 있어 복잡한 작업도 쉽게 처리할 수 있음
  
    - `math`, `random`, `sys`(모듈) 및 `json`, `email`(패키지)등 다양한 모듈과 패키지가 포함됨
  
    - 별도 설치 없이 바로 `import`해서 사용 가능
  
- 파이썬 외부 패키지 (Third-party Packages)
  
  - 필요한 기능을 사용하기 위해 직접 설치해서 쓰는 패키지
  
    - 전 세계 개발자들이 만든 다양한 패키지들이 존재
  
      - 예시) 엑셀 파일 조작(pandas, openyxl) / 데이터 시각화(matplotlib) / 웹 데이터 수집(requests) 등
  
  - 사용할 패키지를 설치할 때는 `pip` 명령어를 사용

**패키지 설치**

- 최신 버전/ 특정 버전/ 최소 버전을 명시하여 설치할 수 있음
  ```PS
  $ pip install SomePackage
  $ pip install SomePackage==1.0.5
  $ pip install SomePackage>=1.0.4
  ```
**requests 외부 패키지 설치 및 사용 예시**

- requests 패키지
  
  - 파이썬에서 웹에 요청을 보내고 응답을 받는 걸 아주 쉽게 만들어주는 외부 패키지
  
- pip를 통해 requests 패키지를 설치
  ```PS
  $ pip install requests
  ```

- requests를 import 하여 웹에 데이터 요청
  ```python
  import requests

  # 공휴일 정보 API
  url = 
  "https://data.nager.at/api/v3/publicholidays/2025/KR"
  response = requests.get(url).json()
  print(response)
  ```