from django import forms
from .models import Income, RecurringIncome

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['user', 'source', 'amount', 'created']

class RecurringIncomeForm(forms.ModelForm):
    class Meta:
        model = RecurringIncome
        fields = ['source', 'name', 'frequency', 'amount', 'day_to_receive', 'is_active']
        widgets = {
            'day_to_receive': forms.NumberInput(attrs={'min': 1, 'max': 31}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }