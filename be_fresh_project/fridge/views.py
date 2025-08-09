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
    - 폐기 임박 아이템과 이미 폐기해야 하는 아이템을 분리해서 카운트
    """
    # services.py의 비즈니스 로직 사용
    fridge_items = FridgeService.get_sorted_fridge_items(request.user)
    main_foods = FoodService.get_main_foods()
    urgent_notifications = NotificationService.get_urgent_notifications(request.user)
    
    # 폐기 임박 아이템 개수 (이미 폐기 대상은 제외)
    expiring_soon_count = FridgeService.get_expiring_soon_count(request.user)
    
    # 이미 폐기해야 하는 아이템 개수 (새로 추가)
    expired_count = FridgeService.get_expired_count(request.user)
    
    context = {
        'fridge_items': fridge_items,
        'main_foods': main_foods,
        'urgent_notifications': urgent_notifications,
        'expiring_soon_count': expiring_soon_count,
        'expired_count': expired_count,  # 새로 추가된 컨텍스트
    }
    
    return render(request, 'fridge/home.html', context)