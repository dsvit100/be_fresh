from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FridgeItem, Food

# 메인 냉장고 화면을 보여주는 뷰
# @login_required: 로그인한 사용자만 접근 가능 (로그인 안 하면 login 페이지로 리다이렉트)

@login_required
def home(request):
    # 현재 로그인한 사용자의 냉장고 아이템들만 가져오기
    # is_consumed=False: 아직 먹지 않은 것들만 (먹은 건 제외)
    fridge_items = FridgeItem.objects.filter(
        user=request.user, 
        is_consumed=False
    )
    
    # 냉장고 아이템들을 위험도 순으로 정렬
    # days_remaining 값이 낮을수록 임박 (0일 = 오늘까지, 1일 = 내일까지...)
    # 할인상품/일반상품 구분 없이 동일한 기준으로 정렬
    sorted_items = sorted(fridge_items, key=lambda item: item.days_remaining)
    
    # 메인 화면에 버튼으로 표시할 식품들 가져오기
    # is_main_button=True인 식품들만 (브로콜리, 닭가슴살, 우유 등)
    main_foods = Food.objects.filter(is_main_button=True)
    
    # 템플릿에 전달할 데이터들을 딕셔너리로 준비
    context = {
        'fridge_items': sorted_items,  # 위험도 순으로 정렬된 냉장고 아이템들
        'main_foods': main_foods,      # 메인 버튼으로 표시할 식품들
    }
    
    # fridge/home.html 템플릿을 렌더링하면서 context 데이터 전달
    return render(request, 'fridge/home.html', context)