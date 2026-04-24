from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('nickname','age','assets','salary','investment_style','profile_image','bio','favorite_bank','saving_style','interest_stocks')}),
    )
