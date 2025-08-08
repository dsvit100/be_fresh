from django.urls import path
from . import views

# 앱별 URL 네임스페이스 설정 (템플릿에서 fridge:home 형태로 사용)
app_name = 'fridge'

# fridge 앱 내의 URL 패턴
urlpatterns = [
    path('', views.home, name='home'),  # 메인 페이지
]