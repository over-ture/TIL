# Media Files

**미디어 파일**

- 사용자가 웹사이트를 통해 직접 업로드하는 파일

## 이미지 업로드

**`ImageField()`**

- 이미지 파일을 업로드하기 위해 사용하는 Django 모델 필드
- 데이터베이스 저장 방식
  - 가장 중요한 특징은 이미지 파일 자체가 DB에 저장되는 것이 아니라는 점
  - 데이터베이스에는 `upload_to` 경로를 기준으로 한 이미지 파일의 경로(문자열)만 저장되고, 실제 파일은 서버의 특정 폴더(MEDIA_ROOT)에 저장

```python
# models.py

class Article(models.Model):
  # 이미지는 'MEDIA_ROOT경로/images/' 경로에 저장되고,
  # DB에는 'images/sample.png'와 같은 경로 문자열이 저장됨
  image = models.ImageField(upload_to='images/')
```

**미디어 파일을 제공하기 전 준비사항**

1. `settings.py`에 `MEDIA_ROOT`, `MEDIA_URL` 설정
2. 작성한 `MEDIA_ROOT`와 `MEDIA_URL`에 대한 URL 지정

**MEDIA_ROOT란?**

![alt text](images/mediaroot.png)

**MEDIA_URL이란?**

![alt text](images/mediaurl.png)

**MEDIA_ROOT와 MEDIA_URL 설정 (1/2)**

- MEDIA_ROOT는 <span style='color:darkred'>파일을 저장하고 관리하기 위한 서버의 실제 경로</span>
- MEDIA_URL은 <span style='color:darkred'>그 파일을 웹에서 보여주기 위한 가상의 주소</span>
  ```python
  # settings.py
  
  MEDIA_ROOT = BASE_DIR / 'media'
  
  MEDIA_URL = 'media/'
  ```
  
**MEDIA_ROOT와 MEDIA_URL 설정 (2/2)**

- `settings.MEDIA_URL`: "media/로 시작하는 URL 요청이 오면"
- `document_root=settings.MEDIA_ROOT`: "MEDIA_ROOT에 지정된 실제 폴더에서 파일을 연결"

  ```python
  from django.conf import settings
  from django.conf.urls.static import static
  
  urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```
  ![alt text](images/mediaroot_tips.png)