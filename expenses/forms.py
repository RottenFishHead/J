from django import forms
from .models import Expense, FixedExpense, Budget, Payment, Savings, Debt

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'category', 'name', 'amount', 'created']
        # Optionally, you can customize the widgets or add additional validation here

    # You can add custom validation methods or override default behavior here if needed
    
class FixedExpenseForm(forms.ModelForm):
    class Meta:
        model = FixedExpense
        fields = '__all__'


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'description']
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['debt', 'savings', 'fixed_expense', 'amount_paid']

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['name', 'description', 'goal']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'goal': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['name', 'description', 'owed', 'due_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'owed': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'due_by': forms.DateInput(attrs={'type': 'date'}),
        }