"""
비즈니스 로직을 담당하는 서비스 레이어
- 복잡한 데이터 처리 로직
- 여러 모델을 조합하는 로직
- 외부 API 연동 로직
- 재사용 가능한 비즈니스 함수들
"""

from typing import List
from django.contrib.auth.models import User
from django.db.models import QuerySet
from .models import FridgeItem, Food, FoodMapping, FoodCategory


class FridgeService:
    """냉장고 관련 비즈니스 로직"""
    
    @staticmethod
    def get_sorted_fridge_items(user: User) -> List[FridgeItem]:
        """
        사용자의 냉장고 아이템을 위험도순으로 정렬해서 반환
        - 폐기 위험이 높은 순서로 정렬
        - 소비 완료된 아이템은 제외
        """
        fridge_items = FridgeItem.objects.filter(
            user=user, 
            is_consumed=False
        ).select_related('food', 'food__category')  # 성능 최적화
        
        return sorted(fridge_items, key=lambda item: item.days_remaining)
    
    @staticmethod
    def get_items_by_status(user: User) -> dict:
        """
        상태별로 냉장고 아이템들을 분류해서 반환
        반환 형태: {'신선': [...], '주의': [...], '위험': [...], '폐기': [...]}
        """
        items = FridgeService.get_sorted_fridge_items(user)
        status_groups = {'신선': [], '주의': [], '위험': [], '폐기': []}
        
        for item in items:
            status_groups[item.status].append(item)
        
        return status_groups
    
    @staticmethod
    def get_expiring_soon_count(user: User, days: int = 2) -> int:
        """지정된 일수 이내에 만료되는 아이템 개수 반환"""
        items = FridgeService.get_sorted_fridge_items(user)
        return len([item for item in items if item.days_remaining <= days])


class FoodService:
    """식품 관련 비즈니스 로직"""
    
    @staticmethod
    def get_main_foods() -> QuerySet[Food]:
        """메인 화면에 버튼으로 표시할 식품들 반환"""
        return Food.objects.filter(is_main_button=True).select_related('category')
    
    @staticmethod
    def search_food_by_keyword(keyword: str) -> Food:
        """
        키워드로 식품 검색
        1. 직접 일치하는 식품명 찾기
        2. 없으면 FoodMapping에서 매핑된 식품 찾기
        3. 둘 다 없으면 None 반환
        """
        # 1. 직접 식품명으로 검색
        try:
            return Food.objects.get(name__icontains=keyword)
        except Food.DoesNotExist:
            pass
        
        # 2. 매핑 테이블에서 검색
        try:
            mapping = FoodMapping.objects.get(search_keyword__icontains=keyword)
            return mapping.mapped_to_food
        except FoodMapping.DoesNotExist:
            return None
    
    @staticmethod
    def get_popular_foods(limit: int = 10) -> QuerySet[Food]:
        """인기 식품 반환 (냉장고 등록 횟수 기준)"""
        from django.db.models import Count
        
        return Food.objects.annotate(
            usage_count=Count('fridgeitem')
        ).order_by('-usage_count')[:limit]


class StatisticsService:
    """통계 관련 비즈니스 로직"""
    
    @staticmethod
    def get_user_waste_statistics(user: User) -> dict:
        """
        사용자의 음식물 쓰레기 통계 반환
        - 총 폐기한 아이템 수
        - 카테고리별 폐기 현황
        - 최근 30일 폐기 트렌드
        """
        # 향후 구현 예정
        # 폐기된 아이템 추적 기능이 추가되면 여기서 통계 계산
        return {
            'total_wasted': 0,
            'category_waste': {},
            'monthly_trend': []
        }
    
    @staticmethod
    def get_saving_statistics(user: User) -> dict:
        """
        사용자의 절약 통계 반환
        - 적절히 소비한 아이템 수
        - 예상 절약 금액 등
        """
        # 향후 구현 예정
        return {
            'items_saved': 0,
            'money_saved': 0
        }


class NotificationService:
    """알림 관련 비즈니스 로직"""
    
    @staticmethod
    def get_urgent_notifications(user: User) -> List[str]:
        """
        긴급 알림 메시지 생성
        - 오늘/내일 폐기 예정 아이템들에 대한 알림
        """
        try:
            items = FridgeService.get_sorted_fridge_items(user)
            notifications = []
            
            for item in items:
                days = item.days_remaining
                food_name = item.food.name
                
                if days < 0:
                    notifications.append(f"🚨 {food_name}이(가) {abs(days)}일 전에 만료되었습니다!")
                elif days == 0:
                    notifications.append(f"🚨 {food_name}을(를) 오늘까지 드셔야 합니다!")
                elif days == 1:
                    notifications.append(f"⚠️ {food_name}을(를) 내일까지 드세요!")
                elif days == 2:
                    notifications.append(f"📌 {food_name}이(가) 모레까지입니다.")
            
            return notifications[:5]  # 최대 5개까지만
            
        except Exception as e:
            # 디버깅용: 오류 발생 시 빈 리스트 반환
            print(f"알림 생성 오류: {e}")
            return []
