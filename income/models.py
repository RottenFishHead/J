from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


FREQUENCY_CHOICES = (
    ('WK', 'Weekly'),
    ('BW', 'Bi-weekly'), 
    ('MT', 'Monthly'),
    ('ON', 'Once')
)

#Source is Poker, Ebay, job, etc...
class Source(models.Model):
    name = models.CharField(max_length=75, blank=False, null=False)
    created = models.DateField(default=now)
    
    def __str__(self):
            return self.name

class ReocurringIncomeManager(models.Manager):
    def due_today(self):
        today = now().date()
        return self.filter(day_to_receive=today.day, is_active=True)
    
    def due_this_month(self):
        today = now().date()
        return self.filter(day_to_receive__lte=today.day, is_active=True)

class ReocurringIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Recipient')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    frequency = models.CharField(max_length=3, choices=FREQUENCY_CHOICES, default='MT')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    day_to_receive = models.IntegerField(blank=False, null=False, help_text="Day of month to receive income (1-31)")
    is_active = models.BooleanField(default=True, help_text="Whether this reocurring income is active")
    created = models.DateField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReocurringIncomeManager()
    
    def __str__(self):
        return f"{self.name} - ${self.amount} on day {self.day_to_receive}"

    def create_income_entry(self):
        """Create an actual Income entry from this reocurring income"""
        from datetime import date
        today = date.today()
        
        # Check if we already created an entry for this month
        existing = Income.objects.filter(
            user=self.user,
            source=self.source,
            amount=self.amount,
            created__year=today.year,
            created__month=today.month,
            reocurring_income=self
        ).exists()
        
        if not existing:
            Income.objects.create(
                user=self.user,
                source=self.source,
                amount=self.amount,
                created=today,
                reocurring_income=self
            )
            return True
        return False
    
class Income(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(default=now)
    reocurring_income = models.ForeignKey(ReocurringIncome, on_delete=models.SET_NULL, blank=True, null=True, 
                                       help_text="Link to reocurring income if auto-generated")
 

    def __str__(self):
        return str(self.source)