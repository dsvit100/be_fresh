from django.db import models
from django.contrib.auth.models import User

# 식품 카테고리 모델
# 대분류(채소, 육류 등)과 소분류(브로콜리류, 쌈채소류 등)를 관리
# 각 카테고리별 기본 보관일 설정
class FoodCategory(models.Model):
    name = models.CharField(max_length=50) # 대분류
    subcategory = models.CharField(max_length=50) # 소분류
    default_storage_days = models.IntegerField() # 기본 보관일

    # django 관리자 페이지에서 한글로 보이도록 설정
    class Meta:
        verbose_name = '식품 카테고리'
        verbose_name_plural = '식품 카테고리들'
    
    # 이건 왜 쓰는지 모르겠는뎅 나중에 django 들어가서 확인하기
    def __str__(self):
        return f"{self.name} - {self.subcategory}"