# 비동기

---

### 동기란?
Synchronous
프로그램의 실행 흐름이 순차적으로 실행
> 하나의 작업이 완료된 후에 다음 작업이 실행되는 방식

#### 동기 코드 예시
- 반복이 완료될 때까지 다음 작업(작업2)이 시작되지 않음
  ```js
  console.log('작업 1 시작')

  const syncTask = function () {
    for (let i = 0; i < 100000000; i++) {
        // 반복 실행 동안 잠시 대기
    }
    return '작업 완료'
  }

  const result = syncTask()
  console.log(result)

  console.log('작업 2 시작')
  ```

### 비동기란?
Asynchronous
특정 작업이 실행이 완료될 때까지 기다리지 않고 다음 작업을 즉시 실행하는 방식
> 한 작업의 완료 여부를 기다리지 않고, <span style="color:crimson">다른 작업을 동시에 수행할 수 있는 방식</span>

<br>

---

## JavaScript와 비동기


### 1. Single Thread 언어, JavaScript

* **Single Thread 정의**: 작업을 처리할 때 실제로 작업을 수행하는 주체(Thread)가 단 하나인 방식을 의미합니다. (참고: Multi-thread는 업무를 수행할 수 있는 주체가 여러 개임을 의미합니다.)
* **JavaScript의 특징**:
  * JS는 한 번에 **하나의 일만 수행할 수 있는 Single Thread 언어**로, 동시에 여러 작업을 스스로 처리할 수 없습니다.
  * 즉, 하나의 작업을 요청한 순서대로만 처리할 수 있습니다.
* **의문점**: 그렇다면 어떻게 Single Thread 언어인 JavaScript가 비동기 처리를 수행할 수 있을까요?

---

### 2. JavaScript Runtime (실행 환경)

JavaScript는 Single Thread이므로 자체적으로는 동시에 작업을 처리할 수 없지만, 이를 지원해 주는 **실행 환경(Runtime)**의 도움을 받아 비동기 처리를 수행합니다.

#### 주요 Runtime 환경
1. **브라우저 (Browser)**
2. **Node.js**
   * 웹 브라우저에서만 작동하던 JavaScript를 서버에서도 실행할 수 있게 해주는 실행 환경입니다.
   * 비동기 방식으로 작동하여 여러 요청을 동시에 처리할 수 있어, 실시간 채팅이나 스트리밍 서비스에 특히 강점이 있습니다.

---

### 3. 브라우저 환경의 비동기 처리 관련 요소

브라우저 환경에서 JavaScript가 비동기로 동작할 때 유기적으로 작용하는 4가지 핵심 요소입니다.

| 구성 요소 | 설명 |
| :--- | :--- |
| **Call Stack** | * JavaScript Engine의 영역<br>* 코드가 실행되면 함수 호출이 순서대로 쌓이는 작업 공간<br>* 기본적인 JavaScript의 Single Thread 작업 처리를 담당 |
| **Web API** | * 브라우저에서 제공하는 runtime 환경<br>* 시간이 걸리거나 언제 실행될지 모르는 비동기 작업들(예: `setTimeout`, AJAX 등)을 넘겨받아 처리하는 곳 |
| **Task Queue** | * Web API에서 처리가 완료된 비동기 콜백 함수들이 순서대로 줄을 서서 기다리는 대기열 |
| **Event Loop** | * Call Stack이 비어 있는지 끊임없이 확인(감시)<br>* Call Stack이 비는 순간, Task Queue에서 가장 오래된 작업을 꺼내어 Call Stack으로 보내는 역할 |

---

### 4. 런타임의 시각적 표현 (동작 과정 분석)

다음 코드가 브라우저 환경에서 실행되는 7단계 과정입니다.

```javascript
console.log('Hi')

setTimeout(function myFunc() {
    console.log('Work')
}, 3000)

console.log('Bye')
```

#### 단계별 흐름

* **1단계**: 코드 해석 준비 단계.
* **2단계 (`console.log('Hi')` 실행)**
  1. `console.log('Hi')` 함수가 호출되며 **Call Stack**에 쌓입니다.
  2. 동기 함수(비동기가 아님)이므로 곧바로 실행되어 처리됩니다.
  3. **Output**에 `'Hi'`가 출력되고 Call Stack에서 제거됩니다.
* **3단계 (`setTimeout` 호출)**
  1. `setTimeout(...)` 함수가 호출되어 **Call Stack**에 쌓입니다.
  2. 비동기 작업이므로 직접 처리하지 않고, **Web API** 영역으로 보낸 뒤 Call Stack에서 즉시 제거됩니다.
* **4단계 (`console.log('Bye')` 실행 및 Web API 동작)**
  1. 브라우저(Web API)가 백그라운드에서 별도로 `setTimeout` 타이머(3초) 작업을 처리하기 시작합니다.
  2. 동시에 다음 코드인 `console.log('Bye')`가 호출되어 **Call Stack**에 쌓입니다.
  3. 동기 함수이므로 즉시 처리되어 **Output**에 `'Bye'`를 출력하고 제거됩니다.
* **5단계 (타이머 완료 및 대기열 이동)**
  1. Web API에서 지정한 3초가 경과하면, 콜백 함수 `myFunc`를 **Task Queue**로 보냅니다.
  2. 콜백 함수들이 순서대로 작업이 처리될 수 있도록 대기열에서 기다립니다.
* **6단계 (Event Loop의 중재)**
  1. **Event Loop**가 Call Stack이 비어 있는지 지속해서 감시합니다.
  2. Call Stack이 완전히 비어 있는 것을 확인하면, **Task Queue**에서 가장 오래 대기한 작업인 `myFunc`를 **Call Stack**으로 이동시킵니다.
* **7단계 (콜백 함수 실행)**
  1. Call Stack으로 이동한 `myFunc()` 내부 코드가 실행됩니다.
  2. 내부의 `console.log('Work')`가 Call Stack에 쌓입니다.
  3. 동기 코드이므로 곧바로 처리되어 **Output**에 `'Work'`를 출력합니다.
  4. 실행이 완료된 함수들이 스택에서 제거되며 전체 과정이 종료됩니다.

<br>

---

# [학습 자료] Ajax 기초 및 Axios 소개

## 1. Ajax (Asynchronous JavaScript and XML)

### 1) Ajax 정의 및 특징
* **개념**: 웹 페이지 전체를 새로고침하지 않고, 백그라운드에서 서버와 데이터를 주고받는 **비동기 통신 기술**입니다.
* **효과**: 웹 페이지를 데스크톱 애플리케이션처럼 동적이고 반응형으로 만들어 주어, 현대 웹 개발의 핵심 기술 중 하나로 자리 잡았습니다.
* **예시**:
  * 구글 지도 앱을 움직여도 화면 끊김이나 전체 새로고침이 없는 경우
  * SNS에서 '좋아요' 버튼을 눌렀을 때 페이지 전환 없이 숫자만 부분적으로 바뀌는 경우

### 2) 용어 정리
* **XML**: 직접 태그를 만들어 데이터를 구조화하는 마크업 언어입니다. (※ Ajax의 'X'는 원래 XML을 의미했으나, 현재는 더 가볍고 자바스크립트에서 다루기 쉬운 **JSON** 형식을 주로 사용합니다.)
* **JSON**: 서로 다른 프로그램 간에 데이터를 편리하게 교환하기 위해 사용하는 데이터 형식입니다.
* **XMLHttpRequest (XHR)**: 웹 브라우저가 서버와 데이터를 주고받을 수 있도록 브라우저가 제공하는 자바스크립트 객체입니다.

---

### 3) 기존 방식 vs Ajax 방식 비교

| 구분 | 기존 방식 (Traditional) | Ajax 방식 |
| :--- | :--- | :--- |
| **동작 순서** | 1. 클라이언트(브라우저)에서 form을 채우고 서버로 제출 (Submit)<br>2. 서버는 처리 후 새로운 웹 페이지 전체를 작성하여 응답 전달 | 1. 클라이언트에서 XHR 객체를 생성하여 비동기 요청 전송<br>2. 서버는 필요한 부분의 데이터(JSON 등)만 처리하여 응답 |
| **화면 갱신** | 모든 요청마다 화면 전체가 **새로고침**됨 | 새로고침 없이 필요한 부분의 **DOM만 부분 업데이트** |
| **효율성** | 유사한 내용의 페이지라도 중복된 전체 코드를 다시 받아오므로 대역폭 낭비가 심함 | 서버가 처리하던 렌더링 업무의 일부를 클라이언트가 분담하여 교환되는 데이터양과 처리량이 대폭 감소 |

---

### 4) Ajax의 목적
1. **비동기 통신**: 전체 페이지를 새로고침하지 않고 백그라운드에서 서버와 데이터를 교환합니다.
2. **부분 업데이트**: 전체 로드 없이 HTML의 일부 DOM만 동적으로 갱신하여 사용자 경험(UX)을 향상합니다.
3. **서버 부하 감소**: 화면 구성을 위한 전체 HTML을 다시 받는 대신, 필요한 데이터만 요청하므로 서버 부하를 줄일 수 있습니다.

---

### 5) 이벤트 핸들러와 비동기 프로그래밍
* **XHR과 이벤트 핸들러**: HTTP 요청은 응답이 올 때까지 시간이 걸릴 수 있는 대표적인 비동기 작업입니다. XHR 객체에 이벤트 핸들러(콜백 함수)를 연결하여 요청의 진행 상태 및 최종 완료에 대응합니다.
* **TIP**:
  * 이벤트 핸들러는 코드를 막지(Block) 않습니다. 요청을 보낸 후 응답을 기다리는 동안 브라우저는 다른 작업을 처리할 수 있습니다.
  * 최근 현대적인 자바스크립트 개발에서는 XHR 이벤트 핸들러보다 **Promise**와 **async/await**를 사용하는 것이 권장됩니다.

---

## 2. Axios 소개

### 1) Axios 정의 및 특징
* **개념**: 브라우저와 Node.js 환경에서 모두 사용할 수 있는 **Promise 기반의 HTTP 클라이언트 라이브러리**입니다.
* **특징**:
  * 간편하게 Ajax 통신을 할 수 있도록 도와주는 자바스크립트 라이브러리입니다.
  * 브라우저와 Node.js 환경 모두에서 동일한 코드로 작동하는 장점이 있습니다.
  * 자동 데이터 변환(JSON), 에러 처리 등이 편리하여 실무 프로젝트에서 매우 대중적으로 사용됩니다.
  * 브라우저 환경에서는 내부적으로 **XHR 객체**를 생성하여 통신합니다.

### 2) Ajax를 활용한 클라이언트-서버 간 동작 흐름
```
[Client (Axios)] ──(XHR 객체 생성 및 요청)──> [Server]
[Client (Axios)] <──(JSON 데이터 응답)─────── [Server]
       │
       └──> [Promise 객체를 활용해 DOM 조작] (웹 페이지의 일부분만 다시 로딩)
```

---

### 3) Axios 설치 및 사용법
* **설치**: CDN 방식을 사용하여 간편하게 가져올 수 있습니다.
```html
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

* **기본 코드 예시**:
```javascript
axios({
  method: 'get',
  url: 'https://api.thecatapi.com/v1/images/search'
})
.then((response) => {
  console.log(response);      // Response 전체 객체
  console.log(response.data); // 서버가 반환한 실제 데이터
})
.catch((error) => {
  console.error(error);       // 에러 객체 출력
});
```

---

## 3. Promise 객체와 Axios 구조

### 1) "Promise" 객체 개요
* **개념**: 자바스크립트에서 비동기 작업의 최종 완료(성공) 또는 실패와 그 결과값을 나타내는 객체입니다.
* `axios()` 호출의 결과는 **Promise 객체**를 반환합니다.
```javascript
const promiseObj = axios({
  method: 'get',
  url: 'https://api.thecatapi.com/v1/images/search'
});

console.log(promiseObj); // Promise object 출력
```

### 2) Promise의 성공과 실패 처리 메서드
* **콜백 함수**: 다른 함수의 인자로 넘겨져 특정 조건이나 완료 시점에 실행되는 함수입니다.

#### ① 성공 처리: `then()`
* 비동기 작업이 성공적으로 완료되었을 때 실행할 콜백 함수를 지정합니다.
* 이전 작업의 성공 결과를 인자(예: `response`)로 전달받아 처리합니다.

#### ② 실패 처리: `catch()`
* 네트워크 오류나 서버 에러 등 예외 상황이 발생했을 때 실행할 콜백 함수를 지정합니다.
* 이전 작업의 실패 객체(예: `error`)를 인자로 전달받아 예외 처리를 진행합니다.
* 여러 `then()` 단계 중 하나라도 실패하면 실행 흐름은 중단되고 `catch()` 블록으로 넘어갑니다.

```javascript
axios({
  method: 'post',
  url: '/user/12345',
  data: {
    firstName: 'Fred',
    lastName: 'Flintstone'
  }
})
.then((response) => {
  // 성공했을 때 수행할 로직
  console.log('성공:', response.data);
})
.catch((error) => {
  // 실패(에러)했을 때 수행할 로직
  console.error('실패:', error);
});
```

<br>

---

# [학습 자료] Ajax와 Axios 활용 및 비동기 처리 패턴

## 1. Ajax와 Axios의 개념적 차이

비동기 웹 개발을 진행할 때 Ajax와 Axios는 서로 다른 계층의 개념으로 이해해야 합니다.

* **Ajax (개념이자 접근 방식)**
  * 하나의 특정 기술만을 의미하는 것이 아닙니다.
  * 비동기적인 웹 애플리케이션 개발에 사용하는 **기술들의 집합**을 지칭하는 용어입니다.
* **Axios (실현하는 구체적인 도구)**
  * 클라이언트와 서버 사이에 HTTP 요청을 만들고 응답을 처리하는 데 사용되는 **자바스크립트 라이브러리**입니다.
  * `XMLHttpRequest` 객체를 추상화하여 개발자가 더 사용하기 쉽게 가공한 도구입니다.
  * **Promise API**를 기반으로 설계되어 비동기 처리를 직관적으로 다룰 수 있게 돕습니다.
* **TIP**: 프론트엔드 실무에서는 Axios를 활용해 Django REST Framework(DRF) 등으로 구축된 API 서버에 요청을 보내고, 받아온 데이터를 비동기적으로 처리하는 로직을 구현할 때 핵심 도구로 활용됩니다.

---

## 2. 비동기 처리의 특성과 관리 방법

### 1) 비동기 처리의 핵심 특성
* 비동기 처리의 본질은 작업이 시작되는 순서가 아니라, **완료되는 순서**에 따라 순차적으로 처리된다는 점입니다.
* **단점**: 개발자 입장에서 코드가 작성된 위아래 방향대로의 실행 순서가 보장되지 않으므로(**실행 순서의 불명확성**), 실행 결과를 정확하게 예측하며 코드를 작성하기 까다로울 수 있습니다.

### 2) 비동기 처리 관리 방법
이러한 실행 순서 제어 문제를 해결하기 위해 두 가지 핵심 관리 방안을 사용합니다.
1. **비동기 콜백**: 비동기 작업이 완료된 후 실행할 함수를 실행 시점에 미리 정의해 두는 방식입니다.
2. **Promise**: 비동기 작업의 최종 완료 또는 실패 상태를 나타내는 객체를 활용하는 방식입니다.

---

## 3. 비동기 콜백과 콜백 지옥 (Callback Hell)

### 1) 비동기 콜백 (Asynchronous Callback)
* 비동기식으로 처리되는 작업이 완전히 끝났을 때 연이어 실행되도록 약속된 함수입니다.
* 연쇄적으로 발생하는 비동기 작업을 순차적으로 동작하게 조율하여, 작업 순서와 동작을 제어하거나 결과를 처리할 때 사용합니다.

```javascript
const asyncTask = function (callback) {
  setTimeout(function () {
    console.log('비동기 작업 완료')
    callback() // 비동기 작업이 끝난 시점에 콜백 호출
  }, 2000) // 2초 후 작업 완료
}

// 비동기 작업 수행 후 실행할 콜백 등록
asyncTask(function () {
  console.log('작업 완료 후 콜백 실행')
})

// [출력 결과]
// 비동기 작업 완료
// 작업 완료 후 콜백 실행
```

### 2) 비동기 콜백의 한계와 콜백 지옥
* 비동기 콜백은 보통 'A 작업 결과를 받아 B 작업을 처리하고, 그 결과를 다시 C 작업에 전달하는' 연쇄적인 상황에서 많이 사용됩니다.
* 이 과정을 단순 콜백 함수로만 작성하다 보면 함수 내부에 또 다른 함수가 계속 중첩되는 비슷한 패턴이 반복됩니다.
* 이로 인해 코드 형태가 마치 오른쪽으로 깊어지는 피라미드 형태를 띠게 되며, 이를 **콜백 지옥(Callback Hell)** 혹은 **파멸의 피라미드(Pyramid of Doom)**라고 부릅니다.

```javascript
// 콜백 지옥의 예시 구조
function hell (win) {
  return function () {
    loadLink(win, REMOTE_SRC, function () {
      loadLink(win, REMOTE_SRC, function () {
        loadLink(win, REMOTE_SRC, function () {
          loadLink(win, REMOTE_SRC, function () {
            // 깊은 중첩 구조 형성...
          })
        })
      })
    })
  }
}
```
* **문제점**: 코드 가독성을 극도로 해치며 코드의 흐름 파악 및 디버깅, 유지보수가 매우 어려워집니다.
* **해결책**: 이러한 문제를 보완하기 위해 자바스크립트는 **Promise 객체**를 도입했습니다.

---

## 4. Promise 객체와 Chaining

### 1) Promise 개요
* **정의**: "비동기 작업이 끝나면 결과값(또는 실패 시 에러)을 반환해 줄게"라는 약속을 나타내는 객체입니다.
* 콜백 지옥 문제를 해결하고 비동기 흐름을 선형적(Linear)으로 작성할 수 있도록 돕습니다.
* 우리가 다루는 **Axios**가 바로 이 Promise를 기반으로 동작하는 라이브러리입니다.

### 2) 비동기 콜백 방식 vs Promise 방식 코드 구조 비교

* **비동기 콜백 방식 (함수 중첩으로 코드가 깊어짐)**
  ```javascript
  work1(function () {
    // 첫 번째 작업 완료 후
    work2(result1, function (result2) {
      // 두 번째 작업 완료 후
      work3(result2, function (result3) {
        console.log('최종 결과: ' + result3)
      })
    })
  })
  ```

* **Promise 방식 (`then` 메서드를 사용한 체이닝 연결)**
  ```javascript
  work1()
    .then((result1) => {
      // work2 수행 후 결과 반환
      return result2
    })
    .then((result2) => {
      // work3 수행 후 결과 반환
      return result3
    })
    .catch((error) => {
      // 체인 전체 과정 중 발생하는 에러 일괄 처리
      console.error(error)
    })
  ```

---

### 3) 실무 실습 코드 개선 예시 (Cat API 사례)

* **개선 전 (단일 `then` 내부에서 모든 작업 처리)**
  ```javascript
  .then((response) => {
    imgUrl = response.data[0].url
    imgElem = document.createElement('img')
    imgElem.setAttribute('src', imgUrl)
    document.body.appendChild(imgElem)
  })
  ```

* **개선 후 (Chaining 적용: 첫 번째 `then`의 반환값이 다음 `then` 콜백의 인자로 전달됨)**
  ```javascript
  .then((response) => {
    imgUrl = response.data[0].url
    return imgUrl // 다음 then으로 데이터 전달
  })
  .then((imgData) => {
    // 이전 then에서 반환한 imgUrl이 imgData로 들어옴
    imgElem = document.createElement('img')
    imgElem.setAttribute('src', imgData)
    document.body.appendChild(imgElem)
  })
  ```

---

## 5. Promise Chaining이 제공하는 핵심 장점

1. **가독성 향상**
   * 비동기 작업의 순서와 의존 관계를 위에서 아래로 흐르는 단방향 코드로 명확히 표현할 수 있습니다.
2. **분할 에러 처리**
   * 체인으로 엮인 각각의 비동기 작업 단계에서 발생하는 에러를 세부적으로 분할하여 디버깅하거나 대응할 수 있습니다.
3. **유연성 제공**
   * 작업 단계마다 데이터를 가공하거나 분기를 설정하는 등, 복잡한 비동기 비즈니스 로직을 구성하기에 유리합니다.
4. **쉬운 코드 관리**
   * 각 비동기 작업을 독립된 함수 블록(`then`)으로 분리하여 구조화하므로 코드 관리 및 협업에 용이합니다.

---

## 6. Promise의 주요 이점 (전통적 콜백과의 비교 요약)

* **실행 순서의 명밀한 보장**
  * **일반 콜백**: 이벤트 루프가 현재 실행 중인 Call Stack을 완전히 완료하기 전에는 호출되지 않아 순서 조율이 간접적입니다.
  * **Promise**: `then/catch` 메서드의 콜백 함수는 Event Queue(Microtask Queue)에 배치되는 물리적 순서대로 엄격하게 보장되어 호출되므로 흐름 예측이 훨씬 직관적입니다.
* **유연한 처리 시점**
  * 비동기 작업이 이미 종료된 이후에도 `then` 메서드를 통해 콜백 함수를 추가하여 결과값을 소급해 안전하게 처리할 수 있습니다.
* **연속적인 비동기 파이프라인 형성**
  * `then` 메서드를 여러 번 연결해 여러 콜백을 순차적으로 실행할 수 있으며, 이전 Promise의 리턴값을 다음 단계의 인자로 쉽게 넘겨받아 사용합니다.
* **에러 처리의 일원화**
  * 여러 비동기 단계를 거치더라도 마지막에 단 한 번의 `catch` 메서드를 붙여 에러를 일괄적으로 수집·대응할 수 있으므로, 전통적인 콜백 방식처럼 매 단계마다 에러 핸들러를 중복 작성해야 하는 번거로움을 해결합니다.