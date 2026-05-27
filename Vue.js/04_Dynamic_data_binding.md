# Vue 3 동적 데이터 바인딩 (Dynamic Data Binding)

## 🎯 학습 목표
*   `v-bind`를 사용하여 HTML 속성을 동적으로 바인딩하는 방법을 이해한다.
*   객체 및 배열을 활용하여 `class`와 `style` 속성을 동적으로 제어한다.
*   `v-on`을 사용하여 DOM 이벤트를 처리하고 `$event` 객체에 접근한다.
*   이벤트 수식어(`Modifiers`)를 활용하여 기본 이벤트 동작을 제어한다.
*   `v-model`을 사용하여 폼(Form) 입력 요소와 양방향 바인딩을 구현한다.

---

## 1. v-bind (속성 바인딩)

`v-bind`는 하나 이상의 속성 또는 컴포넌트 데이터를 표현식에 동적으로 바인딩하는 디렉티브이다.
HTML 태그의 속성(Attribute)을 Vue의 데이터와 실시간으로 연결해 동적으로 제어하며, 데이터 값에 따라 이미지, 스타일, 클래스 등을 자유롭게 변경할 수 있다.

*   **Shorthand (약어):** `:` (콜론) 기호를 사용하여 생략할 수 있다.

```html
<!-- 기본 문법 -->
<img v-bind:src="imageSrc">
<a v-bind:href="myUrl">Move to url</a>

<!-- 약어 사용 -->
<img :src="imageSrc">
<a :href="myUrl">Move to url</a>
```

### Dynamic attribute name (동적 인자 이름)
대괄호(`[]`)로 감싸서 디렉티브 인자(Argument)에 JavaScript 표현식을 사용할 수 있다. 표현식에 따라 동적으로 평가된 값이 최종 인자 값으로 사용된다.

```html
<button :[key]="myValue"></button>
```
> 💡 **TIP**
> *   대괄호 안에 작성하는 이름은 반드시 **소문자**로만 구성해야 한다. (브라우저가 속성 이름을 소문자로 강제 변환하기 때문)
> *   대괄호 안의 값이 `null`이면 해당 속성이나 이벤트 리스너가 아예 제거된다.
> *   대괄호 안에는 띄어쓰기나 따옴표를 쓸 수 없다.

---

## 2. Class and Style Bindings

`class`와 `style`은 모두 HTML 속성이므로 다른 속성과 마찬가지로 `v-bind`를 사용하여 동적으로 문자열 값을 할당할 수 있다. 하지만 단순히 문자열 연결을 사용하여 값을 생성하는 것은 번거롭고 오류가 발생하기 쉽다.

따라서 Vue는 `class` 및 `style` 속성 값을 `v-bind`로 사용할 때 **객체(Object) 또는 배열(Array)**을 활용하여 작성할 수 있도록 지원한다.

### 2.1 Binding HTML Classes

#### ① Binding to Objects (객체 바인딩)
객체를 `:class`에 전달하여 클래스를 동적으로 전환할 수 있다. 값(Boolean)이 `true`일 때만 해당 클래스가 적용된다.

```html
<!-- isActive가 true이면 active 클래스가 추가됨 -->
<div :class="{ active: isActive }">Text</div>

<!-- 일반 클래스 속성과 혼용 가능. 여러 클래스 조건 부여 가능 -->
<div class="static" :class="{ active: isActive, 'text-primary': hasInfo }">Text</div>
```
```javascript
// 인라인 방식이 아닌, 반응형 변수를 활용해 객체를 한 번에 작성하는 방법 (권장)
const classObj = ref({
  active: true,
  'text-primary': false
})
```
```html
<div class="static" :class="classObj">Text</div>
```

#### ② Binding to Arrays (배열 바인딩)
`:class`를 배열에 바인딩하여 여러 개의 클래스 목록을 한 번에 적용할 수 있다.

```html
<!-- 배열 요소로 클래스 변수 전달 -->
<div :class="[activeClass, infoClass]">Text</div>

<!-- 배열 구문 내에서 객체 구문 혼용 가능 -->
<div :class="[{ active: isActive }, infoClass]">Text</div>
```

### 2.2 Binding Inline Styles

#### ① Binding to Objects (객체 바인딩)
`:style`은 HTML의 `style` 속성에 JavaScript 객체를 바인딩하는 것을 지원한다.
속성명 작성 시 `kebab-cased` 문자열도 지원하지만, 가급적 **`camelCase` 작성을 권장**한다.

```html
<!-- inline 방식 -->
<div :style="{ color: activeColor, fontSize: fontSize + 'px' }">Text</div>

<!-- CSS처럼 kebab-case 사용 시 따옴표 필요 -->
<div :style="{ color: activeColor, 'font-size': fontSize + 'px' }">Text</div>
```
```javascript
// 스타일 객체 바인딩 방식
const styleObj = ref({
  color: 'crimson',
  fontSize: '50px' // fontSize.value + 'px' 형태로도 사용 가능
})
```
```html
<div :style="styleObj">Text</div>
```

#### ② Binding to Arrays (배열 바인딩)
여러 스타일 객체를 배열에 작성해서 `:style`에 바인딩할 수 있다. 작성한 객체는 병합되어 동일한 요소에 적용된다.

```html
<div :style="[styleObj, styleObj2]">Text</div>
```

---

## 3. Event Handling (v-on)

`v-on`은 DOM 요소에 이벤트 리스너를 연결 및 수신하는 디렉티브이다.
버튼 클릭, 키보드 입력 등 사용자의 이벤트를 감지하고, 지정된 코드를 실행시켜 사용자와 웹 페이지가 상호작용할 수 있도록 만든다.

*   **Shorthand (약어):** `@` 기호를 사용하여 생략할 수 있다.
```html
<button v-on:click="handler">버튼</button>
<button @click="handler">버튼</button>
```

### 3.1 Handler의 종류

#### ① Inline handlers
이벤트가 트리거 될 때 실행될 간단한 JavaScript 코드를 템플릿에 직접 작성하는 방식이다. 로직이 복잡해지면 가독성이 떨어지고 재사용이 불가능하므로 주로 아주 간단한 로직에만 사용한다.
```html
<button @click="count++">Add 1</button>
```

#### ② Method handlers (메서드 핸들러)
컴포넌트의 `setup`에 정의된 메서드 이름을 호출하는 방식이다. 
괄호 없이 메서드 이름만 연결하면, 핸들러의 **첫 번째 인자로 DOM의 `event` 객체가 자동으로 전달**된다.
```html
<button @click="myFunc">Hello</button>
```
```javascript
const myFunc = function (event) {
  console.log(event) // PointerEvent 객체 출력
  console.log(event.currentTarget)
}
```

### 3.2 Event 인자 전달 및 접근

**① 사용자 지정 인자 전달**
기본 이벤트 객체 대신 사용자 지정 인자를 전달할 수 있다. 이때 메서드에는 호출 시 작성한 인자만 전달된다.
```html
<button @click="greeting('hello')">Say hello</button>
```

**② Inline Handlers에서 event 인자 접근 (`$event`)**
사용자 지정 인자와 함께 원래의 DOM 이벤트 객체에도 접근해야 할 경우, 특수 변수인 **`$event`**를 사용하여 메서드에 전달할 수 있다. `$event` 변수의 전달 위치는 상관없다.
```html
<!-- 경고문자열과 원래의 event 객체를 함께 전달 -->
<button @click="warning('경고입니다', $event)">Warning</button>
```
```javascript
const warning = function (message, event) {
  console.log(message) // '경고입니다'
  console.log(event)   // PointerEvent 객체
}
```

---

## 4. Modifiers (수식어)

디렉티브 뒤에 점(`.`)으로 붙여, 특별한 동작을 추가하거나 기본 동작을 제어하는 기능이다.
메서드 로직 안에서 `event.preventDefault()` 등을 직접 작성할 필요 없이 순수하게 데이터 관련 처리에만 집중할 수 있게 해 준다.

### 4.1 Event Modifiers (이벤트 수식어)
*   **`.prevent`**: 이벤트의 기본 동작을 취소한다. (`event.preventDefault()`)
    *   *예: `<form>`의 제출 동작 시 페이지 새로고침 방지, `<a>` 태그의 링크 이동 방지*
*   **`.stop`**: 이벤트 버블링(Bubbling)을 중단시킨다. (`event.stopPropagation()`)
    *   *💡 버블링: 한 요소의 이벤트가 부모, 조상 요소로 퍼져나가는 현상*

> ⚠️ **주의사항:** Modifiers는 체이닝(Chained) 되게끔 작성할 수 있으며, 이때는 **작성된 순서대로 실행**되므로 순서에 유의해야 한다.

```html
<!-- submit 기본 동작 취소 후 onSubmit 호출 -->
<form @submit.prevent="onSubmit">...</form>

<!-- a 태그 클릭 시 링크 이동 방지(.prevent) 및 버블링 중단(.stop) -->
<a @click.stop.prevent="onLink" href="https://google.com">...</a>
```

### 4.2 Key Modifiers (키 수식어)
키보드 이벤트를 수신할 때 특정 키에 관한 별도 수식어를 사용할 수 있다.

```html
<!-- Enter 키가 입력 되었을 때만 onSubmit 호출 -->
<input @keyup.enter="onSubmit">

<!-- Ctrl + Enter가 입력 되었을 때만 submitComment 호출 -->
<textarea @keydown.ctrl.enter="submitComment"></textarea>
```

---

## 5. Form Input Bindings (v-model)

`form`을 처리할 때 사용자가 `input`에 입력하는 값을 실시간으로 JavaScript 상태 데이터에 동기화해야 하는 경우 **양방향 바인딩**을 사용한다.

양방향 바인딩은 1) 데이터 변경이 화면에 반영되고, 2) 화면의 사용자 입력이 데이터에 반영되는 것을 의미한다.

### 5.1 양방향 바인딩 방법 2가지

#### ① v-bind와 v-on을 함께 사용
*   `v-bind`로 input 요소의 `value` 속성을 반응형 변수에 연결한다.
*   `v-on`으로 `input` 이벤트가 발생할 때마다 요소의 현재 값을 반응형 변수에 저장한다.
```html
<input :value="inputText1" @input="onInput">
```
```javascript
const inputText1 = ref('')
const onInput = function (event) {
  inputText1.value = event.currentTarget.value
}
```

#### ② v-model 사용 (권장)
`v-model`은 `input`과 같은 폼 요소의 값과 Vue의 데이터를 실시간으로 동기화시키는 디렉티브이다. 내부적으로 `v-bind`와 `v-on`을 조합한 동작을 수행하여 코드를 간결하게 만든다.
```html
<input v-model="inputText2">
```

> 🚨 **주의: IME가 필요한 언어 입력 시 문제점**
> 한국어, 중국어, 일본어 등 IME(입력기)가 필요한 언어의 경우, 글자가 조합되는 중에는 `v-model`이 데이터를 제대로 업데이트하지 못하는 현상이 발생한다. 
> 해당 언어 입력 시 글자 단위로 즉각적인 동기화가 필요하다면 `v-model` 대신 **`v-bind`와 `v-on` 방식을 직접 조합하여 사용**해야 한다.

### 5.2 v-model과 다양한 입력 양식 활용

`v-model`은 단순 Text input뿐만 아니라 Checkbox, Radio, Select 등 다양한 타입의 사용자 입력 방식과 함께 사용할 수 있다.

#### ① Checkbox 활용
단일 체크박스는 `boolean` 값을 활용하고, 여러 개의 체크박스는 배열(Array)을 활용한다.
```html
<!-- 단일 체크박스: checked 값이 true/false로 동기화됨 -->
<input type="checkbox" id="checkbox" v-model="checked">

<!-- 다중 체크박스: 선택된 요소의 value 값들이 checkedNames 배열에 추가/삭제됨 -->
<input type="checkbox" id="alice" value="Alice" v-model="checkedNames">
<input type="checkbox" id="bella" value="Bella" v-model="checkedNames">
```
```javascript
const checked = ref(false)
const checkedNames = ref([]) // 배열로 초기화
```

#### ② Select 활용
`select` 요소의 옵션을 선택하면 해당 `option`의 값이 바인딩된다. 초기 반응형 변수 값이 어떤 `option`과도 일치하지 않는 경우 "선택되지 않은(unselected)" 상태로 렌더링 된다.
```html
<select v-model="selected">
  <!-- 첫 번째 옵션은 안내 문구로 주로 사용하며 disabled 처리함 -->
  <option disabled value="">Please select one</option>
  <option>Alice</option>
  <option>Bella</option>
</select>
```
```javascript
const selected = ref('')
```
