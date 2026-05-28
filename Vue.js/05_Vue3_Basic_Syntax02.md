## 1. Computed Properties (계산된 속성)

### `computed()` 란?
- "계산된 속성"을 정의하는 함수이다.
- 미리 계산된 속성을 만들어 템플릿의 표현식을 단순하게 하고, 불필요한 반복 연산을 줄여준다.
- 반응형 데이터를 포함하는 복잡한 로직의 경우 `computed`를 활용하여 값을 미리 계산하여 사용한다.

### `computed` 특징
- 반환되는 값은 계산된 `ref` (computed ref)이며, 일반 `ref`와 유사하게 `.value`로 참조 가능하다. (템플릿에서는 `.value` 생략 가능)
- 의존된 반응형 데이터를 **자동으로 추적**한다.
- **의존하는 반응형 데이터가 변경될 때만 재평가**된다.

### 💡 Computed vs Methods
`computed` 속성 대신 `method`로도 동일한 기능을 정의할 수 있으나, 가장 큰 차이점은 **캐싱(Caching)** 여부이다.

*   **computed**
    *   의존하는 반응형 데이터를 기반으로 그 결과를 **캐시(cached)** 한다.
    *   의존 데이터가 변경되지 않는 한, 여러 번 접근해도 함수를 다시 실행하지 않고 캐시된 결과를 즉시 반환한다.
    *   **사용처:** 의존하는 데이터에 따라 결과가 바뀌는 계산된 속성을 만들 때, 여러 곳에서 재사용하여 중복 연산을 방지할 때 유용하다.
*   **method**
    *   다시 렌더링이 발생할 때마다 **항상 함수를 실행**한다.
    *   **사용처:** 단순히 특정 동작을 수행하거나, 데이터 의존성과 관계없이 항상 동일한 결과를 반환해야 할 때, 혹은 계산에 외부의 인자값이 필요할 때 사용한다.

> **TIP:** 템플릿에서 호출 시 `computed`는 괄호 없이(`{{ restOfTodos }}`), `method`는 괄호를 붙여(`{{ getRestOfTodos() }}`) 호출한다.

---

## 2. Conditional Rendering (조건부 렌더링)

### `v-if`, `v-else-if`, `v-else`
- 표현식 값의 `true`/`false`를 기반으로 요소를 조건부로 렌더링하는 Directive이다.
- 조건이 `true`일 때만 HTML 요소를 화면에 보여주며, `false`일 경우 해당 요소는 DOM(문서 구조)에서 완전히 제거된다.

```html
<p v-if="isSeen">true일때 보여요</p>
<p v-else>false일때 보여요</p>
```

```html
<div v-if="name === 'Alice'">Alice입니다</div>
<div v-else-if="name === 'Bella'">Bella입니다</div>
<div v-else>아무도 아닙니다.</div>
```

### 여러 요소에 대한 `v-if` 적용 (`<template>`)
- `<template>` 요소에 `v-if`를 사용하면, 눈에 보이는 래퍼(wrapper) 요소(ex. `<div>`)를 추가하지 않고도 여러 요소를 하나의 조건부 블록으로 묶을 수 있다.

```html
<template v-if="name === 'Cathy'">
  <div>Cathy입니다</div>
  <div>나이는 30살입니다</div>
</template>
```

### 💡 `v-if` vs `v-show`
*   **`v-show`**: `v-if`와 비슷하게 작동하지만, 요소가 항상 DOM에 렌더링되어 남아있다. 오직 CSS의 `display` 속성만 토글(`none`)하여 화면에서 숨긴다.
*   **적절한 사용처 비교**
    *   `v-if` (Cheap initial load, expensive toggle): 초기 조건이 false면 렌더링하지 않아 초기 비용이 낮지만, 토글 비용이 높다. **실행 중에 조건이 잘 변경되지 않는 경우** 권장한다.
    *   `v-show` (Expensive initial load, cheap toggle): 조건에 관계없이 무조건 렌더링하므로 초기 렌더링 비용이 높지만, 토글 비용이 낮다. **콘텐츠를 매우 자주 전환해야 하는 경우** 권장한다.

---

## 3. List Rendering (리스트 렌더링)

### `v-for`
- 배열(Array), 객체(Object), 숫자, 문자열 등의 소스 데이터를 기반으로 요소 또는 템플릿 블록을 반복 렌더링하는 Directive이다.
- `alias in expression` 형식의 구문을 사용한다.

**1. 배열 반복**
```html
<div v-for="(item, index) in myArr">
  {{ index }} / {{ item.name }}
</div>
```

**2. 객체 반복**
객체는 순회 시 값(value), 키(key), 인덱스(index)를 제공한다.
```html
<div v-for="(value, key, index) in myObj">
  {{ index }} / {{ key }} / {{ value }}
</div>
```

**3. 여러 요소 반복 (`<template>`)**
`v-if`와 마찬가지로 `<template>` 태그를 활용하여 묶음 단위로 반복 렌더링이 가능하다.

**4. 중첩된 `v-for`**
상위 영역의 데이터에 하위 `v-for`가 접근할 수 있다.

---

## 4. `v-for` with `key`

- `v-for` 구문은 각 요소를 `key` 속성을 활용하여 고유한 값으로 식별해야 한다.
- Vue의 내부 가상 DOM 알고리즘이 노드를 비교하고 추적할 때 올바른 항목만 효율적으로 업데이트하기 위한 힌트로 사용된다.
- **반드시 `v-for`와 `key`를 함께 사용해야 한다.**
- `key` 값은 **number 혹은 string**으로만 사용해야 한다.

```html
<div v-for="item in items" :key="item.id">
  {{ item.name }}
</div>
```

*   **권장하는 key 값:** 데이터베이스의 고유 ID, 항목의 고유 식별자(UUID 등)
*   **피해야 할 key 값:** 배열의 인덱스(index) - 항목의 순서가 변경되면 인덱스도 변경되어 버그를 유발할 수 있다. 객체 자체를 키로 사용하는 것도 지양해야 한다.

---

## 5. `v-for`와 `v-if`의 혼용 주의사항

> 🚨 **주의:** 동일한 요소에 `v-for`와 `v-if`를 함께 사용하면 안 된다!

- **이유:** Vue 3에서는 동일한 요소에서 **`v-if`가 `v-for`보다 우선순위가 더 높기 때문**이다.
- `v-if` 조건문이 먼저 평가되므로, `v-for` 범위에 있는 변수(alias)에 `v-if`에서 접근할 수 없어 에러(`undefined`)가 발생한다.

**❌ 잘못된 예시**
```html
<!-- v-if가 먼저 실행되어 todo라는 변수를 찾지 못함 -->
<li v-for="todo in todos" v-if="!todo.isComplete" :key="todo.id">
  {{ todo.name }}
</li>
```

### ✅ 해결 방법 2가지

**1. `computed` 활용 (권장)**
목록을 필터링하는 로직을 `computed`로 분리하여 미리 계산된 배열을 반환받아 반복한다.
```javascript
// Script
const completeTodos = computed(() => {
  return todos.value.filter((todo) => !todo.isComplete)
})
```
```html
<!-- Template -->
<ul>
  <li v-for="todo in completeTodos" :key="todo.id">
    {{ todo.name }}
  </li>
</ul>
```

**2. `<template>` 요소 활용**
`v-for`와 `v-if`의 위치를 분리한다. `<template>`으로 먼저 반복을 돌고, 내부의 실제 요소에서 조건을 검사한다.
```html
<ul>
  <template v-for="todo in todos" :key="todo.id">
    <li v-if="!todo.isComplete">
      {{ todo.name }}
    </li>
  </template>
</ul>
```


---

## 6. Watchers (감시자)

### `watch()` 란?
- 하나 이상의 반응형 데이터를 감시하고, **감시하는 데이터가 변경되면 특정 콜백 함수를 호출**하는 기능이다.
- 새로운 값을 계산하여 반환하는 `computed`와 달리, `watch`는 데이터가 바뀔 때 **특정 행동(Side Effect - 예: DOM 변경, 비동기 통신 등)을 수행**하기 위해 사용된다.

### `watch` 구조
`watch` 함수는 크게 두 개의 인자를 받는다.

1.  **첫 번째 인자 (source)**
    *   `watch`가 감시하는 대상이다. (반응형 변수, 값을 반환하는 함수 등)
2.  **두 번째 인자 (callback function)**
    *   `source`가 변경될 때 호출되는 콜백 함수이다.
    *   `newValue`: 감시하는 대상이 변화된 새로운 값
    *   `oldValue` (optional): 감시하는 대상의 기존(변화 전) 값

```javascript
watch(source, (newValue, oldValue) => {
  // 데이터가 변경되었을 때 실행할 로직 (Side Effect)
})
```

### `watch` 기본 동작 및 예시
- `count` 값이 변경될 때마다 그 변화를 감지하여 콘솔에 새 값과 이전 값을 출력한다.
```javascript
const count = ref(0)
watch(count, (newValue, oldValue) => {
  console.log(`newValue: ${newValue}, oldValue: ${oldValue}`)
})
```

- 감시하는 변수에 변화가 생겼을 때 연관된 다른 데이터를 업데이트하는 데 활용할 수 있다.
```javascript
const message = ref('')
const messageLength = ref(0)

watch(message, (newValue) => {
  messageLength.value = newValue.length
})
```

### 여러 source를 감시하는 `watch`
- 배열을 활용하여 한 번에 여러 대상을 감시할 수 있다.
- **TIP:** 여러 소스를 감시할 때, 콜백의 인자(새 값, 이전 값)도 같은 순서의 '배열'로 전달된다.
- **TIP:** 배열 속 `ref` 객체의 내부 깊은 곳의 속성 변경까지 감시하려면 `{ deep: true }` 옵션을 추가로 설정해야 한다.

```javascript
watch([foo, bar], ([newFoo, newBar], [prevFoo, prevBar]) => {
  /* ... */
})
```

---

## 7. `computed` vs `watch`

두 기능 모두 데이터의 변화를 감지하고 처리하지만, 목적과 동작 방식에 차이가 있다.

| 구분 | Computed | Watchers |
| :--- | :--- | :--- |
| **공통점** | <td colspan="2" style="text-align:center">데이터의 변화를 감지하고 처리</td> |
| **동작** | 의존하는 데이터 속성의 **계산된 값을 반환** | 특정 데이터 속성의 변화를 감시하고 **작업을 수행 (side-effects)** |
| **사용 목적** | 계산한 값을 캐싱하여 재사용 (중복 계산 방지) | 데이터 변화에 따른 특정 작업을 수행 |
| **사용 예시** | 연산 된 길이, 필터링 된 목록 계산 등 | DOM 변경, 다른 비동기 작업 수행, 외부 API와 연동 등 |

> 🚨 **주의:** `computed`와 `watch` 모두 의존(감시)하는 원본 데이터를 직접 변경해서는 안 된다.

---

## 8. Lifecycle Hooks (생애 주기 훅)

### Lifecycle Hooks 란?
- Vue 컴포넌트가 **생성되고, DOM에 마운트되고, 업데이트되고, 소멸되는 각 생애 주기 단계에서 실행되도록 제공되는 함수**이다.
- 개발자는 컴포넌트의 특정 시점에 원하는 로직을 실행할 수 있다.
- 생성 단계 / 마운트 단계 / 업데이트 단계 / 소멸 단계 등 다양한 단계가 존재한다.
- 가장 일반적으로 사용되는 것은 `onMounted`, `onUpdated`, `onUnmounted` 이다.

### 주요 Lifecycle Hooks

**1. Mounting (`onMounted`)**
- Vue 컴포넌트 인스턴스가 **초기 렌더링 및 DOM 요소 생성이 완료된 후** 특정 로직을 수행한다.
```javascript
import { onMounted } from 'vue'

setup() {
  onMounted(() => {
    console.log('mounted') // 컴포넌트가 화면에 나타난 직후 실행됨
  })
}
```

**2. Updated (`onUpdated`)**
- 반응형 데이터의 변경으로 인해 **컴포넌트의 DOM이 업데이트된 후** 특정 로직을 수행한다.
```javascript
import { onUpdated } from 'vue'

const message = ref(null)

onUpdated(() => {
  message.value = 'updated!' // DOM 변화가 일어난 후 실행됨
})
```

### Lifecycle Hooks 활용 예시 (API 연동)
- 컴포넌트가 마운트되는 시점(`onMounted`)에 외부 API에 요청을 보내어 애플리케이션에 필요한 초기 데이터를 가져올 수 있다.

**예시: Cat API를 활용한 초기 렌더링**
```javascript
const API_URL = 'https://api.thecatapi.com/v1/images/search'
const app = createApp({
  setup() {
    const imgUrl = ref(null)

    const getCatImage = function () {
      axios({
        method: 'get',
        url: API_URL,
      })
        .then((response) => {
          imgUrl.value = response.data[0].url
        })
        .catch((error) => {
          console.log('실패했다옹', error)
        })
    }

    // 컴포넌트가 마운트 된 직후(초기 렌더링 후) API 요청을 보냄
    onMounted(() => {
      getCatImage()
    })

    return { imgUrl, getCatImage }
  }
})
```
```html
<!-- 데이터 흐름 처리를 위한 v-if 활용 -->
<!-- imgUrl 값이 존재할 때만 <img> 태그가 렌더링되도록 처리 -->
<div v-if="imgUrl">
  <img :src="imgUrl" alt="랜덤 고양이 이미지">
</div>
```

---

## 9. Computed 속성 사용 시 주의사항

### 1. `computed`의 반환 값은 변경하지 말 것
- `computed`의 반환 값은 의존하는 데이터로부터 파생된 값(계산이 완료된 값)이다.
- 일종의 **스냅샷(snapshot)** 이며, 의존하는 데이터가 변경될 때만 새로운 스냅샷이 생성된다.
- 따라서 계산된 값은 **읽기 전용(Read-only)** 으로 취급되어야 하며 직접 변경해서는 안 된다.
- 대신 새로운 값을 얻기 위해서는 의존하는 **원본 데이터를 업데이트**해야 한다.

> **TIP:** `computed` 값에 직접 값을 할당하려고 하면, 기본적으로 경고가 발생하며 값이 변경되지 않는다.

### 2. `computed` 사용 시 원본 배열을 변경하지 말 것
- `computed` 내부에서 `reverse()`나 `sort()`처럼 원본 배열 자체를 변경(mutate)하는 메서드를 사용할 때는 주의가 필요하다.
- **반드시 원본 배열의 복사본을 만들어 처리해야 한다.**

**❌ 옳지 않은 예 (원본 배열 변경)**
```javascript
return numbers.reverse()
```

**✅ 옳은 예 (스프레드 문법을 활용한 복사본 생성)**
```javascript
return [...numbers].reverse()
```

---

## 10. Lifecycle Hooks 사용 시 주의사항

### Lifecycle Hooks는 반드시 "동기적"으로 작성해야 한다
- Vue는 컴포넌트가 초기화될 때 모든 훅(Hooks)을 한 번에 스캔하고 준비한다.
- 만약 **비동기로(예: `setTimeout` 내부에서) 훅을 등록**하려고 하면, Vue는 해당 훅을 인식하지 못한다.
- 비동기 처리 완료 후 훅을 설정하려고 할 때는 이미 해당 라이프사이클 단계가 지나간 후일 수 있으므로 **원래 의도한 타이밍에 코드가 실행되지 않는다.**

**❌ 비동기적으로 작성한 lifecycle hook 예시 (실행되지 않음)**
```javascript
setTimeout(() => {
  onMounted(() => {
    console.log('이 코드는 실행되지 않습니다!')
  })
}, 100)
```
- **결론:** Lifecycle Hooks는 컴포넌트 로딩 과정에서 동기적으로 정의함으로써, Vue가 올바른 타이밍에 해당 로직을 수행할 수 있도록 보장해야 한다.

---

## 11. `v-for`와 배열을 활용한 "필터링 / 정렬"

원본 데이터를 수정하거나 교체하지 않고, 조건에 맞게 필터링하거나 정렬된 새로운 데이터를 화면에 표시하는 방법이다.

### 1. `computed` 활용 (권장)
- 원본 배열을 기반으로 필터링 된 새로운 결과를 생성하여 반환한다.
```javascript
const numbers = ref([1, 2, 3, 4, 5])

// 짝수만 필터링하는 computed 속성
const evenNumbers = computed(() => {
  return numbers.value.filter((number) => number % 2 === 0)
})
```
```html
<ul>
  <li v-for="number in evenNumbers">
    {{ number }}
  </li>
</ul>
```

### 2. `method` 활용
- `computed` 사용이 불가능한 **중첩된 `v-for`** 구문이나, 계산에 **매개변수(인자)가 필요한 경우**에 사용한다.
```javascript
const numberSets = ref([
  [1, 2, 3, 4, 5],
  [6, 7, 8, 9, 10]
])

// 배열을 인자로 받아 짝수만 필터링하여 반환하는 함수
const evenNumbers = function (numbers) {
  return numbers.filter((number) => number % 2 === 0)
}
```
```html
<ul v-for="numbers in numberSets">
  <!-- 상위 v-for에서 나온 배열(numbers)을 함수의 인자로 전달 -->
  <li v-for="num in evenNumbers(numbers)">
    {{ num }}
  </li>
</ul>
```

---

## 12. 배열 변경 관련 메서드 주의사항

`v-for`와 배열을 함께 사용할 때, 호출하는 배열 메서드가 원본을 변경하는지 여부를 인지하고 주의해서 사용해야 한다.

1.  **변화 메서드 (Mutation Methods)**
    *   호출하는 **원본 배열 자체를 변경**한다.
    *   종류: `push()`, `pop()`, `shift()`, `unshift()`, `splice()`, `sort()`, `reverse()`
2.  **배열 교체 메서드 (Non-mutating Methods)**
    *   원본 배열을 수정하지 않고, **항상 새로운 배열을 반환**한다.
    *   종류: `filter()`, `concat()`, `slice()`

---

## 13. 종합 실습: Todo 애플리케이션 구현

지금까지 배운 `v-model`(양방향 바인딩), `v-on`(이벤트 핸들링), `v-bind`(속성 바인딩), `v-for`(리스트 렌더링)를 모두 활용하여 간단한 Todo 리스트를 구현한 예시이다.

**1. Script (로직 구현)**
```javascript
import { ref } from 'vue'

let id = 0 // 고유 식별자(key)를 위한 변수

const newTodo = ref(null)
const todos = ref([
  { id: id++, text: 'Learn HTML' },
  { id: id++, text: 'Learn JS' },
  { id: id++, text: 'Learn Vue' }
])

// 새로운 Todo 항목을 추가하는 함수
const addTodo = function () {
  // todos 배열에 새로운 Todo 객체 추가
  todos.value.push({ id: id++, text: newTodo.value })
  // 입력 필드 초기화
  newTodo.value = null
}

// 선택한 Todo 항목을 삭제하는 함수
const removeTodo = function (selectedTodo) {
  // filter를 사용하여 선택한 Todo를 제외한 새로운 배열을 생성하여 덮어씌움
  todos.value = todos.value.filter((todo) => todo !== selectedTodo)
}
```

**2. Template (화면 렌더링)**
```html
<!-- submit 이벤트의 기본 동작(새로고침)을 막고 addTodo 함수 실행 -->
<form @submit.prevent="addTodo">
  <input v-model="newTodo">
  <button>Add Todo</button>
</form>

<ul>
  <!-- 배열 순회 및 고유 식별자 key 바인딩 -->
  <li v-for="todo in todos" :key="todo.id">
    {{ todo.text }}
    <!-- 클릭 시 현재 순회 중인 todo 객체를 인자로 전달하여 삭제 -->
    <button @click="removeTodo(todo)">X</button>
  </li>
</ul>
```