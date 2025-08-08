from django.db import models
from django.contrib.auth.models import User

# 식품 카테고리 모델
# 대분류(채소, 육류 등)과 소분류(브로콜리류, 쌈채소류 등)를 관리
# 각 카테고리별 기본 보관일 설정
class FoodCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='대분류') # 대분류
    subcategory = models.CharField(max_length=50, verbose_name='소분류') # 소분류
    default_storage_days = models.IntegerField(verbose_name='기본 보관일') # 기본 보관일

    # django 관리자 페이지에서 한글로 보이도록 설정
    class Meta:
        verbose_name = '식품카테고리'
        verbose_name_plural = '식품카테고리들'
    
    # 이건 왜 쓰는지 모르겠는뎅 나중에 django 들어가서 확인하기
    def __str__(self):
        return f"{self.name} - {self.subcategory}"


# 개별 식품 모델
# 구체적인 식품명과 어떤 카테고리에 속하는지 관리
# 메인 화면 버튼으로 표시할지 여부 (True/False)
class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='식품명')
    # 예: 브로콜리, 닭가슴살, 우유, 토마토 등
    
    # 위에서 만든 FoodCategory와 연결
    category = models.ForeignKey(
        FoodCategory, 
        on_delete=models.CASCADE,
        verbose_name='카테고리'
    )
    
    is_main_button = models.BooleanField(
        default=False, 
        verbose_name='메인버튼 표시'
    )
    # True면 메인 화면에 버튼으로 표시

    class Meta:
        verbose_name = '식품'
        verbose_name_plural = '식품들'
    
    def __str__(self):
        return self.name


# 식품 매핑 모델
# 사용자가 검색한 키워드를 기존 식품과 연결
# 예: '콜리플라워' 검색 시 '브로콜리'와 같은 보관기간 적용
class FoodMapping(models.Model):
    search_keyword = models.CharField(
        max_length=100, 
        verbose_name='검색키워드'
    )
    # 사용자가 입력한 검색어 (예: 콜리플라워, 양배추, 케일 등)
    
    mapped_to_food = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE,
        verbose_name='매핑될식품'
    )
    # 검색어와 연결될 기존 식품 (예: 브로콜리)
    
    confidence_level = models.FloatField(
        default=1.0, 
        verbose_name='신뢰도'
    )
    # 1.0 = 100% 확실, 0.8 = 80% 정도 비슷함

    class Meta:
        verbose_name = '식품매핑'
        verbose_name_plural = '식품매핑들'
        unique_together = ['search_keyword', 'mapped_to_food']  # 같은 매핑의 중복저장 방지
    
    def __str__(self):
        return f"{self.search_keyword} → {self.mapped_to_food.name}"