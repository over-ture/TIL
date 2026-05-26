# Vue.js 3 기초 및 기본 문법

## 1. Vue.js 소개

### Vue 란?
*   사용자 인터페이스(UI)를 구축하기 위한 **JavaScript 프레임워크**입니다.
*   레고 블록처럼 재사용 가능한 부품(**컴포넌트**)으로 화면을 조립합니다.
*   데이터가 바뀌면 화면도 자동으로 바뀌는 **'반응성'**이 가장 큰 특징입니다.
*   2014년 Evan You(전 Angular 개발팀)에 의해 발표되었으며, 현재 **최신 버전은 "Vue 3"** 입니다. *(학습 시 Vue 2 문서를 보지 않도록 주의!)*

### Vue의 주요 특징
1.  **반응형 데이터 바인딩:** 데이터 변경 시 UI가 자동으로 업데이트됩니다.
2.  **컴포넌트 기반 아키텍처:** 재사용 가능한 UI 조각으로 화면을 구성합니다.
3.  **간결한 문법과 직관적인 API:** 가독성이 높고 학습 곡선이 낮습니다.
4.  **유연한 스케일링:** 작은 토이 프로젝트부터 대규모 애플리케이션까지 모두 적합합니다.

### Vue를 학습하는 이유 (SSAFY 기준 포함)
*   React나 Angular에 비해 **문법이 간결하고 직관적**이라 짧은 시간 내에 효율적으로 결과물을 만들 수 있습니다.
*   잘 정리된 공식 문서와 활성화된 글로벌 커뮤니티 덕분에 풍부한 리소스와 예제를 얻기 쉽습니다.
*   다양한 플러그인과 라이브러리를 제공하여 **확장성**이 매우 높습니다.

---

## 2. Vue의 2가지 핵심 기능

### 1. 선언적 렌더링 (Declarative Rendering)
*   표준 HTML을 확장하는 Vue의 **"템플릿 구문(`{{ }}` 등)"**을 사용합니다.
*   JavaScript 상태(데이터)를 기반으로 화면에 출력될 HTML을 **선언적**으로 작성합니다.
*   *"이 데이터가 여기에 보여야 해"* 라고 선언만 하면 Vue가 알아서 그려줍니다.

### 2. 반응성 (Reactivity)
*   JavaScript **상태(데이터)의 변경을 추적**합니다.
*   데이터에 변경사항이 발생하면 **자동으로 DOM을 업데이트**하여 화면을 바꿉니다.

---

## 3. Vue 코드 체험하기 (Basic Example)

아래는 CDN을 활용하여 Vue 3의 핵심 기능을 구현한 간단한 예시입니다.

```html
<!-- HTML 부분 (View) -->
<div id="app">
  <!-- 1. 선언적 렌더링: message 데이터가 바인딩 됨 -->
  <h1>{{ message }}</h1>
  
  <!-- 2. 이벤트 처리 및 반응성: 클릭 시 count가 증가하고 화면이 자동 갱신됨 -->
  <button v-on:click="count++">
    Count is: {{ count }}
  </button>
</div>

<!-- JavaScript 부분 (Logic) -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script>
  const { createApp, ref } = Vue

  const app = createApp({
    setup() {
      // ref()를 사용하여 '반응형 데이터' 생성
      const message = ref('Hello vue!')
      const count = ref(0)

      // 템플릿(HTML)에서 사용할 데이터를 반환(return)
      return {
        message,
        count
      }
    }
  })

  // id가 'app'인 요소에 Vue 앱을 연결(mount)
  app.mount('#app')
</script>
```

---

## 4. Component (컴포넌트)

### 컴포넌트란?
*   **"재사용 가능한 코드 블록"**입니다.
*   웹 UI를 독립적이고 재사용 가능한 일부분으로 분할하고, 각 부분을 개별적으로 다룰 수 있게 해줍니다.
*   **구조:** 애플리케이션은 자연스럽게 **중첩된 Component의 트리 형태**로 구성됩니다.
    *   예: `<Root>` 컴포넌트 아래에 `<Header>`, `<Main>`, `<Aside>`가 있고, `<Main>` 아래에 여러 개의 `<Article>`이 존재하는 방식.
*   **예시:** Facebook이나 음악 스트리밍 서비스 웹페이지를 볼 때, 좌측 네비게이션 바, 메인 피드, 우측 친구 목록, 개별 게시글 등을 각각 하나의 독립적인 컴포넌트로 분리하여 조립하듯 화면을 구성합니다.

---

## 5. Vue Tutorial: Vue를 사용하는 2가지 방법

1.  **'CDN' 방식:** HTML 내에 스크립트 태그를 삽입하여 사용 (기초 학습에 주로 사용)
2.  **'NPM' 설치 방식:** Node.js 환경에서 패키지를 설치하여 사용 (실제 프로젝트 개발 시 주로 사용)

---

## 6. Vue Application 생성하기 (CDN 방식 기준)

Vue 애플리케이션은 다음의 단계적인 과정을 거쳐 생성되고 화면에 연결됩니다.

### ① CDN 작성
*   HTML 문서 내에 Vue를 사용하기 위한 CDN 스크립트를 작성합니다.
```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

### ② Application instance 할당
*   CDN에서 Vue를 사용하는 경우 전역 `Vue` 객체를 불러오게 됩니다.
*   **구조분해할당** 문법을 사용하여 Vue 객체에서 `createApp` 함수만 추출하여 할당합니다.
```javascript
const { createApp } = Vue
```

### ③ Application instance 생성
*   모든 Vue 애플리케이션은 `createApp` 함수를 통해 새로운 Application instance를 생성하는 것으로 시작합니다.
```javascript
const app = createApp({
  setup() {}
})
```

### ④ Root Component (최상위 컴포넌트)
*   `createApp` 함수에는 **객체(컴포넌트)**가 인자로 전달됩니다.
*   모든 앱에는 다른 하위 컴포넌트들을 포함할 수 있는 **Root(최상위) 컴포넌트**가 반드시 필요합니다. 전달된 객체가 그 역할을 합니다.

### ⑤ setup() 함수
*   컴포넌트 내부에 작성되는 `setup()` 함수는 컴포넌트가 동작하기 전에 미리 준비하는 **"시작점"**이자 **"초기 설정용 함수"**입니다.
*   이 함수 안에서 반응형 데이터를 정의하거나, 화면에 표시할 값을 계산하거나, 각종 로직(함수)을 준비합니다.
*   `setup`에서 설정 후 반환(`return`)한 값들은 이후 템플릿(HTML)이나 컴포넌트의 다른 부분에서 바로 사용할 수 있습니다.

### ⑥ Mounting the App (앱 연결)
*   준비된 Vue Application instance를 실제 **HTML 요소에 탑재(연결)**합니다.
*   `mount()` 메서드를 사용하며 인자로 CSS 선택자를 전달합니다.
*   **주의:** 각 앱 인스턴스에 대해 `mount()`는 **단 한 번만** 호출할 수 있습니다.
```html
<!-- 연결될 대상 HTML 요소 -->
<div id="app"></div>

<script>
  // ... (Vue 인스턴스 생성 코드) ...

  // id가 'app'인 DOM 요소에 Vue 앱을 연결
  app.mount('#app')
</script>
```

---

## 7. 반응형 상태 (Reactive State)

### `ref()` 함수
*   **반응형 상태(데이터)를 선언하는 함수**입니다. (Declaring Reactive State)
*   일반 JavaScript 변수를 Vue가 변화를 감지할 수 있는 **반응형 객체**로 만들어줍니다.
*   컴포넌트 내에서 변하는 값(예: 숫자, 문자열, input 값 등)의 상태를 추적하고 관리하기 위해 사용됩니다.
*   **`ref` === reactive reference** (반응형을 가지는 참조 변수를 만드는 것)

### `ref()` 함수의 특징과 동작 원리
1.  **래핑 (Wrapping):** 인자로 받은 값을 `.value` 속성이 있는 `ref` 객체로 감싸서(래핑하여) 반환합니다.
    *   *인자로는 어떠한 타입(숫자, 문자, 객체 등)도 가능합니다.*
2.  **자동 업데이트:** `ref`로 선언된 변수의 값이 변경되면, 해당 값을 사용하는 템플릿(화면)에서 **자동으로 업데이트(렌더링)** 됩니다.
3.  **접근 방식의 차이:**
    *   **JavaScript (`setup` 내부):** `ref` 객체의 실제 값에 접근하거나 수정하려면 반드시 **`.value`** 속성을 사용해야 합니다.
    *   **템플릿 (HTML):** 템플릿에서 사용할 때는 `.value`를 작성할 필요가 없습니다. Vue가 **자동으로 언래핑(unwrapped)** 하여 실제 값을 출력해 줍니다.

```javascript
const { createApp, ref } = Vue

const app = createApp({
  setup() {
    // 1. 반응형 데이터 선언
    const message = ref('Hello vue!')
    
    // JS 내부에서 접근 시
    console.log(message) // ref 객체 자체 출력
    console.log(message.value) // 실제 값 'Hello vue!' 출력
    
    // 2. 템플릿에서 사용하기 위해 반드시 객체 형태로 반환(return)
    return {
      message
    }
  }
})
```

---

## 8. Vue 기본 구조 및 템플릿 렌더링

### Vue 컴포넌트의 기본 구조
*   `createApp()`에 전달되는 객체가 바로 Vue 컴포넌트입니다.
*   컴포넌트의 상태(데이터)와 로직(함수)은 **`setup()` 함수 내에서 선언**되어야 합니다.
*   템플릿의 참조에 접근하려면 `setup` 함수가 **반드시 객체를 반환(`return`)**해야 합니다. 반환된 객체의 속성들만 템플릿에서 사용할 수 있습니다.

### 템플릿 렌더링 (동적 텍스트)
*   **Mustache syntax (콧수염 구문, `{{ }}`)**: 반환된 메시지 값을 기반으로 동적 텍스트를 렌더링할 때 사용합니다.
*   데이터(변수) 값에 따라 화면의 내용이 실시간으로 바뀝니다.

```html
<!-- HTML 템플릿: .value 없이 변수명만 작성 -->
<div id="app">
  <h1>{{ message }}</h1>
</div>
```

### JavaScript 표현식 사용
*   `{{ }}` 내부의 콘텐츠는 단순한 변수명 식별자에만 국한되지 않습니다.
*   단일 변수뿐만 아니라, **유효한 JavaScript 표현식**을 직접 작성하여 사용할 수 있습니다.

```html
<!-- JavaScript 내장 메서드를 활용한 표현식 예시 -->
<h1>{{ message.split('').reverse().join('') }}</h1>
```

---

## 9. Event Listeners in Vue (이벤트 처리기)

*   **`v-on` 디렉티브**를 사용하여 DOM 이벤트를 수신하고 처리할 수 있습니다.
*   버튼 클릭 등의 이벤트가 발생했을 때, `setup` 함수 내에 정의된 메서드(함수)를 실행하여 **반응형 변수 상태를 업데이트**합니다.

### 이벤트 처리 예시 코드

```html
<!-- HTML 부분 -->
<div id="app">
  <!-- v-on:이벤트이름="실행할 함수명" -->
  <button v-on:click="increment">버튼</button>
  
  <p>{{ number }}</p>
  <p>{{ number }}</p>
</div>
```

```javascript
// JavaScript 부분
const { createApp, ref } = Vue

const app = createApp({
  setup() {
    // 반응형 변수 선언
    const number = ref(0)
    
    // 이벤트를 처리할 함수 선언
    const increment = function () {
      // JS 내부에서 ref 값을 수정하므로 .value 사용 필수!
      number.value++ 
    }
    
    // 변수와 함수 모두 템플릿에서 사용할 수 있도록 반환
    return {
      number,
      increment
    }
  }
})
```