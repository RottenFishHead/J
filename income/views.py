# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import IncomeForm, reocurringIncomeForm
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Income, reocurringIncome
from expenses.models import Expense, FixedExpense
from django.contrib import messages
from datetime import datetime, date

@login_required
def index(request):
    # Calculate the start and end dates for the current month
    today = datetime.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month, today.day)

    # Filter incomes for the current user and current month
    monthly_incomes = Income.objects.filter(created__range=(start_date, end_date))
    total_monthly_income = monthly_incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter regular expenses for the current user and current month
    monthly_expenses = Expense.objects.filter(created__range=(start_date, end_date))
    total_monthly_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter fixed expenses for the current user
    # Only show fixed expenses with day_to_pay less than today
    fixed_expenses = FixedExpense.objects.due_this_month()
    total_fixed_expenses = fixed_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate total expenses
    total_all_expenses = float(f"{(total_monthly_expenses + total_fixed_expenses):.2f}")

    # Truncate to two decimal places
    total_monthly_income = float(f"{total_monthly_income:.2f}")
    total_monthly_expenses = float(f"{total_monthly_expenses:.2f}")
    total_fixed_expenses = float(f"{total_fixed_expenses:.2f}")
    net_income = total_monthly_income - total_all_expenses

    # Calculate percentages for expenses
    monthly_expenses_percentage = (total_monthly_expenses / total_all_expenses * 100) if total_all_expenses > 0 else 0
    fixed_expenses_percentage = (total_fixed_expenses / total_all_expenses * 100) if total_all_expenses > 0 else 0

    context = {
        'monthly_incomes': monthly_incomes,
        'total_monthly_income': total_monthly_income,
        'monthly_expenses': monthly_expenses,
        'total_monthly_expenses': total_monthly_expenses,
        'fixed_expenses': fixed_expenses,
        'total_fixed_expenses': total_fixed_expenses,
        'total_all_expenses': total_all_expenses,
        'net_income': net_income,
        'monthly_expenses_percentage': monthly_expenses_percentage,
        'fixed_expenses_percentage': fixed_expenses_percentage,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'income/index.html', context)


@login_required
def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income/income_list.html', {'incomes': incomes})

def income_detail(request, pk):
    income = get_object_or_404(Income, pk=pk)
    return render(request, 'income/income_detail.html', {'income': income})

def income_create(request):
    # Check for and create any due recurring income entries
    process_reocurring_income(request.user)
    
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Assuming you are using authentication
            income.save()
            return redirect('income:income_list')
    else:
        form = IncomeForm()
    return render(request, 'income/income_form.html', {'form': form})

def process_reocurring_income(user):
    """Process all due recurring income for a user"""
    due_incomes = reocurringIncome.objects.due_today().filter(user=user)
    created_count = 0
    
    for reocurring_income in due_incomes:
        if reocurring_income.create_income_entry():
            created_count += 1
    
    return created_count

@login_required
def reocurring_income_list(request):
    reocurring_incomes = reocurringIncome.objects.filter(user=request.user)
    return render(request, 'income/reocurring_income_list.html', {'reocurring_incomes': reocurring_incomes})

@login_required
def reocurring_income_create(request):
    if request.method == 'POST':
        form = reocurringIncomeForm(request.POST)
        if form.is_valid():
            reocurring_income = form.save(commit=False)
            reocurring_income.user = request.user
            reocurring_income.save()
            messages.success(request, 'recurring income created successfully!')
            return redirect('income:reocurring_income_list')
    else:
        form = reocurringIncomeForm()
    return render(request, 'income/reocurring_income_form.html', {'form': form, 'action': 'Create'})

@login_required
def reocurring_income_edit(request, pk):
    reocurring_income = get_object_or_404(reocurringIncome, pk=pk, user=request.user)
    if request.method == 'POST':
        form = reocurringIncomeForm(request.POST, instance=reocurring_income)
        if form.is_valid():
            form.save()
            messages.success(request, 'recurring income updated successfully!')
            return redirect('income:reocurring_income_list')
    else:
        form = reocurringIncomeForm(instance=reocurring_income)
    return render(request, 'income/reocurring_income_form.html', {'form': form, 'action': 'Edit'})

@login_required
def reocurring_income_delete(request, pk):
    reocurring_income = get_object_or_404(reocurringIncome, pk=pk, user=request.user)
    if request.method == 'POST':
        reocurring_income.delete()
        messages.success(request, 'recurring income deleted successfully!')
        return redirect('income:reocurring_income_list')
    return render(request, 'income/reocurring_income_confirm_delete.html', {'reocurring_income': reocurring_income})

@login_required
def process_all_reocurring_income(request):
    """Manually trigger processing of all recurring income for the current user"""
    created_count = process_reocurring_income(request.user)
    if created_count > 0:
        messages.success(request, f'Created {created_count} new income entries from recurring income.')
    else:
        messages.info(request, 'No new recurring income entries were due.')
    return redirect('income:income_list')

def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Assuming you are using authentication
            income.save()
            return redirect('income:income_detail', pk=income.pk)
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income/income_form.html', {'form': form})

def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return redirect('income:income_list')


@login_required
def monthly_income_view(request):

    # Calculate the start and end dates for the current month
    today = datetime.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month, today.day)

    # Filter incomes for the current user and current month
    monthly_incomes = Income.objects.filter(created__range=(start_date, end_date))
    total_monthly_income = monthly_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    # Filter expenses for the current user and current month
    monthly_expenses = Expense.objects.filter(created__range=(start_date, end_date))
    total_monthly_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter fixed_expenses for the current user
    fixed_expenses = FixedExpense.objects.all()
    total_fixed_expenses = fixed_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_all_expenses = total_fixed_expenses + total_monthly_income

    # Calculate the net income
    net_income = total_monthly_income - (total_monthly_expenses + total_fixed_expenses)

    # Truncate to two decimal places
    total_monthly_income = float(f"{total_monthly_income:.2f}")
    total_monthly_expenses = float(f"{total_monthly_expenses:.2f}")
    total_fixed_expenses = float(f"{total_fixed_expenses:.2f}")
    total_all_expenses = float(f"{total_all_expenses:.2f}")
    net_income = float(f"{net_income:.2f}")

    context = {
        'monthly_incomes': monthly_incomes,
        'total_monthly_income': total_monthly_income,
        'monthly_expenses': monthly_expenses,
        'total_monthly_expenses': total_monthly_expenses,
        'fixed_expenses': fixed_expenses,
        'total_fixed_expenses': total_fixed_expenses,
        'net_income': net_income,
        'start_date': start_date,
        'end_date': end_date,
        'total_all_expenses': total_all_expenses
    }

    return render(request, 'income/monthly_income.html', context)

@login_required
def source_create_ajax(request):
    """AJAX endpoint to create a new income source"""
    import json
    from django.http import JsonResponse
    from .models import Source
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source_name = data.get('name', '').strip()
            
            if not source_name:
                return JsonResponse({'success': False, 'error': 'Source name is required'})
            
            # Check if source already exists
            existing_source = Source.objects.filter(name__iexact=source_name).first()
            if existing_source:
                return JsonResponse({
                    'success': True,
                    'source': {
                        'id': existing_source.id,
                        'name': existing_source.name
                    }
                })
            
            # Create new source
            source = Source.objects.create(name=source_name)
            return JsonResponse({
                'success': True,
                'source': {
                    'id': source.id,
                    'name': source.name
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
