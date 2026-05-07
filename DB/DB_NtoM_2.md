# 팔로우 기능 구현

## 프로필 페이지

- 각 회원의 개인 프로필 페이지에 팔로우 기능을 구현하기 위해 프로필 페이지를 먼저 구현하기

- 프로필 페이지에 해당 사용자의 추가 정보를 같이 볼 수 있게 내용 추가
  - 해당 사용자가 작성한 게시글 목록
  - 해당 사용자가 작성한 댓글 목록
  - 해당 사용자가 좋아요를 누른 게시글 목록

---

## 👤 Django 프로필 페이지 구현

### 1. URL 주소 작성
프로필 페이지로 접근하기 위한 URL을 설정합니다.

* 프로필 페이지는 사용자와 관련된 기능이기 때문에 `accounts` 앱의 `urls.py`에 추가합니다.
* 로그인한 유저뿐만 아니라 다른 사람의 프로필 페이지 방문도 가능해야 합니다.
* 사용자의 `username`을 variable routing을 활용하여 정보 전달이 필요합니다.

```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns =[
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # ... (중략)
    
    # username을 인자로 받는 프로필 URL 패턴 추가
    path('profile/<username>/', views.profile, name='profile'),
]
```

<br>

### 2. View 함수 작성
URL로 전달받은 username을 활용해 사용자 데이터를 조회하는 뷰 함수를 작성합니다.

* URL로 전달되는 `username`을 이용하여 사용자 정보를 조회하고 이를 template으로 전달합니다.
* 유저 모델은 직접 import 하지 않고, `get_user_model()` 함수를 사용해야 합니다.

```python
# accounts/views.py

from django.contrib.auth import get_user_model
from django.shortcuts import render

def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)
```

<br>

### 3. 프로필 페이지 세부 내용 작성
조회한 사용자(person)의 정보와 역참조를 활용하여 작성한 글, 댓글, 좋아요 한 글을 표시합니다.

```html
<!-- accounts/profile.html -->

<h1>{{ person.username }}님의 프로필</h1>
<hr>

<h2>{{ person.username }}가 작성한 게시글</h2>
{% for article in person.article_set.all %}
  <div>{{ article.title }}</div>
{% endfor %}
<hr>

<h2>{{ person.username }}가 작성한 댓글</h2>
{% for comment in person.comment_set.all %}
  <div>{{ comment.content }}</div>
{% endfor %}
<hr>

<h2>{{ person.username }}가 좋아요한 게시글</h2>
{% for article in person.like_articles.all %}
  <div>{{ article.title }}</div>
{% endfor %}
```

<br>

### 4. 내 프로필 링크 추가 (Index 페이지)
메인 페이지(`index.html`)에서 로그인한 사용자가 자신의 프로필로 이동할 수 있는 링크를 추가합니다.

```html
<!-- articles/index.html -->

<h1>Articles</h1>
{% if request.user.is_authenticated %}
  <h3>Hello, {{ user.username }}</h3>
  
  <!-- 내 프로필로 이동하는 링크 추가 -->
  <a href="{% url 'accounts:profile' user.username %}">내 프로필</a>
  
  <a href="{% url 'articles:create' %}">NEW</a>
  
  <!-- ... (중략) -->
{% endif %}
<hr>
```

<br>

### 5. 다른 유저의 프로필 링크 추가 (Index 페이지)
게시글 목록에서 다른 유저의 아이디를 클릭하면 해당 유저의 프로필 페이지로 이동할 수 있도록 링크를 추가합니다.

```html
<!-- articles/index.html -->

<!-- ... (중략) -->

{% for article in articles %}
  <!-- 작성자 이름을 클릭하면 해당 작성자의 프로필로 이동하는 링크 추가 -->
  <p>작성자 : 
    <a href="{% url 'accounts:profile' article.user.username %}">
      {{ article.user }}
    </a>
  </p>
  <p>글 번호: {{ article.pk }}</p>
  
  <!-- ... (중략) -->
  <hr>
{% endfor %}
```

---

## 모델 관계 설정

**User(M) - User(N)**

팔로우는 유저와 유저와의 관계를 나타냄
  - 회원은 여러 명의 회원을 팔로우 할 수 있고, 한 명도 하지 않을 수도 있음
  - 회원은 여러 명의 팔로워를 가질 수 있고, 한 명도 가지지 않을 수도 있음


---

### 🤝 팔로우 모델 관계 설정

#### 1. 모델 필드 추가 (1/2)
커스텀한 User 모델 클래스에 `ManyToManyField`를 사용하여 팔로우 필드를 추가합니다.

* User 모델과 관계를 맺는 것이기 때문에 `settings.AUTH_USER_MODEL`을 사용해도 되지만, 자기 자신과의 관계이기 때문에 `'self'`로 표현할 수 있습니다.
* 팔로우 기능은 단방향의 관계이기 때문에 반드시 `symmetrical` 속성을 `False`로 설정해야 합니다.
* **참조 필드**는 `followings` 필드로, 내가 팔로우하는 사람들을 의미합니다.
* **역참조 필드**는 `user_set`을 사용해도 되지만 명확한 설정을 위해 `related_name`을 이용하여 `'followers'`로 변경합니다.

```python
# accounts/models.py

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
```

> **※ 참고**
> 참조, 역참조는 서로 바뀌어도 상관없으나 관계 조회 시 생각하기 편한 방향으로 정하여 작성되었습니다.

<br>

#### 2. 데이터베이스 테이블 확인 (2/2)
Migration 진행 후 데이터베이스에 중개 테이블이 정상적으로 생성되었는지 확인합니다.

* **Migration 진행 후 생성된 중개 테이블 구조**
  * 테이블명: `accounts_user_followings`
  * **Columns**
    * 🔑 `id` (INTEGER) : Primary Key
    * 🔗 `from_user_id` (bigint) : Foreign Key (팔로우를 하는 사람)
    * 🔗 `to_user_id` (bigint) : Foreign Key (팔로우를 받는 사람)