
# DRF Charging Station API 구현 정리

## 요구사항

- Location 정보를 생성할 수 있어야 한다.
- Station 정보를 생성할 수 있어야 한다.
- Station이 참조하는 Location 정보는 사용자가 직접 입력하지 않는다.
- Station 전체 목록을 조회할 수 있어야 한다.
- Station 목록 조회 시 `address`, `is_opening` 정보를 제공한다.
- Station 상세 정보를 조회할 수 있어야 한다.
- Station 상세 조회 시 Station의 모든 정보를 제공한다.

---

## URL 구성

```python
# stations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.location_create),
    path('locations/<int:location_pk>/stations/', views.station_create),
    path('stations/', views.station_list),
    path('stations/<int:station_pk>/', views.station_detail),
]
```

### URL 역할

| URL | Method | 기능 |
|---|---|---|
| `/api/v1/locations/` | POST | Location 생성 |
| `/api/v1/locations/<location_pk>/stations/` | POST | 특정 Location을 참조하는 Station 생성 |
| `/api/v1/stations/` | GET | Station 전체 목록 조회 |
| `/api/v1/stations/<station_pk>/` | GET | Station 상세 조회 |

---

## View 구성

```python
# stations/views.py

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Location, Station
from .serializers import LocationSerializer, StationListSerializer, StationSerializer


@api_view(['POST'])
def location_create(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def station_create(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)

    serializer = StationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(address=location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def station_list(request):
    stations = Station.objects.all()
    serializer = StationListSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def station_detail(request, station_pk):
    station = get_object_or_404(Station, pk=station_pk)
    serializer = StationSerializer(station)
    return Response(serializer.data)
```

---

## 핵심 구현 포인트

### 1. Location 생성

```python
@api_view(['POST'])
def location_create(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

사용자가 보낸 `address` 값을 이용해 Location 객체를 생성한다.

---

### 2. Station 생성

```python
@api_view(['POST'])
def station_create(request, location_pk):
    location = get_object_or_404(Location, pk=location_pk)

    serializer = StationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(address=location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Station 생성 시 사용자가 Location 정보를 직접 입력하지 않는다.

대신 URL에서 받은 `location_pk`를 이용해 Location 객체를 조회한 뒤,

```python
serializer.save(address=location)
```

형태로 Station의 ForeignKey 필드에 직접 저장한다.

---

### 3. Station 목록 조회

```python
@api_view(['GET'])
def station_list(request):
    stations = Station.objects.all()
    serializer = StationListSerializer(stations, many=True)
    return Response(serializer.data)
```

전체 Station 목록을 조회한다.

목록에서는 `StationListSerializer`를 사용하여 필요한 필드만 응답한다.

---

### 4. Station 상세 조회

```python
@api_view(['GET'])
def station_detail(request, station_pk):
    station = get_object_or_404(Station, pk=station_pk)
    serializer = StationSerializer(station)
    return Response(serializer.data)
```

URL에서 받은 `station_pk`를 이용해 특정 Station 객체를 조회한다.

존재하지 않는 pk가 들어오면 404 응답을 반환한다.

---

## Serializer 구성

```python
# stations/serializers.py

from rest_framework import serializers
from .models import Station, Location


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class StationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('address', 'is_opening',)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
```

---

## 참고: address를 문자열로 보여주고 싶은 경우

기본적으로 `Station` 모델의 `address` 필드는 `Location`을 참조하는 ForeignKey이므로 응답에서는 Location의 pk가 출력된다.

예를 들어 다음과 같이 응답될 수 있다.

```json
[
  {
    "address": 1,
    "is_opening": false
  }
]
```

만약 Location의 실제 주소 문자열을 출력하고 싶다면 Serializer에서 다음처럼 작성할 수 있다.

```python
class StationListSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address.address', read_only=True)

    class Meta:
        model = Station
        fields = ('address', 'is_opening',)
```

그러면 응답은 다음처럼 나온다.

```json
[
  {
    "address": "서울특별시 강남구",
    "is_opening": false
  }
]
```

---

## 실수했던 부분

### 함수 인자 불일치

처음에는 `station_list` 함수가 `location_pk`를 받도록 되어 있었지만, `/stations/` URL에서는 `location_pk`를 넘기지 않았다.

```python
def station_list(request, location_pk):
```

이 상태에서 `/stations/`로 요청하면 URL과 View 함수의 인자가 맞지 않아 문제가 생긴다.

따라서 목록 조회와 Station 생성을 분리했다.

```python
def station_list(request):
def station_create(request, location_pk):
```

---

### Station 생성 시 Location 연결 누락

Station 생성에서 `location_pk`를 URL로 받더라도, 실제로 저장할 때 연결하지 않으면 ForeignKey 값이 저장되지 않는다.

따라서 다음처럼 저장해야 한다.

```python
serializer.save(address=location)
```

---

### source 오타

주소 문자열을 출력하려고 할 때 다음처럼 오타가 있으면 `address`가 응답에서 빠질 수 있다.

```python
address = serializers.CharField(source='address.addresss', read_only=True)
```

올바른 코드는 다음과 같다.

```python
address = serializers.CharField(source='address.address', read_only=True)
```
