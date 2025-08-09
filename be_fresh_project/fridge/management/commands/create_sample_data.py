from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fridge.models import FoodCategory, Food, FridgeItem
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '샘플 데이터 생성'

    def handle(self, *args, **options):
        # 1. 식품 카테고리 생성
        categories = [
            ('채소', '잎채소', 7),
            ('채소', '뿌리채소', 14),
            ('육류', '닭고기', 3),
            ('유제품', '우유류', 5),
            ('과일', '베리류', 5),
        ]
        
        for main_cat, sub_cat, days in categories:
            category, created = FoodCategory.objects.get_or_create(
                name=main_cat,
                subcategory=sub_cat,
                defaults={'default_storage_days': days}
            )
            if created:
                self.stdout.write(f'카테고리 생성: {category}')

        # 2. 식품 생성
        foods_data = [
            ('브로콜리', '채소', '잎채소', True),
            ('닭가슴살', '육류', '닭고기', True),
            ('우유', '유제품', '우유류', True),
            ('당근', '채소', '뿌리채소', True),
            ('블루베리', '과일', '베리류', True),
            ('시금치', '채소', '잎채소', False),
        ]
        
        for food_name, main_cat, sub_cat, is_main in foods_data:
            category = FoodCategory.objects.get(name=main_cat, subcategory=sub_cat)
            food, created = Food.objects.get_or_create(
                name=food_name,
                defaults={'category': category, 'is_main_button': is_main}
            )
            if created:
                self.stdout.write(f'식품 생성: {food}')

        # 3. 테스트 사용자의 냉장고 아이템 생성 (admin 계정이 있다면)
        try:
            user = User.objects.get(username='admin')  # 또는 다른 사용자명
            
            # 샘플 냉장고 아이템들 (다양한 상태로 생성)
            sample_items = [
                ('브로콜리', False, None),  # 일반상품 (7일)
                ('닭가슴살', True, 'today'),  # 할인상품 - 오늘까지 (긴급!)
                ('우유', False, None),  # 일반상품 (5일)
                ('블루베리', True, 'tomorrow'),  # 할인상품 - 내일까지
                ('당근', True, 'day_after_tomorrow'),  # 할인상품 - 모레까지
            ]
            
            for food_name, is_discount, urgency in sample_items:
                food = Food.objects.get(name=food_name)
                item, created = FridgeItem.objects.get_or_create(
                    user=user,
                    food=food,
                    is_discount=is_discount,
                    defaults={'urgency': urgency}
                )
                if created:
                    self.stdout.write(f'냉장고 아이템 생성: {item}')
                    
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('admin 사용자가 없습니다. 슈퍼유저를 먼저 생성하세요.'))

        self.stdout.write(self.style.SUCCESS('샘플 데이터 생성 완료!'))