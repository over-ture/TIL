# REST API

### API
Application Programming Interface
두 소프트웨어가 서로 <span style="color:crimson">통신</span>할 수 있게 하는 <span style="color:crimson">메커니즘</span>

#### Web API

- 웹 서버 또는 웹 브라우저를 위한 API
- 현대 웹 개발은 하나부터 열까지 직접 개발하기보다 여러 <span style="color:crimson">Open API</span>들을 활용
- 대표적인 Third Party Open API 서비스 목록
  - Youtube API
  - Google Map API
  - Naver Papago API
  - Kakao Map API

---

### REST
Representational State Transfer
API Server를 개발하기 위한 일종의 <span style="color:crimson">소프트웨어 설계 방법론</span>
- 엄격한 규칙을 의미하지는 않음

#### RESTful API
"자원을 정의"하고 "자원에 대한 주소를 지정"하는 전반적인 방법을 서술

- **REST** 원리를 따르는 시스템을 **RESTful** 하다고 부른다.

#### REST에서 자원을 정의하고 주소를 지정하는 방법

- 자원의 **"식별"**
  - URI
- 자원의 **"행위"**
  - HTTP Methods
- 자원의 **"표현"**
  - JSON 데이터 (궁극적으로 표현되는 데이터 결과물)

- URL만 보고도 무슨 데이터를 어떤 방식으로 처리할지 예측 가능해야 함
- 개발 시에는 항상 <span style="color:crimson">"자원 중심 + 동작 명확화 + 일관된 응답 포맷"</span>을 기준으로 설계

---

## 자원의 식별

### URI
Uniform Resource Identifier (통합 자원 식별자)
인터넷에서 리소스(자원)을 식별하는 문자열
- 가장 일반적인 URI는 웹 주소로 알려진 <span style="color:crimson">URL</span>

---

## 🌐 URL (Uniform Resource Locator) 구조 요약
URL(통합 자원 위치)은 웹 상의 리소스 위치를 나타내는 규약입니다. 

**[기본 구조 예시]**
> `http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#SomewhereInTheDocument`

위 URL은 아래와 같은 구성 요소로 나눌 수 있습니다. *(Domain Name과 Port를 합쳐서 Authority라고 부르기도 합니다.)*

---

### 1. Scheme (or Protocol)
> 예시: `http://`
* 브라우저가 리소스를 요청하는 데 사용해야 하는 **규약**입니다.
* URL의 가장 첫 부분에 위치하여 어떤 규약을 사용하는지 나타냅니다.
* 기본적으로 웹은 **http(s)**를 요구합니다.
* 그 외에도 메일을 열기 위한 `mailto:`, 파일 전송을 위한 `ftp:` 등 다른 프로토콜도 존재합니다.

### 2. Domain Name
> 예시: `www.example.com`
* 요청 중인 **웹 서버**를 나타냅니다.
* 직접 IP 주소(예: 142.251.42.142)를 사용하는 것도 가능하지만, 사람이 외우기 어렵기 때문에 주로 사람이 읽기 쉬운 Domain Name으로 사용합니다.
* 예) 도메인 `google.com`의 IP 주소는 `142.251.42.142`

### 3. Port
> 예시: `:80`
* 웹 서버의 리소스에 접근하는 데 사용되는 **기술적인 문(Gate)**입니다.
* **HTTP 프로토콜의 표준 포트:**
  * HTTP: `80`
  * HTTPS: `443`
* **표준 포트**를 사용할 경우 작성 시 **생략이 가능**합니다.

### 4. Path
> 예시: `/path/to/myfile.html`
* 웹 서버의 **리소스 경로**를 나타냅니다.
* 초기에는 실제 파일이 위치한 물리적 위치를 나타냈지만, **오늘날은 실제 위치가 아닌 추상화된 형태의 구조**를 표현합니다.
* 예) `/articles/create/`라는 주소가 실제 `articles` 폴더 안에 `create` 폴더가 있음을 나타내는 것은 아닙니다.

### 5. Parameters
> 예시: `?key1=value1&key2=value2`
* 웹 서버에 제공하는 **추가적인 데이터**입니다.
* `?`로 시작하며, **`&` 기호로 구분되는 key-value 쌍**의 목록으로 이루어집니다.
* 서버는 리소스를 응답하기 전에 이러한 파라미터를 사용하여 추가 작업을 수행할 수 있습니다.

### 6. Anchor
> 예시: `#SomewhereInTheDocument`
* 일종의 **"북마크"** 역할을 하며, 브라우저에게 해당 지점에 있는 콘텐츠를 표시하도록 합니다.
* **중요:** `#` (fragment identifier, 부분 식별자) 이후 부분은 **서버에 전송되지 않습니다.**
* 예) `https://.../install/#quick-install-guide` 요청에서 `#quick-install-guide`는 서버에 전달되지 않고, 오직 브라우저가 문서 내 해당 지점으로 스크롤을 이동할 수 있도록 돕습니다.

---

## 자원의 행위

### HTTP Request Methods
리소스에 대한 행위
<span style="color:crimson">수행하고자 하는 동작</span>을 정의

#### 종류

- **GET**
  - 서버에 리소스의 표현을 요청
  - GET을 사용하는 요청은 데이터만 검색해야 함

- **POST**
  - 데이터를 지정된 리소스에 제출
  - 서버의 상태를 변경

- **PUT**
  - 요청한 주소의 리소스를 수정

- **DELETE**
  - 지정된 리소스를 삭제

#### status code

HTTP response status codes
특정 HTTP 요청이 <span style="color:crimson">성공적으로 완료되었는지</span> 여부를 나타냄

- **Informational responses (100-199)**  
  - 요청을 계속 진행 중이라는 중간 응답
<br>
- **Successful responses (200-299)**
  - 요청이 정상적으로 처리되었음을 의미
<br>
- **Redirection messages (300-399)**
  - 요청한 리소스가 다른 위치로 옮겨졌을 때 사용
<br>
- **Client error responses (400-499)**
  - 클라이언트 요청에 문제가 있을 때 반환
<br>
- **Server error responses (500-599)**
  - 서버 내부의 문제로 요청을 처리하지 못했을 때 사용

---

## DRF with Single Model

### Django REST Framework (DRF)
Django에서 RESTful API 서버를 쉽게 구축할 수 있도록 도와주는 <span style="color:crimson">오픈소스 라이브러리</span>

#### Serializer 정의
직렬화
- 여러 시스템에서 활용하기 위해 데이터 구조나 객체 상태를 <span style="color:crimson">재구성할 수 있는 포맷으로 변환하는 과정</span>

**Serializer**

- Serialization을 진행하여 Serialized data를 반환해주는 클래스

**ModelSerializer**

- Django 모델과 연결된 Serializer 클래스
    > `일반 Serializer와 달리 사용자 데이터를 받아 자동으로 모델 필드에 맞추어 Serialization을 진행`