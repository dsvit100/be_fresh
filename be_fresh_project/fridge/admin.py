from django.contrib import admin
from .models import FoodCategory, Food, FoodMapping, FridgeItem

# foodcategory 모델 admin 등록
admin.site.register(FoodCategory)
admin.site.register(Food)
admin.site.register(FoodMapping)
admin.site.register(FridgeItem)