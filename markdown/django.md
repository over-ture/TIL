
---

## 장고 프로젝트 순서

1. **프로젝트 작성**: 
    ```
    django-admin startproject yourprojectname
    ```
2. **앱 생성**: 
    ```
    python manage.py startapp yourappname
    ```
3. **모델 정의**: 앱의 `models.py`에서 데이터베이스 테이블 정의
4. **보기와 템플릿 작성**: 검토를 통해 로직 처리하며 템플릿 사용하여 HTML 작성
5. **URL 설정**: `urls.py`에서 URL 패턴 정의 및 보기와 연결
6. **데이터베이스 마이그레이션**: 
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
7. **정적 및 미디어 파일 관리**: CSS, JavaScript, 이미지 등 관리 및 설정
8. **개발 서버 실행**: 
    ```
    python manage.py runserver
    ```
9. **배포**: 호스팅 서비스에 배포

---

### mysite03 예제 (blog)

1. ```
   python manage.py startapp blog
   ```
2. `mysite03.setting`에 `INSTALLED_APPS = ['blog']` 추가
3. `blog.view.py` 함수 생성 (request, response)
4. `blog.urls.py` URL 패턴 매핑
5. `mysite03.urls.py`에 `blog.urls.py` 연결

### mysite03 예제 (notice)

1. ```
   python manage.py startapp notice
   ```
2. `mysite03.setting`에 `INSTALLED_APPS = ['notice']` 추가
3. `notice.view.py` 함수 생성 (request, response)
4. `notice.urls.py` URL 패턴 매핑
5. `mysite03.urls.py`에 `notice.urls.py` 연결

---

## 실습

- **새 마이그레이션 생성**: 
    ```
    python manage.py makemigrations
    ```

- **변경사항 데이터베이스 적용**: 
    ```
    python manage.py migrate
    ```

- **마이그레이션 상태 확인**: 
    ```
    python manage.py showmigrations
    ```

---

## 장고 관리자

1. `admin.py`에 `Post` 속성값 추가: `admin.site.register(Post)`
2. `127.0.0.1:8000/admin` 접속 후 `blog/post` 확인 및 게시물 등록
3. 등록된 게시물 표시: `blog.views.py`
4. `settings.py`에 `TEMPLATES =['DIRS': [BASE_DIR/'templates'],]` 추가

---

## 장고 레이아웃 및 폼 양식

1. 앱 디렉토리 `blog.forms.py` 파일 생성
2. `django.forms.ModelForm` 임포트
3. `class PostForm(ModelForm):` 클래스 생성
4. `PostForm` 경로 URL 패턴에 등록

---

## 'django-admin'의 db 관련 명령어

- `makemigrations`
- `migrate`
- `sqlflush`
- `sqlmigrate`: sql 미리보기
- `sqlsequencereset`

---

## 실습

- **1**. urls.py에 가서 `urlpattern = [ path( '/post/edit/<int:id>', views.edit_post), , , ]` 추가
- **2**. urls.py에 가서 `urlpattern = [ path( '/post/delete/<int:id>', views.delete_post), , , ]` 추가
- **3**. `blog/post_form.html`의 데이터를 수정 ->
Id 값 추가 수정 `<h2>{% if id %} Edit {% else %} New {% endif %} Post </h2>`
- **4**. `home.html` 각 게시물에 편집(EDIT) 링크를 포함하도록 템플릿을 수정
	`<p> <a href = '{%url 'post-edit' post.id %}'> Edit </a></p>`
- **5**.	`<a>` 태그를 통해 get 방식으로 id값을 넘겨서 페이지 렌더링 한 것을 확인하기
	GET 방식으로 id값은 링크된 url로 넘어가는 것 확인 후 내용 변경한 다음 save 버튼을 클릭할 때
	POST 방식으로 업데이트 되지 않는다
- **6**. POST 방식의 코드를 추가한다. `views.edit_post : GET / POST`
- **7**. `message`를 선언하고 활용한다. 각 메시지가 적용되는 `views.py` 함수에 모듈 추가 후 코드 작성
    - `from django.contrib import messages`
- **8**. base.html에 https://docs.djangoproject.com/en/4.2/ref/contrib/messages/ 참조해서 작성
- **9**. `delete` 렌더링 한다. `views.delete_post, GET / POST`

---

## Django에 User 추가하기
```django
> from django.contrib.auth.models import User
> user = User.objects.create_user('test', 'test91@example.com', 'testtest')
> # user.is_superuser = True
> user.is_staff = True
> user.save()
```
---
## 사용자 가입 화면 추가

1. `from django.contrib.auth.forms import UserCreationForm`의 클래스를 임포트하고 상속받기 -> `form.py`
2. `urls.py` 매핑, `views.py` 코드 작성
3. `def sign_up(request)`: get/post(조건지정 저장)
4. register.html: error 체크, base.html: register 링크 추가
5. 사용자가 다른 사용자가 작성한 내용을 수정,삭제 하지 못하도록 하기 -> `blog.views.py` ->
`from django.contrib.auth.decorators import login_required`
@login_required 수정, 삭제 함수 위에 선언하고 404 요청지정함수 추가
6. `home.html` : 수정, 삭제 링크 숨기기

---
### 자료 관리
1. dumpdata / loaddata
- **실습**
    1. data.json -> 모델명, 기본 키값, 모델 필드
        -  python manage.py dumpdata -> data.json
    2. 다른 확장자를 가진 파일로 내보내기 할 때 `--format` 지정한다.
        - `python manage.py dumpdata > filename --format file_format (docs Serialization formats)`
        - `python manage.py dumpdata > data.xml --format xml`
        - `python manage.py dumpdata blog.Post > Post.json`
    3. 데이터 업로드 실습
        - 데이터 업로드 할 때는 폴더명이 반드시 존재
        - `python manage.py loaddata data.json`