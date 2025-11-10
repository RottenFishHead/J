# urls.py
from django.urls import path
from .views import (income_list, income_detail, income_create, income_edit, income_delete, monthly_income_view,
                    reocurring_income_list, reocurring_income_create, reocurring_income_edit, reocurring_income_delete,
                    process_all_reocurring_income, source_create_ajax)

app_name = 'income' 

urlpatterns = [
    path('', income_list, name='income_list'),
    path('<int:pk>/', income_detail, name='income_detail'),
    path('edit/<int:pk>/', income_edit, name='income_edit'),
    path('new/', income_create, name='income_create'),
    path('monthly-income/', monthly_income_view, name='monthly_income'),
    path('delete/<int:pk>/', income_delete, name='income_delete'),
    
    # recurring income URLs
    path('recurring/', reocurring_income_list, name='reocurring_income_list'),
    path('recurring/new/', reocurring_income_create, name='reocurring_income_create'),
    path('recurring/<int:pk>/edit/', reocurring_income_edit, name='reocurring_income_edit'),
    path('recurring/<int:pk>/delete/', reocurring_income_delete, name='reocurring_income_delete'),
    path('process-recurring/', process_all_reocurring_income, name='process_all_reocurring_income'),
    
    # AJAX endpoints
    path('ajax/source/create/', source_create_ajax, name='source_create_ajax'),
]
