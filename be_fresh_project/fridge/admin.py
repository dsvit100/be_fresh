from django.contrib import admin
from .models import FoodCategory, Food

# foodcategory 모델 admin 등록
admin.site.register(FoodCategory)
admin.site.register(Food)