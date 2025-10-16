# yourapp/admin.py
from django.contrib import admin
from .models import Income, Source, RecurringIncome

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'user', 'source', 'created', 'recurring_income')
    search_fields = ('amount', 'user__username', 'source__name')
    list_filter = ('source', 'user', 'created', 'recurring_income')
    date_hierarchy = 'created'

@admin.register(RecurringIncome)
class RecurringIncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'source', 'amount', 'day_to_receive', 'frequency', 'is_active')
    search_fields = ('name', 'user__username', 'source__name')
    list_filter = ('source', 'user', 'frequency', 'is_active', 'created')
    date_hierarchy = 'created'

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


admin.site.register(Source, SourceAdmin)