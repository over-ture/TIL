
# [학습 자료] Ajax 복습 및 비동기 팔로우 구현

## 1. Ajax 개념 복습

### 1.1 Ajax란?
* **개념**: **Asynchronous JavaScript and XML** (비동기적인 웹 애플리케이션 개발을 위한 기술)
* **특징**:
  * 웹 페이지 전체를 새로고침(Reload)하지 않고, 백그라운드에서 서버와 데이터를 주고받는 비동기 통신 기술입니다.
  * 페이지의 일부분만 동적으로 바꾸는 것이 가능하므로 사용자 경험(UX)을 크게 향상시킵니다. (예: 구글 지도 탐색, SNS의 '좋아요' 및 '팔로우' 버튼 등)
  * 웹 페이지를 데스크톱 애플리케이션처럼 작동하도록 만들어 주는 현대 웹의 핵심 기술 중 하나입니다.

### 1.2 클라이언트-서버 간 동작 흐름
1. **이벤트 발생**: 웹 페이지에서 사용자 동작(클릭, 서브밋 등) 발생
2. **XHR 객체 생성 및 요청**: JavaScript(예: Axios 라이브러리)를 사용하여 비동기 요청(XHR 객체 생성 및 전송)을 서버로 보냄
3. **서버 처리 및 응답 데이터 생성**: 서버(Django 등)가 요청을 처리하고 결과 데이터를 생성
4. **JSON 데이터 응답**: 서버가 HTML 전체 페이지가 아닌 가벼운 **JSON 데이터** 형태로 응답
5. **DOM 조작**: 클라이언트가 Promise 객체를 활용해 응답 데이터를 수신한 후, 필요한 DOM 요소를 선택하여 화면의 일부분만 갱신

---

## 2. Django 비동기 팔로우 구현 (Ajax 적용)

### 2.1 사전 준비
1. **M:N 관계(다대다) 모델링**이 완료된 Django 프로젝트 준비
2. 가상 환경 생성 및 활성화, 패키지 설치 완료

---

### 2.2 클라이언트 사이드 구현 (HTML & JavaScript)

#### ① Axios CDN 추가
프로필 페이지 파일 하단(`</body>` 태그 직전)에 Axios 라이브러리를 로드하기 위한 CDN 스크립트를 작성합니다.

```html
<!-- accounts/profile.html -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
  // 이후 JavaScript 코드는 이곳에 작성합니다.
</script>
```

#### ② HTML Form 수정 및 요소 선택
* 비동기 통신은 JavaScript(Axios)가 대신 요청을 보낼 것이므로, 기존 `<form>` 태그의 `action`과 `method` 속성은 삭제합니다.
* JavaScript에서 요소를 쉽게 선택할 수 있도록 `id` 속성을 부여합니다.

```html
<!-- accounts/profile.html -->
<form id="follow-form" data-user-id="{{ person.pk }}">
  {% csrf_token %}
  {% if request.user in person.followers.all %}
    <input type="submit" value="Unfollow">
  {% else %}
    <input type="submit" value="Follow">
  {% endif %}
</form>
```

```javascript
// JavaScript에서 Form 요소 선택
const formTag = document.querySelector('#follow-form')
```

#### ③ 기본 이벤트 방지 (`preventDefault`)
Form이 제출(submit)될 때 브라우저가 페이지 전체를 새로고침하는 기본 동작을 차단합니다.

```javascript
formTag.addEventListener('submit', function (event) {
  // HTML의 기본 submit 동작(새로고침) 취소
  event.preventDefault()
  
  // 이후 비동기 요청(Axios) 로직 작성
})
```

#### ④ HTML에서 JS로 데이터 전달 (`data-*` 속성 사용)
요청 URL을 동적으로 구성하기 위해서는 팔로우 대상 사용자의 `PK` 값이 필요합니다. 이를 HTML에서 JavaScript로 안전하게 전달하기 위해 사용자 지정 데이터 속성(`data-*`)을 활용합니다.

##### `data-*` 속성 규칙
* HTML에서 `data-user-id`와 같이 케밥 케이스(kebab-case)로 작성하면, JavaScript에서는 `dataset.userId`와 같이 카멜 케이스(camelCase)로 변환되어 접근할 수 있습니다.
* 주의사항: 대소문자 여부와 관계없이 'xml' 문자로 시작할 수 없으며, 세미콜론이나 대문자를 포함할 수 없습니다.

```javascript
// 이벤트 핸들러 내부에서 user_id 가져오기 (세 가지 방법 중 선택 가능)
const userId = event.currentTarget.dataset.userId
// const userId = this.dataset.userId
// const userId = formTag.dataset.userId
```

#### ⑤ CSRF 토큰 처리
Django는 보안상의 이유로 POST 요청 시 CSRF 토큰 검증을 수행합니다. 비동기 POST 요청을 보낼 때도 반드시 헤더에 CSRF 토큰 정보를 담아 전송해야 합니다.

* HTML 내부에 생성되어 있는 CSRF 토큰 입력 요소(`<input type="hidden" name="csrfmiddlewaretoken" ...>`)의 값을 가져옵니다.
* Axios 요청의 `headers` 옵션에 `X-CSRFToken` 키로 전달합니다.

```javascript
// CSRF 토큰 값 가져오기
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
```

---

### 2.3 서버 사이드 구현 (Django View)

기존에는 팔로우 처리 후 전체 페이지를 다시 그리기 위해 다른 URL로 리다이렉트(`redirect`)시켰지만, 비동기 통신을 위해 상태 정보를 포함한 **JSON 데이터**를 반환하도록 변경합니다.

```python
# accounts/views.py
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    
    if person != request.user:
        # 이미 팔로우한 상태이면 팔로우 취소
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        # 팔로우하지 않은 상태이면 팔로우 등록
        else:
            person.followers.add(request.user)
            is_followed = True
        
        # 클라이언트에 응답할 데이터를 딕셔너리로 정의
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        # JsonResponse를 사용해 JSON 형태로 데이터 반환
        return JsonResponse(context)
        
    return redirect('accounts:profile', person.username)
```

---

### 2.4 클라이언트 사이드 응답 처리 및 DOM 조작

#### ① Axios 요청 및 응답 데이터 확인
Axios를 활용해 Django 서버로 비동기 요청을 발송하고, 반환되는 Promise 객체의 `.then()` 메서드를 이용하여 서버의 응답 데이터를 처리합니다.

```javascript
axios({
  method: 'post',
  url: `/accounts/${userId}/follow/`,
  headers: {'X-CSRFToken': csrftoken},
})
.then((response) => {
  console.log(response)       // Axios의 전체 응답 데이터 객체
  console.log(response.data)  // Django 뷰에서 보낸 context 데이터 ({'is_followed': ...})
})
```

#### ② 버튼 텍스트 변경 (DOM 조작)
서버에서 응답받은 `is_followed` 값에 따라 제출 버튼의 값을 `'Follow'` 또는 `'Unfollow'`로 조작합니다.

```javascript
.then((response) => {
  const isFollowed = response.data.is_followed
  const followBtn = document.querySelector('input[type=submit]')

  if (isFollowed === true) {
    followBtn.value = 'Unfollow'
  } else {
    followBtn.value = 'Follow'
  }
})
```

#### ③ 팔로잉/팔로워 수 동적 변경
화면상에 팔로잉 및 팔로워 인원 수 값을 나타내는 영역을 각각 `<span>` 태그로 감싸고, JavaScript에서 선택할 수 있도록 `id` 속성을 추가합니다.

##### HTML 구조 수정
```html
<!-- accounts/profile.html -->
<div>
  팔로잉 : <span id="followings-count">{{ person.followings.all|length }}</span> / 
  팔로워 : <span id="followers-count">{{ person.followers.all|length }}</span>
</div>
```

##### JavaScript DOM 갱신 로직 추가
```javascript
.then((response) => {
  // ... 생략 (버튼 토글 로직) ...

  // 1. DOM 요소 선택
  const followingsCountTag = document.querySelector('#followings-count')
  const followersCountTag = document.querySelector('#followers-count')

  // 2. 서버로부터 전달받은 최신 데이터로 변경
  followingsCountTag.textContent = response.data.followings_count
  followersCountTag.textContent = response.data.followers_count
})
```

---

### 2.5 동작 확인 방법 (디버깅)
* 브라우저 개발자 도구(F12)의 **Network** 탭을 엽니다.
* 팔로우 버튼을 눌렀을 때, 새로운 페이지 이동 없이 요청(`follow/`)이 기록되는지 확인합니다.
* 해당 요청 항목의 **Type**이 `xhr`인지 확인하고, **Response**의 **Content-Type** 헤더 값이 `application/json`으로 표시되는지 체크합니다.