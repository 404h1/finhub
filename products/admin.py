from django.contrib import admin
from .models import DepositProduct, DepositOption

class OptionInline(admin.TabularInline):
    model = DepositOption
    extra = 0

@admin.register(DepositProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('kor_co_nm', 'fin_prdt_nm', 'join_way', 'dcls_month')
    search_fields = ('kor_co_nm', 'fin_prdt_nm')
    inlines = [OptionInline]

admin.site.register(DepositOption)
