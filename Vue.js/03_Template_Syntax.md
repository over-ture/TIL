# Vue 3 템플릿 문법과 디렉티브 (Template Syntax & Directives)

## 🎯 학습 목표 (Objectives)
*   `v-` 접두사를 가진 디렉티브의 개념과 역할을 이해한다.
*   `v-bind` 디렉티브를 사용해 HTML 속성을 동적으로 바인딩한다.
*   객체나 배열을 이용해 `class`와 `style`을 동적으로 바인딩한다.
*   `v-on` 디렉티브로 DOM 이벤트를 수신하고 메서드를 실행한다.
*   `.prevent`와 같은 이벤트 수식어로 이벤트 동작을 제어한다.
*   `v-model` 디렉티브로 폼 요소에 양방향 바인딩을 한다.
*   `v-model`이 `v-bind`와 `v-on`의 조합임을 이해한다.

---

## 1. Template Syntax (템플릿 문법)

### 템플릿 문법이란?
Vue는 DOM(화면)을 컴포넌트 인스턴스의 데이터에 **선언적으로 바인딩**할 수 있는 HTML 기반 템플릿 구문을 사용합니다.
*   **선언적 바인딩:** JavaScript 데이터(상태)가 바뀌면 DOM이 알아서 업데이트되는 것을 의미합니다.
*   쉽게 말해, 기존 HTML에 Vue만의 특별한 문법을 추가하여 JavaScript 데이터와 HTML 화면을 아주 쉽고 직관적으로 연결하는 방법입니다.

### 템플릿 문법의 4가지 종류

#### ① Text Interpolation (텍스트 보간법)
*   데이터 바인딩의 가장 기본적인 형태입니다.
*   **이중 중괄호 구문 (콧수염 구문, `{{ }}`)**을 사용합니다.
*   작성된 콧수염 구문은 해당 컴포넌트 인스턴스의 데이터(속성 값)로 대체되며, 데이터가 변경될 때마다 화면도 실시간으로 업데이트됩니다.
```html
<p>Message: {{ msg }}</p>
```

#### ② Raw HTML (원시 HTML)
*   콧수염 구문(`{{ }}`)은 데이터를 일반 텍스트로만 해석합니다.
*   데이터에 포함된 실제 HTML 태그를 렌더링하려면 **`v-html`** 속성을 사용해야 합니다.
```html
<!-- 데이터: const rawHtml = ref('<span style="color:red">This should be red.</span>') -->

<!-- 텍스트로 출력됨: <span style="color:red">...</span> -->
<div>{{ rawHtml }}</div>

<!-- 실제 빨간색 글씨로 렌더링 됨 -->
<div v-html="rawHtml"></div>
```

#### ③ Attribute Bindings (속성 바인딩)
*   콧수염 구문은 HTML 태그의 '속성(Attribute)' 내부에서는 사용할 수 없습니다.
*   HTML 태그의 속성(id, class, src, href 등) 값을 Vue의 데이터와 동기화하려면 **`v-bind`** 디렉티브를 사용합니다.
*   만약 바인딩 값이 `null`이나 `undefined`인 경우, 해당 속성은 렌더링 되는 HTML 요소에서 완전히 제거됩니다.
```html
<!-- id 속성 값을 dynamicId 변수 값과 연결 -->
<div v-bind:id="dynamicId"></div>
```

#### ④ JavaScript Expressions (자바스크립트 표현식)
*   Vue는 모든 데이터 바인딩 내에서 JavaScript 표현식의 모든 기능을 지원합니다.
*   **사용 가능 위치:** 콧수염 구문 내부, 모든 디렉티브의 속성 값 (`v-`로 시작하는 특수 속성)
```html
{{ number + 1 }}
{{ ok ? 'YES' : 'NO' }}
{{ message.split('').reverse().join('') }}

<div v-bind:id="`list-${id}`"></div>
```

> ⚠️ **표현식 사용 시 주의사항**
> 각 바인딩에는 **하나의 단일 표현식**만 포함될 수 있습니다. (표현식: 하나의 값으로 평가/계산될 수 있는 코드 조각)
> 
> *작동하지 않는 경우 (에러 발생):*
> ```html
> <!-- 표현식이 아닌 '선언문'입니다. -->
> {{ const number = 1 }}
> 
> <!-- '제어문'은 사용할 수 없습니다. 삼항 연산자를 사용해야 합니다. -->
> {{ if (ok) { return message } }}
> ```

---

## 2. Directive (디렉티브)

### 디렉티브란?
*   **`v-` 접두사**가 있는 특수 속성입니다.
*   DOM 요소에 특정 반응형 동작을 적용하는 명령어 역할을 합니다.
*   JavaScript 로직을 HTML 템플릿 안에서 선언적으로 사용하여, 코드를 깔끔하고 직관적으로 유지하게 돕는 강력한 도구입니다.

> **💡 간단 퀴즈 (접두사 `v-`의 의미)**
> 1. HTML 태그 속성 값을 Vue 데이터와 동적 연결 👉 `v-bind`
> 2. 버튼 클릭 등 사용자 이벤트를 감지하여 함수 실행 👉 `v-on`
> 3. `<input>` 등 폼 요소의 값과 데이터를 실시간 양방향 동기화 👉 `v-model`

### 디렉티브의 특징
*   디렉티브의 속성 값은 **단일 JavaScript 표현식**이어야 합니다. (`v-for`, `v-on` 등 일부 예외 존재)
*   표현식 값이 변경될 때 DOM에 반응적으로 업데이트를 적용합니다.
*   **TIP:** 디렉티브 안에는 문자열 리터럴을 값으로 주려면 `"'문자열'"` 처럼 따옴표로 한 번 더 감싸야 합니다.
```html
<!-- seen 변수가 true일 때만 화면에 렌더링 됨 -->
<p v-if="seen">Hi There</p>
```

---

## 3. Directive 전체 구문 구조 (Anatomy)

디렉티브는 보통 다음과 같은 구조로 작성됩니다.
`v-Name:Argument.Modifiers="Value"` 

예시: `v-on:submit.prevent="onSubmit"`

#### ① Name (이름)
*   디렉티브의 핵심 이름으로, 어떤 종류의 기능을 수행할지를 의미합니다. (`v-`로 시작)
*   단축 문법(shorthand)을 사용할 때는 `v-`를 생략할 수 있습니다. (예: `@`, `:`)

#### ② Argument (전달 인자)
*   일부 디렉티브는 디렉티브 이름 뒤에 **콜론(`:`)**으로 표시되는 인자를 사용할 수 있습니다.
*   디렉티브가 '무엇에 대해' 동작할지 알려주는 구체적인 대상입니다.
```html
<!-- v-bind의 인자: href 속성에 바인딩 하겠다 -->
<a v-bind:href="myUrl">Link</a>

<!-- v-on의 인자: click 이벤트를 수신하겠다 -->
<button v-on:click="doSomething">Button</button>
```

#### ③ Modifiers (수식어)
*   **점(`.`)**으로 표시되는 특수한 접미사입니다.
*   디렉티브가 특별한 방식으로 바인딩되거나, 기본 동작을 수정해야 함을 나타냅니다.
*   **TIP:** 여러 수식어를 체이닝(이어서 붙이기) 할 수 있습니다. (예: `@click.stop.prevent`)
```html
<!-- .prevent 수식어: 이벤트 발생 시 event.preventDefault()를 자동으로 호출함 -->
<form v-on:submit.prevent="onSubmit">
  <input type="submit">
</form>
```

#### ④ Value (값)
*   디렉티브에 연결될 **JavaScript 표현식**입니다. (따옴표 `""` 안의 내용)

