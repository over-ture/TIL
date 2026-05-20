# 객체

---

## 객체 기초 (정의, 구조, 접근)

### Object
    키로 구분된 데이터 집합을 저장하는 자료형

#### 객체 구조

- 중괄호('{}')를 이용해 작성
- 중괄호 안에는 `key: value`쌍으로 구성된 속성(property)를 여러 개 작성 가능
- key는 문자형만 허용
- value는 모든 자료형 허용
  ```js
  const user = {
    name: 'Alice',
    'key with space': true,
    greetine: function () {
        return 'hello'
    }
  }
  ```

**속성 참조**

<br>

- 점('.')표기법 또는 대괄호('[]') 표기법으로 객체 속성에 접근
- key 이름에 띄어쓰기 같은 구분자가 있으면 대괄호 접근만 가능
```js
// 조회
console.log(user.name) // Alice
console.log(user['key with space']) // True

// 추가
user.address = 'korea'
console.log(user) // {name: 'Alice', key with space: true, address: 'korea', greeting: f}

user.name = 'Bella'
console.log(user.name)    // Bella

// 삭제
delete user.name
console.log(user) // {key with space: true, address: 'korea', greeting: f}
```

**in 연산자**

<br>

- 속성이 객체에 존재하는지 여부를 확인
- 객체의 키나 배열이 인덱스 존재 여부를 확인하는 연산자
  ```js
  cosole.log('greeting' in user)    // true
  console.log('country' in user)    // false
  ```
> 객체에서 값의 포함 여부를 확인하려면, "in" 연산자 대신 "hasOwnProperty()" 메서드를 사용하는 것이 올바르다

> 프로토타입 체인을 따라 상속된 속성까지 확인하므로, 의도치 않게 true가 나올 수 있어 주의

<br>

---

## 메서드와 this

### Method

- 객체 속성에 정의된 함수
- object.method() 방식으로 호출, 객체가 '행동'할 수 있게 함

#### Method 기본 문법

- 메서드도 값이 함수인 속성
```js
const myObj2 = {
    numbers: [1, 2, 3],
    myFunc: function () {
        this.numbers.forEach(function (number) {
            console.log(this) // window
        })
    }
}

console.log(myObj2.myFunc())
```
- 메서드와 일반 함수의 차이는?
  - 메서드는 자신이 속한 객체의 다른 속성들에 접근할 수 있음
  -> 이를 위한 방법이 바로 `this`

**this**

- 함수나 메서드를 호출한 객체를 가리키는 키워드
  -> <span style="color:crimson">this</span> 키워드를 사용해 객체에 대한 특정한 작업을 수행할 수 있음

```js
const person = {
    name: 'Alice',
    greeting: function () {
        return `Hello my name is ${this.name}`
    },
}

console.log(person.greeting()) // Hello my name is Alice
```

- **JS에서 this는 함수를 <span style="color:crimson">"호출하는 방법"</span>에 따라 가리키는 대상이 달라짐**

    |호출 방법|대상|
    |:---:|:---:|
    |일반 함수에서의 단순 호출|전역 객체|
    |객체에서의 메서드 호출|메서드를 호출한 객체|

- **단순 호출 this**
  - 가리키는 대상 -> 전역 객체
    ```js
    const myFunc = function () {
        return this
    }

    console.log(myFunc())  // window
    ```

- **메서드 호출 시 this**
  - 가리키는 대상 -> 메서드를 호출한 객체
    ```js
    const myObj = {
        data: 1,
        myFunc: function () {
            return this
        }
    }

    console.log(myObj.myFunc())  // myObj
    ```

- **중첩된 함수에서의 this 문제점**
  - forEach의 인자로 전달된 콜백함수는 일반 함수로 호출되므로, this는 전역 객체를 가리킴
  ```js
  const myObj2 = {
    numbers: [1, 2, 3],
    myFunc: function () {
        this.numbers.forEach(function (number) {
            console.log(this) // window
        })
    }
  }

  console.log(myObj2.myFunc())
  ```

**JS `this` 정리**

- JS의 함수는 호출될 때 this를 암묵적으로 전달 받음
- JS에서 this는 함수가 "호출되는 방식"에 따라 결정되는 현재 객체를 나타냄
- Python의 self와 Java의 this가 선언 시점에 이미 값이 정해지는 것과 달리 JS의 this는 <span style="color:crimson">함수가 호출될 때 동적으로 결정</span>

<br>

- 장점
  - 함수(메서드)를 하나만 만들어 여러 객체가 공유하여 각자 자신의 데이터로 동작하게 할 수 있음
- 단점
  - 이런 유연함이 실수로 이어질 수 있다는 것

> 개발자는 this의 동작 방식을 충분히 이해하고 장점을 취하면서 실수를 피하는 데에 집중해야 한다

> this가 헷갈릴 땐 '누가 점(.)을 찍어 호출했는가?'에 집중. 점 앞의 객체가 this가 된다.

---


# 📚 JavaScript: JSON 및 추가 객체 문법

## 1. JSON (JavaScript Object Notation)
Key-Value 형태로 이루어진 자료 표기법입니다.

### 특징
* JavaScript의 Object와 유사한 구조를 가지지만, JSON은 일정한 형식을 가진 **"문자열(String)"** 입니다.
* JavaScript에서 JSON을 사용하기 위해서는 Object 자료형으로 변경해야 합니다.
* 특정 언어에 종속되지 않는 데이터 형식으로, API 통신 등에서 널리 사용됩니다.

### Object $\Leftrightarrow$ JSON 변환 메서드
* **`JSON.stringify()`**: Object(객체) $\rightarrow$ JSON(문자열) 변환
* **`JSON.parse()`**: JSON(문자열) $\rightarrow$ Object(객체) 변환

```javascript
const jsObject = {
  coffee: 'Americano',
  iceCream: 'Cookie and cream',
}

// 1. Object -> JSON (문자열로 변환)
const objToJson = JSON.stringify(jsObject);
console.log(objToJson); // {"coffee":"Americano","iceCream":"Cookie and cream"}
console.log(typeof objToJson); // string

// 2. JSON -> Object (객체로 변환)
const jsonToObj = JSON.parse(objToJson);
console.log(jsonToObj); // { coffee: 'Americano', iceCream: 'Cookie and cream' }
console.log(typeof jsonToObj); // object
```

---

## 2. 추가 객체 문법

### 2.1 단축 속성 (Shorthand property names)
키 이름과 값으로 쓰이는 변수의 이름이 같은 경우 단축 구문을 사용할 수 있습니다.

```javascript
const name = 'Alice';
const age = 30;

// 기존 방식
const user1 = { name: name, age: age };

// 단축 속성 적용
const user2 = { name, age }; 
```

### 2.2 단축 메서드 (Shorthand method names)
객체 내부에서 메서드 선언 시 `function` 키워드를 생략할 수 있습니다.

```javascript
// 기존 방식
const myObj1 = {
  myFunc: function () {
    return 'Hello';
  }
}

// 단축 메서드 적용
const myObj2 = {
  myFunc() {
    return 'Hello';
  }
}
```

### 2.3 구조 분해 할당 (Destructuring assignment)
배열 또는 객체를 분해하여 속성을 변수에 쉽게 할당할 수 있는 문법입니다.

#### 일반적인 객체 구조 분해
```javascript
const userInfo = {
  firstName: 'Alice',
  userId: 'alice123',
  email: 'alice123@gmail.com'
}

// 기존 방식: const firstName = userInfo.firstName; ...
// 구조 분해 할당 적용
const { firstName } = userInfo;
const { firstName, userId } = userInfo;
const { firstName, userId, email } = userInfo;

console.log(firstName, userId, email); // Alice alice123 alice123@gmail.com
```

#### 함수의 매개변수로 활용
함수 호출 시 객체를 구조 분해하여 매개변수로 바로 전달할 수 있습니다.
```javascript
const person = { name: 'Bob', age: 35, city: 'London' };

function printInfo({ name, age, city }) {
  console.log(`이름: ${name}, 나이: ${age}, 도시: ${city}`);
}

printInfo(person); // 이름: Bob, 나이: 35, 도시: London
```

### 2.4 객체와 전개 구문 (Spread Syntax, `...`)
객체 내부에서 다른 객체를 전개하여 "객체 복사"에 활용할 수 있습니다.
* 💡 **참고 (얕은 복사):** 겉(최상위 속성)만 복사하고, 속(중첩 객체)은 메모리 주소를 공유하는 복사 방식입니다.

```javascript
const obj = { b: 2, c: 3, d: 4 };
const newObj = { a: 1, ...obj, e: 5 };

console.log(newObj); // { a: 1, b: 2, c: 3, d: 4, e: 5 }
```

### 2.5 유용한 객체 메서드
객체의 키나 값들을 배열(리스트) 형태로 쉽게 추출할 수 있습니다.

```javascript
const profile = { name: 'Alice', age: 30 };

// 1. Object.keys(): Key 값들을 배열로 반환
console.log(Object.keys(profile)); // ['name', 'age']

// 2. Object.values(): Value 값들을 배열로 반환
console.log(Object.values(profile)); // ['Alice', 30]

// 3. Object.entries(): [Key, Value] 쌍을 배열로 묶어 반환
console.log(Object.entries(profile)); // [['name', 'Alice'], ['age', 30]]
```

### 2.6 Optional Chaining (`?.`)
속성이 없는 중첩 객체에 접근하려 할 때 에러 발생 없이 안전하게 접근하는 방법입니다.

* 만약 참조 대상이 `null` 또는 `undefined`라면 에러가 발생하는 것 대신 평가를 멈추고 `undefined`를 반환합니다.

```javascript
const user = {
  name: 'Alice',
  greeting: function() { return 'hello'; }
}

// 일반적인 접근 -> 에러 발생
// console.log(user.address.street); // Uncaught TypeError
// console.log(user.nonMethod());    // Uncaught TypeError

// Optional chaining 적용 -> 에러 없이 undefined 반환
console.log(user.address?.street); // undefined
console.log(user.nonMethod?.());   // undefined
```

#### 장점
* 참조가 누락될 가능성이 있는 경우 더 짧고 간단한 표현식 작성이 가능합니다.
* 기존의 `&&` 연산자를 사용한 긴 체이닝을 대체할 수 있습니다.
  * 예: `user.address && user.address.street` $\rightarrow$ `user.address?.street`

#### 주의사항
1. **남용 금지:** 존재하지 않아도 괜찮은 대상(선택적 속성)에만 사용해야 합니다. 
   * 예) `user` 객체는 반드시 있어야 하지만 `address`는 필수가 아닐 때:
     * ❌ Bad: `user?.address?.street` (user가 없는 논리적 오류를 숨길 수 있음)
     * ⭕ Good: `user.address?.street`
2. Optional chaining 앞의 변수는 **반드시 선언**되어 있어야 합니다. (선언되지 않은 변수에 사용 시 `ReferenceError` 발생)

#### Optional Chaining 형태 정리
1. `obj?.prop`: obj가 존재하면 `obj.prop` 반환, 없으면 `undefined`
2. `obj?.[prop]`: obj가 존재하면 `obj[prop]` 반환, 없으면 `undefined`
3. `obj?.method()`: obj가 존재하면 `obj.method()` 호출, 없으면 `undefined`

> 💡 **TIP (단락 평가):** `?.`는 `null`과 `undefined`일 때만 동작합니다. 체인 중간이 nullish인 경우 그 뒤의 코드는 실행되지 않습니다. 이를 '단락 평가'라고 부릅니다.