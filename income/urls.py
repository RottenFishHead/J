# urls.py
from django.urls import path
from .views import (income_list, income_detail, income_create, income_edit, income_delete, monthly_income_view,
                    recurring_income_list, recurring_income_create, recurring_income_edit, recurring_income_delete,
                    process_all_recurring_income, source_create_ajax)

app_name = 'income' 

urlpatterns = [
    path('', income_list, name='income_list'),
    path('<int:pk>/', income_detail, name='income_detail'),
    path('edit/<int:pk>/', income_edit, name='income_edit'),
    path('new/', income_create, name='income_create'),
    path('monthly-income/', monthly_income_view, name='monthly_income'),
    path('delete/<int:pk>/', income_delete, name='income_delete'),
    
    # Recurring income URLs
    path('recurring/', recurring_income_list, name='recurring_income_list'),
    path('recurring/new/', recurring_income_create, name='recurring_income_create'),
    path('recurring/<int:pk>/edit/', recurring_income_edit, name='recurring_income_edit'),
    path('recurring/<int:pk>/delete/', recurring_income_delete, name='recurring_income_delete'),
    path('process-recurring/', process_all_recurring_income, name='process_all_recurring_income'),
    
    # AJAX endpoints
    path('ajax/source/create/', source_create_ajax, name='source_create_ajax'),
]
