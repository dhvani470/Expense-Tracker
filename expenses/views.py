from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Expense, Category
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Budget
from decimal import Decimal
import pandas as pd


def home(request):
    return render(request, 'expenses/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form.fields['password2'].label = 'Confirm password'
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        form.fields['password2'].label = 'Confirm password'

    return render(request, 'expenses/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'expenses/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


@login_required
def add_expense(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        payment_method = request.POST.get('payment_method')

        if not all([amount, category_id, date, description, payment_method]):
            messages.error(request, 'Please fill in all fields.')
        else:
            try:
                category = Category.objects.get(id=category_id)

                expense = Expense(
                    user=request.user,
                    amount=amount,
                    category=category,
                    date=date,
                    description=description,
                    payment_method=payment_method,
                )

                expense.full_clean()
                expense.save()

                messages.success(request, 'Expense added successfully!')
                return redirect('dashboard')

            except Category.DoesNotExist:
                messages.error(request, 'Please select a valid category.')
            except Exception:
                messages.error(
                    request,
                    'Please enter valid expense details.'
                )

    return render(request, 'expenses/add_expense.html', {
        'categories': categories,
    })



@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).select_related('category')
    has_any_expenses = Expense.objects.filter(user=request.user).exists()

    category_id = request.GET.get('category', '')
    payment_method = request.GET.get('payment_method', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    search = request.GET.get('search', '').strip()

    if category_id.isdigit():
        expenses = expenses.filter(category_id=category_id)

    valid_methods = [choice[0] for choice in Expense.PAYMENT_METHODS]
    if payment_method in valid_methods:
        expenses = expenses.filter(payment_method=payment_method)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    if search:
        expenses = expenses.filter(description__icontains=search)

    expenses = expenses.order_by('-date', '-id')

    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0

    today = timezone.localdate()
    monthly_spent = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses,
        'total_spent': total_spent,
        'monthly_spent': monthly_spent,
        'categories': Category.objects.all(),
        'payment_methods': Expense.PAYMENT_METHODS,
        'selected_category': category_id,
        'selected_payment_method': payment_method,
        'start_date': start_date,
        'end_date': end_date,
        'search': search,
        'has_any_expenses': has_any_expenses,
    })


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(
        Expense, id=expense_id, user=request.user
    )
    categories = Category.objects.all()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        payment_method = request.POST.get('payment_method')

        if not all([amount, category_id, date, description, payment_method]):
            messages.error(request, 'Please fill in all fields.')
        else:
            try:
                category = Category.objects.get(id=category_id)

                expense.amount = amount
                expense.category = category
                expense.date = date
                expense.description = description
                expense.payment_method = payment_method

                expense.full_clean()
                expense.save()

                messages.success(request, 'Expense updated successfully!')
                return redirect('dashboard')

            except Category.DoesNotExist:
                messages.error(request, 'Please select a valid category.')
            except Exception:
                messages.error(request, 'Please enter valid expense details.')

    return render(request, 'expenses/edit_expense.html', {
        'expense': expense,
        'categories': categories,
    })


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(
        Expense, id=expense_id, user=request.user
    )

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def manage_budget(request):
    today = timezone.localdate()

    budget, created = Budget.objects.get_or_create(
        user=request.user,
        month=today.month,
        year=today.year,
        defaults={'amount': Decimal('0.00')}
    )

    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            new_amount = Decimal(amount)

            if not new_amount.is_finite() or new_amount <= 0:
                raise ValueError

            budget.amount = new_amount
            budget.full_clean()
            budget.save()

            messages.success(request, 'Monthly budget saved!')
            return redirect('manage_budget')

        except (ValueError, TypeError, ArithmeticError):
            messages.error(request, 'Enter a valid budget greater than zero.')
        except Exception:
            messages.error(request, 'Could not save the budget. Please check the amount.')

    monthly_spent = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    remaining = budget.amount - monthly_spent

    return render(request, 'expenses/budget.html', {
        'budget': budget,
        'monthly_spent': monthly_spent,
        'remaining': remaining,
        'current_month': today.strftime('%B %Y'),
    })


@login_required
def expense_charts(request):
    category_data = (
        Expense.objects.filter(user=request.user)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('category__name')
    )

    monthly_data = (
        Expense.objects.filter(user=request.user)
        .values('date__year', 'date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__year', 'date__month')
    )

    category_labels = [item['category__name'] for item in category_data]
    category_totals = [float(item['total']) for item in category_data]

    month_labels = [
        f"{item['date__year']}-{item['date__month']:02d}"
        for item in monthly_data
    ]
    monthly_totals = [float(item['total']) for item in monthly_data]

    return render(request, 'expenses/charts.html', {
        'category_labels': category_labels,
        'category_totals': category_totals,
        'month_labels': month_labels,
        'monthly_totals': monthly_totals,
    })


@login_required
def expense_analysis(request):
    expense_records = Expense.objects.filter(
        user=request.user
    ).select_related('category').values(
        'amount', 'category__name', 'date', 'description'
    )

    df = pd.DataFrame(list(expense_records))

    if df.empty:
        total_spent = 0
        average_expense = 0
        highest_category = "No data yet"
        category_summary = []
        monthly_summary = []
    else:
        df['amount'] = pd.to_numeric(df['amount'])

        total_spent = round(df['amount'].sum(), 2)
        average_expense = round(df['amount'].mean(), 2)

        category_totals = (
            df.groupby('category__name')['amount']
            .sum()
            .sort_values(ascending=False)
        )

        highest_category = category_totals.index[0]

        category_summary = [
            {'category': category, 'total': round(total, 2)}
            for category, total in category_totals.items()
        ]

        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)

        monthly_totals = df.groupby('month')['amount'].sum().sort_index()

        monthly_summary = [
            {'month': month, 'total': round(total, 2)}
            for month, total in monthly_totals.items()
        ]

    return render(request, 'expenses/analysis.html', {
        'total_spent': total_spent,
        'average_expense': average_expense,
        'highest_category': highest_category,
        'category_summary': category_summary,
        'monthly_summary': monthly_summary,
    })


