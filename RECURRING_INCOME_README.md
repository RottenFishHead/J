# Automatic Income Entries Feature

This feature allows you to set up reocurring income entries that will automatically create income records on specified days of the month.

## How It Works

1. **Set Up reocurring Income**: Create reocurring income entries specifying:
   - Source (salary, freelance, etc.)
   - Name (description)
   - Amount
   - Day of month to receive (1-31)
   - Frequency (Weekly, Bi-weekly, Monthly, Once)
   - Active status

2. **Automatic Processing**: Income entries are automatically created when:
   - You visit the income creation page
   - You manually trigger processing
   - You run the management command (for automation)

## Usage

### Web Interface

1. Go to Income List page
2. Click "Manage reocurring Income" to set up reocurring entries
3. Click "Process Due Income" to manually trigger processing
4. View auto-generated entries (marked with "Auto-Generated" badge)

### Management Command

For automation (cron jobs, scheduled tasks):

```bash
# Process all users' reocurring income
python manage.py process_reocurring_income

# Process specific user only
python manage.py process_reocurring_income --user-id 1

# Dry run (see what would be processed without creating entries)
python manage.py process_reocurring_income --dry-run
```

## Features

- **Smart Duplicate Prevention**: Won't create duplicate entries for the same month
- **User-Specific**: Each user manages their own reocurring income
- **Flexible Scheduling**: Support for different frequencies
- **Manual Override**: Can disable/enable reocurring income entries
- **Audit Trail**: Tracks which entries were auto-generated vs manual

## Integration

The automatic processing is integrated into the `income_create` view, so reocurring income is processed whenever a user visits the income creation page. This ensures timely processing without requiring separate automation setup.

## Database Changes

- New `reocurringIncome` model
- `Income.reocurring_income` field links auto-generated entries back to their source
- Admin interface updated to manage reocurring income

## Templates

- `reocurring_income_list.html` - Manage reocurring income entries
- `reocurring_income_form.html` - Create/edit reocurring income
- `reocurring_income_confirm_delete.html` - Delete confirmation
- Updated `income_list.html` with reocurring income management links