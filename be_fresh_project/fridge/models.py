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


# 냉장고 아이템 모델
# 사용자가 실제 냉장고에 넣은 개별 식품들을 관리
# 버튼 클릭으로 식품 선택, 할인상품 체크로 간단하게 관리
class FridgeItem(models.Model):
    # 긴급도 선택지 - 할인상품일 때 언제까지 먹어야 하는지 (3일 이내)
    URGENCY_CHOICES = [
        ('today', '오늘'),                    
        ('tomorrow', '내일'),                 
        ('day_after_tomorrow', '모레'),       
    ]
    
    # 누구의 냉장고인지 연결
    # CASCADE: 사용자 삭제 시 해당 사용자의 모든 냉장고 아이템도 함께 삭제
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='사용자'
    )
    
    # 어떤 식품인지 연결 (브로콜리, 닭가슴살 등의 마스터 데이터)
    # 사용자가 메인 화면 버튼을 클릭해서 선택
    # CASCADE: 식품 마스터가 삭제되면 해당 식품을 사용하는 냉장고 아이템도 삭제
    food = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE,
        verbose_name='식품'
    )
    
    # 할인상품 여부를 체크박스로 선택
    # True: 할인상품 → 빨리 먹어야 함, urgency 설정 필요
    # False: 일반상품 → 카테고리의 기본 보관일 사용
    is_discount = models.BooleanField(
        default=False, 
        verbose_name='할인상품'
    )
    
    # 할인상품일 때만 설정하는 긴급도 (오늘/내일/모레 중 선택)
    # 일반상품이면 비어있음 (NULL)
    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        blank=True,          
        null=True,           
        verbose_name='언제까지'
    )
    
    # 해당 냉장고 아이템을 다 먹었거나 버렸을 때 True로 변경
    # 통계나 기록 용도로 사용
    # False: 아직 냉장고에 있음, True: 처리 완료
    is_consumed = models.BooleanField(
        default=False, 
        verbose_name='소비 완료'
    )
    
    # 냉장고에 아이템을 넣은 날짜와 시간
    # auto_now_add=True: 객체 생성 시 자동으로 현재 시간 저장
    # 일반상품의 소진일 계산할 때 기준점으로 사용
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='냉장고 등록일시'
    )

    class Meta:
        verbose_name = '냉장고 아이템'
        verbose_name_plural = '냉장고 아이템들'
        # 최근 등록한 순으로 기본 정렬
        # 실제 위험도 정렬은 View에서 days_remaining 기준으로 동적 처리
        ordering = ['-created_at']  
    
    # 냉장고 아이템을 문자열로 표현할 때의 형식
    # Django Admin이나 디버깅 시 보여지는 내용
    def __str__(self):
        if self.is_discount and self.urgency:
            # 할인상품이고 긴급도가 설정된 경우
            return f"{self.user.username} - {self.food.name} (할인, {self.get_urgency_display()})"
        # 일반상품인 경우 간단하게 표시
        return f"{self.user.username}의 냉장고 - {self.food.name}"
    
    # 남은 일수를 계산하는 속성(property)
    # 할인상품과 일반상품 모두 동일한 기준으로 계산
    # View에서 정렬할 때 이 값을 기준으로 사용
    @property
    def days_remaining(self):
        if self.is_discount and self.urgency:
            # 할인상품이고 긴급도가 설정된 경우 (오늘/내일/모레)
            urgency_days = {
                'today': 0,                    
                'tomorrow': 1,                 
                'day_after_tomorrow': 2,       
            }
            return urgency_days.get(self.urgency, 0)
        else:
            # 일반상품의 경우: 냉장고 등록일 + 카테고리 기본 보관일로 계산
            from datetime import date, timedelta
            purchase_date = self.created_at.date()  
            expiry_date = purchase_date + timedelta(days=self.food.category.default_storage_days)
            return (expiry_date - date.today()).days
    
    # 냉장고 아이템 상태를 문자열로 반환
    # 시각화(색상, 애니메이션 등)할 때 사용
    # 할인상품/일반상품 구분 없이 days_remaining 기준으로 동일하게 처리
    @property 
    def status(self):
        days = self.days_remaining
        if days > 3:
            return "신선"      
        elif days > 1:
            return "주의"      
        elif days >= 0:
            return "위험"      
        else:
            return "폐기"      
    
    # 상태에 따른 색상 반환 (시각화용)
    # days_remaining 기준으로 할인상품/일반상품 동일하게 처리
    @property
    def urgency_color(self):
        status = self.status
        colors = {
            '신선': '#4CAF50',    
            '주의': '#FFC107',    
            '위험': '#FF9800',    
            '폐기': '#F44336'     
        }
        return colors.get(status, '#9E9E9E')