from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import FridgeService, FoodService, NotificationService


@login_required
def home(request):
    """
    메인 냉장고 화면
    - 사용자의 냉장고 아이템들을 위험도순으로 표시
    - 메인 버튼으로 표시할 식품들 제공
    - 긴급 알림 메시지 표시
    """
    # services.py의 비즈니스 로직 사용
    fridge_items = FridgeService.get_sorted_fridge_items(request.user)
    main_foods = FoodService.get_main_foods()
    urgent_notifications = NotificationService.get_urgent_notifications(request.user)
    expiring_soon_count = FridgeService.get_expiring_soon_count(request.user)
    
    context = {
        'fridge_items': fridge_items,
        'main_foods': main_foods,
        'urgent_notifications': urgent_notifications,
        'expiring_soon_count': expiring_soon_count,
    }
    
    return render(request, 'fridge/home.html', context)