# Cookie & Session

## HTTP

![alt text](images/HTTPintro.png)

**HTTP 특징**

1. 비 연결 지향(connectionless)
     - 서버는 요청에 대한 응답을 보낸 후 연결을 끊음
     - 클라이언트는 서버와 서로 연결되어 있는 상태가 아님![alt text](images/httpauth_01.png)

2. 무상태(stateless)
      - 연결을 끊는 순간 클라이언트와 서버 간의 통신이 끝나며 상태 정보가 유지되지 않음
      - 무상태의 의미
        - 장바구니에 담은 상품을 유지할 수 없음
        - 로그인 상태를 유지할 수 없음
  ![alt text](images/httpauth_02.png)

---

## 쿠키(Cookie)

![alt text](images/cookieintro.png)

**쿠키 특징**

- 서버가 사용자의 웹 브라우저에 전송하는 작은 데이터 조각
- 사용자 인증, 추적, 상태 유지 등에 사용되는 데이터 저장 방식
- key-value 형식의 데이터

**쿠키 사용 예시**

- 로그인 유지(세션 관리)
- 장바구니
- 언어, 테마 등 사용자 설정 기억

---

#### 쿠키 동작 예시 (1/2)

1. 브라우저가 웹 서버에 웹 페이지를 요청
2. 웹 서버는 요청된 페이지가 함께 쿠키를 포함한 응답을 브라우저에게 전송
3. 브라우저는 받은 쿠키를 저장소에 저장하고, 쿠키의 속성(만료 시간, 도메인, 주소 등)도 함께 저장됨
   ![alt text](images/cookie_ex_1.png)
   
#### 쿠키 동작 예시 (2/2)

4. 이후 브라우저가 같은 웹서버에 웹페이지를 요청할 때, 저장된 쿠키 중 해당 요청에 적용 가능한 쿠키를 포함하여 함께 전송
5. 웹서버는 받은 쿠키정보를 확인하고, 필요에 따라 사용자 식별, 세션 관리 등을 수행
6. 웹서버는 요청에 대한 응답을 보내며, 필요한 경우 새로운 쿠키를 설정하거나 기존 쿠키를 수정할 수 있음
   ![alt text](images/cookie_ex_2.png)
   
   
#### 쿠키의 작동 원리와 활용

1. **쿠키 저장 방식**
    - 브라우저(클라이언트)는 쿠키를 KEY-VALUE의 데이터 형식으로 저장
    - 쿠키에는 이름, 값 외에도 만료 시간, 도메인, 경로 등의 추가 속성이 포함됨

2. **쿠키 전송 과정**
    - 서버는 HTTP 응답 헤더의 Set-Cookie 필드를 통해 클라이언트에게 쿠키를 전송
    - 브라우저는 받은 쿠키를 저장해 두었다가, 동일한 서버에 재요청 시 HTTP 요청 Header의 Cookie 필드에 저장된 쿠키를 함께 전송
  
3. **쿠키의 주요 용도**
    - 두 요청이 동일한 브라우저에서 들어왔는지 아닌지를 판단할 때 주로 사용됨
    - 이를 이용해 사용자의 로그인 상태를 유지할 수 있음
    - 상태가 없는(stateless) HTTP 프로토콜에서 상태 정보를 기억시켜 주는 역할

  -> 서버에게 "나 로그인 된(인증된) 사용자야!" 라는 인증 정보가 담긴 쿠키를 매 요청마다 계속 보내는 것
  
#### 쿠키 사용 목적

1. **세션 관리(Session management)**
    - 로그인, 아이디 자동완성, 공지 하루 안 보기, 팝업 체크, 장바구니 등의 정보 관리

2. **개인화(Personalizaiton)**
    - 사용자 선호 설정(언어 설정, 테마 등) 저장

3. **추적, 수집(Tracking)**
    - 사용자 행동을 기록 및 분석

![alt text](images/cookieusagetip.png)

---

## 세션

![alt text](images/session_info.png)

#### 세션 작동 원리

1. 클라이언트가 로그인 요청 후 인증에 성공하면 서버가 session 데이터를 생성 후 저장

2. 생성된 session 데이터에 인증할 수 있는 session id를 발급

3. 발급한 session id를 클라이언트에게 응답 (데이터는 서버에 저장, 열쇠만 주는 것)

4. 클라이언트는 응답 받은 session id를 쿠키에 저장
![alt text](images/sessionprog_1.png)

5. 클라이언트가 다시 동일한 서버에 접속하면 요청과 함께 쿠키(session id가 저장된)를 서버에 전달

6. 쿠키는 요청 때마다 서버에 함께 전송되므로 서버에서 session id를 확인해 로그인 되어있다는 것을 계속해서 확인하도록 함

7. 사용자의 요청을 처리하고 응답

#### 세션 정리

1. <span style='color:darkred'>서버 측에서는 세션 데이터를 생성 후 저장</span>하고, 이 데이터에 접근할 수 있는 <span style='color:darkred'>세션 ID</span>를 생성
2. 이 ID를 클라이언트 측으로 전달하고, <span style='color:darkred'>클라이언트는 쿠키에 이 ID를 저장</span>
3. 이후 클라이언트가 같은 서버에 재요청 시마다 저장해 두었던 <span style='color:darkred'>쿠키도 요청과 함께 전송</span>
    - 로그인 상태 유지를 위해 로그인 되어있다는 사실을 입증하는 데이터를 매 요청마다 계속해서 보내는 것

#### 쿠키와 세션의 목적

- 클라이언트와 서버 간의 <span style='color:darkred'>상태 정보를 유지하고 사용자를 식별</span>하기 위해 사용

---

## Django Auth System

**인증의 필요성**

- 클라이언트와 서버 간의 상태 정보를 유지하기 위해서 쿠키와 세션을 사용

- 클라이언트와 서버는 각기 다른 사용자를 식별해야 하는 상태

- 그래서 사용자를 식별하기 위해서 필요한 과정이 바로 '인증(Authentication)'

- 다양한 인증이 존재
  - ID와 Password
  - 소셜 로그인 (OAuth)
  - 생체인증

-> Django에서는 사용자 인증과 관련된 가장 중요하고 기본적인 뼈대를 제공 (Django Autentication System)

### Django Authentication System

- Django에서 사용자 인증과 관련된 기능을 모아 놓은 시스템

- 인증에 중요한 기본적인 기능을 제공
  - User Model: 사용자 인증 후 연결될 User Model 관리
  - Session 관리: 로그인 상태를 유지하고 서버에 저장하는 방식을 관리
  - 기본 인증(Id/Password) 로그인/로그아웃 등 다양한 기능을 제공

**기본 User Model의 한계**

- 인증 후 사용되는 User Model은 별도의 User 클래스 정의 없이 <span style='color:darkred'>내장된 auth 앱에 작성된 User 클래스</span>를 사용했음
- 하지만 Django의 기본 `User` 모델은 username, password 등 제공되는 필드가 매우 제한적
- 추가적인 사용자 정보(예: 생년월일, 주소, 나이 등)가 필요하다면 이를 위해 기본 User Model을 변경하기 어려움
  - 별도의 설정 없이 사용할 수 있어 간편하지만, 개발자가 직접 수정하기 어려움

**내장된 auth 앱**

- 기본적으로 `username`, `password`, `email` 등의 필드를 가진 `User` 모델을 제공
- 단순히 로그인 여부만 확인하는 것을 넘어, 사용자별 또는 그룹별로 특정 행동에 대한 권한 부여가 가능
  ![alt text](images/intergrated_auth.png)
  
  
**User Model 대체의 필요성**

- 프로젝트의 특정 요구사항에 맞춰 사용자 모델을 <span style='color:darkred'>확장</span>할 수 있음
  - 이메일을 `username`으로 사용하거나, 다른 추가 필드를 포함시킬 수 있음
  - 기본 `User` 모델읠 `frist_name`, `last_name`처럼 우리 프로젝트에 필요 없는 필드를 제거하여 데이터베이스 모델을 <span style='color:darkred'>더 간결하게 관리할 수 있음</span>

---

## Login

- 클라이언트와 서버 간의 상태 정보를 유지하기 위해서 쿠키와 세션을 사용
- 클라이언트와 서버는 각기 다른 사용자를 식별해야 하는 상태
- 서버에 "나"임을 인증하는 과정이 바로 "Login"

-> 결국 Login은 <span style='color:darkred'>인증(id/password)</span>을 완료하고, <span style='color:darkred'>Session을 만들고 클라이언트와 연결</span>하는 것
![alt text](images/loginprog_1.png)

#### 로그인 기능 구현

![alt text](images/logincode_1.png)
![alt text](images/logincode_2.png)
![alt text](images/login_authform.png)
![alt text](images/logincode_3.png)
![alt text](images/logincode_4.png)
![alt text](images/logincode_5.png)

## Template with authentication data

- 템플릿에서 인증 관련 데이터를 출력하는 방법

**현재 로그인 되어 있는 유저 정보 출력하기**

- `user`라는 `context` 데이터를 사용할 수 있는 이유는?
  - django가 미리 준비한 context 데이터가 존재하기 때문(context processors)
  ![alt text](images/contextprocessors.png)
  
**context processors**

- 템플릿이 렌더링 될 때 호출 가능한 컨테스트 데이터 목록
- 작성된 컨텍스트 데이터는 기본적으로 템플릿에서 사용 가능한 변수로 포함됨
- django에서 자주 사용하는 데이터 목록을 미리 템플릿에 로드 해 둔 것
  ```python
  # settings.py
  
  TEMPLATES = [
    {
      ...,
      'OPTIONS': {
        'context_processors': [
          'django.template.context_processors.request',
          'django.contrib.auth.context_processors.auth',  # 바로 여기
          'django.contrib.messages.context_processors.messages',
        ],
      }
    },
  ]
  ```