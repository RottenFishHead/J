from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from income.models import ReocurringIncome
from datetime import date


class Command(BaseCommand):
    help = 'Process all due reocurring income entries for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Process reocurring income for a specific user ID only',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually creating entries',
        )

    def handle(self, *args, **options):
        today = date.today()
        self.stdout.write(f'Processing reocurring income for {today}...')
        
        # Filter users if specific user ID provided
        if options['user_id']:
            users = User.objects.filter(id=options['user_id'])
            if not users.exists():
                self.stdout.write(
                    self.style.ERROR(f'User with ID {options["user_id"]} not found')
                )
                return
        else:
            users = User.objects.all()

        total_created = 0
        
        for user in users:
            # Get all due reocurring income for this user
            due_incomes = ReocurringIncome.objects.due_today().filter(user=user)
            user_created = 0
            
            for Reocurring_income in due_incomes:
                if options['dry_run']:
                    # Check if entry would be created
                    from income.models import Income
                    existing = Income.objects.filter(
                        user=Reocurring_income.user,
                        source=Reocurring_income.source,
                        amount=Reocurring_income.amount,
                        created__year=today.year,
                        created__month=today.month,
                        reocurring_income=Reocurring_income
                    ).exists()
                    
                    if not existing:
                        self.stdout.write(
                            f'  [DRY RUN] Would create: {Reocurring_income.name} - ${Reocurring_income.amount} for {user.username}'
                        )
                        user_created += 1
                else:
                    # Actually create the entry
                    if Reocurring_income.create_income_entry():
                        self.stdout.write(
                            f'  Created: {Reocurring_income.name} - ${Reocurring_income.amount} for {user.username}'
                        )
                        user_created += 1
                    else:
                        self.stdout.write(
                            f'  Skipped (already exists): {Reocurring_income.name} for {user.username}'
                        )
            
            if user_created > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'User {user.username}: {user_created} income entries {"would be " if options["dry_run"] else ""}created'
                    )
                )
            
            total_created += user_created
        
        if total_created > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Total: {total_created} income entries {"would be " if options["dry_run"] else ""}processed'
                )
            )
        else:
            self.stdout.write('No Reocurring income entries were due for processing.')