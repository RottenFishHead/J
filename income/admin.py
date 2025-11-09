# yourapp/admin.py
from django.contrib import admin
from .models import Income, Source, reocurringIncome

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'user', 'source', 'created', 'reocurring_income')
    search_fields = ('amount', 'user__username', 'source__name')
    list_filter = ('source', 'user', 'created', 'reocurring_income')
    date_hierarchy = 'created'

@admin.register(reocurringIncome)
class reocurringIncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'source', 'amount', 'day_to_receive', 'frequency', 'is_active')
    search_fields = ('name', 'user__username', 'source__name')
    list_filter = ('source', 'user', 'frequency', 'is_active', 'created')
    date_hierarchy = 'created'

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


admin.site.register(Source, SourceAdmin)