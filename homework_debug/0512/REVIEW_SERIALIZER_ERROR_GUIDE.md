# ReviewListSerializer AssertionError 정리

## 발생 상황

다음 URL로 `GET` 요청을 보냈을 때 에러가 발생한다.

```http
GET http://127.0.0.1:8000/api/v1/reviews/
```

발생한 에러 메시지:

```text
AssertionError at /api/v1/reviews/
The field 'book' was declared on serializer ReviewListSerializer, but has not been included in the 'fields' option.
```

## 에러 발생 과정

`/api/v1/reviews/` 요청이 들어오면 `libraries/views.py`의 `review_list` 함수가 실행된다.

```python
@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
```

여기서 `ReviewListSerializer`를 사용해 `Review` 객체 목록을 JSON 응답으로 변환하려고 한다.

문제가 되는 serializer는 다음과 같다.

```python
class ReviewListSerializer(serializers.ModelSerializer):

    class BookisbnSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('isbn', )

    book = BookisbnSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('content', 'score',)
```

`ReviewListSerializer` 안에는 `book` 필드가 직접 선언되어 있다.

```python
book = BookisbnSerializer(read_only=True)
```

하지만 `Meta.fields`에는 `book`이 포함되어 있지 않다.

```python
fields = ('content', 'score',)
```

DRF는 serializer에 직접 선언된 필드가 있으면, 그 필드가 `Meta.fields`에도 포함되어 있어야 한다고 검사한다. 따라서 `serializer.data`를 평가하는 과정에서 `book` 필드가 누락되었다고 판단하고 `AssertionError`를 발생시킨다.

## 원인

직접 선언한 serializer 필드 `book`이 `Meta.fields` 옵션에 포함되어 있지 않기 때문이다.

현재 코드:

```python
book = BookisbnSerializer(read_only=True)

class Meta:
    model = Review
    fields = ('content', 'score',)
```

DRF 기준에서 위 코드는 다음과 같은 의미가 된다.

- `book`이라는 응답 필드를 만들겠다고 선언함
- 하지만 실제 출력 필드 목록에는 `book`을 넣지 않음
- 선언된 필드와 출력 필드 목록이 맞지 않으므로 에러 발생

## 해결 방안 1: `fields`에 `book` 추가

가장 직접적인 해결 방법은 `Meta.fields`에 `book`을 포함하는 것이다.

```python
class ReviewListSerializer(serializers.ModelSerializer):

    class BookisbnSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ('isbn', )

    book = BookisbnSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('content', 'score', 'book',)
```

예상 응답 형태:

```json
[
  {
    "content": "리뷰 내용",
    "score": 5,
    "book": {
      "isbn": "1234567890"
    }
  }
]
```

## 해결 방안 2: `book` 필드를 사용하지 않을 경우 삭제

리뷰 목록 응답에 책 정보가 필요 없다면, 직접 선언한 `book` 필드를 삭제해도 된다.

```python
class ReviewListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ('content', 'score',)
```

예상 응답 형태:

```json
[
  {
    "content": "리뷰 내용",
    "score": 5
  }
]
```

## 해결 방안 3: ISBN만 문자열로 보여주기

`book`을 중첩 객체가 아니라 ISBN 문자열만 보여주고 싶다면 `source`를 사용할 수 있다.

```python
class ReviewListSerializer(serializers.ModelSerializer):
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    
    class Meta:
        model = Review
        fields = ('content', 'score', 'book_isbn',)
```

예상 응답 형태:

```json
[
  {
    "content": "리뷰 내용",
    "score": 5,
    "book_isbn": "1234567890"
  }
]
```

## 추천

현재 코드의 의도는 리뷰 목록에서 연결된 책의 ISBN을 함께 보여주려는 것으로 보인다.

따라서 가장 간단한 수정은 다음과 같다.

```python
class Meta:
    model = Review
    fields = ('content', 'score', 'book',)
```

이렇게 하면 기존에 작성한 `BookisbnSerializer`를 그대로 활용하면서 에러를 해결할 수 있다.
