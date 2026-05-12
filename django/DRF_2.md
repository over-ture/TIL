# DRF with N:1 Relation

---
### 사전 준비 (1/3)

* **Comment 모델 클래스 정의**

```python
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

<br>

### 사전 준비 (2/3)

* **Articles app에 정의된 모델 정보 makemigration**

```bash
$ python manage.py makemigrations
```
```text
Migrations for 'articles':
  articles\migrations\0001_initial.py
    + Create model Article
    + Create model Comment
```

> **※ 각 명령어 실행 후, 실행 결과 확인 필수!**

<br>

### 사전 준비 (3/3)

* **데이터베이스 초기화**

```bash
$ python manage.py migrate
```
```text
Operations to perform:
  Apply all migrations: admin, articles, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
```

* **fixtures 데이터 삽입**

```bash
$ python manage.py loaddata articles.json comments.json
```
```text
Installed 40 object(s) from 2 fixture(s)
```

> **※ 각 명령어 실행 후, 실행 결과 확인 필수!**

<br>

### URL 및 HTTP request method 구성

> **※ 오늘 수업에서 작성할 request method 구성**

| URL | GET | POST | PUT | DELETE |
| :--- | :--- | :--- | :--- | :--- |
| `comments/` | 댓글 목록 조회 | | | |
| `comments/1/` | 단일 댓글 조회 | | 단일 댓글 수정 | 단일 댓글 삭제 |
| `articles/1/comments/` | | 댓글 생성 | | |

*<small><표1_Django_DRF 2_request method 구성></small>*


---

## GET method

<br>

### GET - List (1/3)

* **댓글 목록 조회를 위한 CommentSerializer 정의**

```python
# articles/serializers.py
from .models import Article, Comment
from rest_framework import serializers # 이미지에는 생략되어 있으나 통상적으로 필요함

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
```

> **💡 ModelSerializer**
> Django 모델 구조를 바탕으로 자동으로 필드를 생성해주는 Serializer 클래스

* **url 작성**

```python
# articles/urls.py
urlpatterns = [
    ...,
    path('comments/', views.comment_list),
]
```

<br>

### GET - List (2/3)

* **view 함수 작성**

```python
# articles/views.py

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer

@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
```

<br>

### GET - List (3/3)

* GET[http://127.0.0.1:8000/api/v1/comments/](http://127.0.0.1:8000/api/v1/comments/) 응답 확인

<br>

---

<br>

### GET - Detail (1/2)

* **단일 댓글 조회를 위한 url 및 view 함수 작성**

```python
# articles/urls.py

urlpatterns =[
    ...,
    path('comments/<int:comment_pk>/', views.comment_detail),
]
```

```python
# articles/views.py

@api_view(['GET'])
def comment_detail(request, comment_pk):
    # 특정 댓글 데이터를 조회
    comment = Comment.objects.get(pk=comment_pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
```

<br>

### GET - Detail (2/2)

* GET[http://127.0.0.1:8000/api/v1/comments/1/](http://127.0.0.1:8000/api/v1/comments/1/) 응답 확인


---

## POST method

<br>

### POST (1/6)

* **단일 댓글 생성을 위한 url 및 view 함수 작성**

```python
# articles/urls.py

urlpatterns =[
    ...,
    path('articles/<int:article_pk>/comments/', views.comment_create),
]
```

```python
# articles/views.py

@api_view(['POST'])
def comment_create(request, article_pk):
    # 어떤 게시글에 작성되는 댓글인지 단일 게시글을 조회
    article = Article.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

<br>

### POST (3/6)

* **POST[http://127.0.0.1:8000/api/v1/articles/1/comments/](http://127.0.0.1:8000/api/v1/articles/1/comments/) 응답 확인**

```json
{
    "article":[
        "This field is required."
    ]
}
```

> **400 Bad Request**
> **※ 상태코드 400 응답 확인**

*<small><그림5_Django_DRF 2_댓글 생성 실패 POSTman></small>*

<br>

### POST (4/6)

* **POST[http://127.0.0.1:8000/api/v1/articles/1/comments/](http://127.0.0.1:8000/api/v1/articles/1/comments/) 응답 확인**
  * **상태 코드 400** 응답 확인
  * `CommentSerializer`에서 외래 키에 해당하는 `article` field 또한 사용자로부터 입력 받도록 설정되어 있기 때문에 서버 측에서는 누락되었다고 판단한 것
  * **유효성 검사 목록에서 제외 필요**
  * `article` field를 **읽기 전용 필드**로 설정하기

> **💡 상태 코드**
> 요청 처리 결과를 알려주는 숫자 응답 신호
> *<small><개념2_Django_DRF 2_상태 코드></small>*

<br>

### POST (5/6)

* **데이터를 전송받은 시점에 "**유효성 검사에서 제외**시키고, **데이터 조회 시에는 출력**" 하는 필드**

```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)
```

> **💡 유효성 검사 (Validation)**
> 입력된 데이터가 조건에 맞는지 확인하는 검사 과정
> *<small><개념3_Django_DRF 2_유효성 검사></small>*

<br>

### POST (6/6)

* **POST[http://127.0.0.1:8000/api/v1/articles/1/comments/](http://127.0.0.1:8000/api/v1/articles/1/comments/) 재요청**

```json
{
    "id": 21,
    "content": "댓글 생성",
    "created_at": "...",
    "updated_at": "...",
    "article": 1
}
```

> **201 Created**
> **※ 상태코드 201 응답 확인**

*<small><그림6_Django_DRF 2_댓글 생성 성공 POSTman></small>*

---

## 읽기 전용 필드 (`read_only_fields`)

<br>

### 1. 읽기 전용 필드 개념
**서버가 조회 요청에 대한 응답 시에만 값을 표시하는 필드**입니다.
* `read_only_fields`는 클라이언트가 입력해서는 안 되는 필드를 **응답 전용 필드**로 지정할 때 사용합니다.
* **(중요)** view 함수에서 값을 직접 주입할 필드(예: 댓글 작성 시 특정 게시글 참조를 위한 `article` 필드)는 반드시 `read_only_fields`로 지정해야 합니다.
* 지정하지 않을 경우, DRF는 클라이언트 요청 데이터에 해당 필드 값이 빠졌다고 판단하여 유효성 검사 실패(**400 Bad Request 에러**)를 발생시킵니다.

<br>

### 2. 읽기 전용 필드 사용 목적
* 클라이언트 측에서 직접 수정하면 안 되는 경우
* 서버 로직에 의해 자동 생성·관리되는 값 활용
* 입력은 받지 않지만 정보를 제공해야 하는 경우
* 새로운 필드 값(추가 계산, 가공)을 만들어 제공해야 하는 경우

<br>

### 3. 읽기 전용 필드 특징 및 주의사항

#### 📌 유효성 검사에서 제외됨
* 읽기 전용 필드는 클라이언트가 보내는 요청 데이터에서 고려되지 않으므로, 유효성 검사 대상에서 제외됩니다.
* 즉, 클라이언트가 악의적이나 실수로 해당 필드에 값을 넣어서 요청하더라도 **무시**되며 검증 오류를 일으키지 않습니다.

#### 📌 생성·수정 요청 모두에서 적용 가능
* 읽기 전용 필드라 해서 생성(POST) 단계에서만 무의미한 것은 아닙니다.
* 수정(PUT) 요청에서도 해당 필드는 여전히 클라이언트 입력을 받지 않고, 오직 응답 시에만 노출됩니다.

---

## 응답 데이터 재구성

### 댓글 조회 시 게시글 출력 내역 변경

#### 1. 변경 목표
댓글(Comment) 조회 시 참조하고 있는 게시글(Article)의 **번호(id)만 제공하는 것이 아니라, '게시글의 제목(title)'까지 포함**하여 제공하도록 응답 데이터를 재구성합니다.
* **기존 응답:** `"article": 1`
* **변경 응답:** `"article": { "title": "게시글 제목 내용..." }`

<br>

#### 2. 기본 동작의 한계와 해결책
* **한계:** `Comment` 모델은 `Article`과 외래 키(ForeignKey)로 연결되어 있으며, Django DRF의 기본 `ModelSerializer`는 관계된 모델의 값으로 숫자(id)만을 반환합니다.
* **해결책:** 응답 구조를 결정하는 것은 Serializer입니다. `Article`의 특정 필드(`title`)만 반환하는 **새로운 Serializer를 별도로 정의**하여 이를 적용해야 합니다.

<br>

#### 3. Nested Serializer (중첩 시리얼라이저) 작성
* `Article`의 제목만 처리하는 `ArticleTitleSerializer`를 생성합니다.
* 이 Serializer가 오직 `CommentSerializer` 안에서만 사용된다면, 코드의 응집도를 높이기 위해 **클래스 내부에 정의**하는 것이 좋습니다.
* 기존 `article` 외래 키 필드를 새로 만든 `ArticleTitleSerializer`로 덮어씌워(Override) 줍니다.

```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    
    # 1. 게시글의 title 필드만 포함하는 내부 Serializer 정의
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)

    # 2. Comment 모델의 article 필드를 재정의 
    # (주의: 내부 필드로 재정의 시 read_only 속성을 여기에 직접 부여합니다)
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        # 3. 기존에 사용했던 아래 코드는 주석 처리 또는 삭제합니다.
        # read_only_fields = ('article',) 
```

<br>

#### 4. 결과 확인
* `GET http://127.0.0.1:8000/api/v1/comments/1/` 조회 시 다음과 같이 중첩된 JSON 형태로 데이터가 성공적으로 재구성된 것을 확인할 수 있습니다.

```json
{
    "id": 1,
    "article": {
        "title": "Water behavior return interesting return understand."
    },
    "content": "Tonight free why name break...",
    "created_at": "1975-12-07T13:38:25Z",
    "updated_at": "1991-01-16T06:45:10Z"
}
```

---

## 역참조 데이터 구성

### Article -> Comment 간 역참조 관계를 활용한 JSON 데이터 재구성
* 단일 게시글 조회 시 아래 2가지 사항에 대한 데이터 재구성하기
    1. 단일 게시글 조회 시 **해당 게시글에 작성된 댓글 목록**도 함께 붙여서 응답
    2. 단일 게시글 조회 시 **해당 게시글에 작성된 댓글 개수**도 함께 붙여서 응답

---

### 1. 단일 게시글 + 댓글 목록

#### Nested relationships (역참조 매니저 활용)
* 모델 관계 상으로 **참조하는 대상(N)**은 **참조되는 대상(1)**의 표현에도 포함되거나 중첩될 수 있습니다.
* `Comment`가 `Article`에 대한 정보를 `article` field를 사용하여 표현하였듯, `Article`은 자신을 참조하고 있는 `comment`들에 대한 정보를 역참조 매니저를 통해 표현할 수 있습니다.

```python
# articles/serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    # 1. 중첩할 역참조 데이터(댓글)를 위한 Serializer 내부 정의
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
            
    # 2. 역참조 매니저 이름(comment_set)을 필드명으로 사용하여 재정의
    # 여러 개의 댓글이 올 수 있으므로 many=True 설정 필수
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
```

* **응답 확인:** `GET http://127.0.0.1:8000/api/v1/articles/2/` 요청 시 응답 JSON 구조 안에 `comment_set` 배열이 포함되어 해당 게시글의 댓글 목록이 출력됩니다.

---

### 2. 단일 게시글 + 댓글 개수

#### 단일 게시글 조회 시, 댓글 개수도 함께 제공하고 싶다면?
* 기본적으로 게시글(`Article`)을 조회하면 참조 중인 댓글(`Comment`)의 개수는 알 수 없습니다.
    * `Comment` 모델과의 관계는 `Article.comment_set`으로 연결되지만, **댓글의 개수를 저장하는 별도 필드**는 `Article` 모델에 정의한 적이 없기 때문입니다.
* 따라서, 댓글 수를 응답하려면 **직접 계산해서 응답에 포함**시켜야 합니다.

#### View 로직 개선: `annotate` 사용
* View에서 `Article` 객체를 조회할 때 `annotate`를 활용해 `num_of_comments` 필드를 임시로 추가합니다.
* 다음과 같이 댓글 수를 세어 필드를 추가하면, `article` 객체에는 `num_of_comments`라는 주석(annotate) 필드가 포함되게 됩니다.

> **💡 `annotate` 란?**
> Django ORM 함수로, SQL의 집계 함수를 활용하여 쿼리 단계에서 데이터 가공을 수행합니다.

```python
# articles/views.py
from django.db.models import Count

@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    # Count('comment')에서 'comment'는 Article을 참조하고 있는 모델 Comment의 소문자 표기입니다.
    article = Article.objects.annotate(num_of_comments=Count('comment')).get(pk=article_pk)
    # ... 아래 로직 동일
```

#### Serializer 개선: `SerializerMethodField` 사용
* 단순히 `fields = '__all__'` 만으로는 `annotate`된 필드가 포함되지 않습니다. (`__all__`은 실제 모델의 필드 기준으로 작동하기 때문)
* 동적으로 계산된 임시 필드를 응답에 포함하려면 **`SerializerMethodField`**를 사용해야 합니다.
* `SerializerMethodField`는 **읽기 전용 필드를 커스터마이징** 하는데 사용됩니다.
* 이 필드를 선언한 뒤 `get_<필드명>` 메서드를 정의하면, 해당 메서드의 반환 값이 직렬화 결과에 포함됩니다.

```python
# articles/serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    # ... (생략)
    
    # 1. SerializerMethodField 선언
    num_of_comments = serializers.SerializerMethodField()
    
    class Meta:
        # ...
        pass
        
    # 2. get_num_of_comments 메서드 정의
    def get_num_of_comments(self, obj):
        # 여기서 obj는 Serializer가 처리하는 Article 인스턴스입니다.
        # View에서 annotate 한 필드를 객체의 속성처럼 그대로 사용 가능합니다.
        return obj.num_of_comments
```
* 이제 `serializer.data` 호출 시 자동으로 `get_num_of_comments` 메서드가 실행되어 `num_of_comments` 값이 응답 데이터에 제공됩니다.
* **응답 확인:** `GET http://127.0.0.1:8000/api/v1/articles/3/` 요청 시 응답 JSON 하단에 `"num_of_comments": 2` 와 같이 댓글 개수가 정상적으로 출력됩니다.