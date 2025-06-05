from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Portfolio, Transaction, Asset, Currency
from django.contrib.auth import get_user_model
from django.db import models 
from django.contrib.auth import login
from collections import defaultdict
from django.utils.timezone import localtime
from django.db.models import F
import json
from .models import Account, Portfolio, Transaction
from django.contrib.auth import logout
from django.shortcuts import redirect

from .forms import CustomUserCreationForm

@login_required
# def dashboard(request):
#     accounts = Account.objects.filter(user=request.user)
#     portfolio = Portfolio.objects.filter(user=request.user)
#     transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
#     leaderboard = (
#         Portfolio.objects
#         .values('user__username')
#         .annotate(total=models.Sum(models.F('quantity') * models.F('asset__current_price')))
#         .order_by('-total')[:10]
#     )
#     return render(request, 'dashboard.html', {
#         'accounts': accounts,
#         'portfolio': portfolio,
#         'transactions': transactions,
#         'leaderboard': leaderboard,
#     })

def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    portfolio = Portfolio.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('timestamp')  # по возрастанию!

    # История изменения стоимости портфеля
    portfolio_history = defaultdict(float)

    for t in transactions:
        date_str = localtime(t.timestamp).strftime("%Y-%m-%d")
        value = t.quantity * t.price_at_transaction
        if t.is_purchase:
            portfolio_history[date_str] += value
        else:
            portfolio_history[date_str] -= value

    # Накопительный подсчёт по датам
    sorted_dates = sorted(portfolio_history.keys())
    cumulative = 0
    cumulative_values = []
    for date in sorted_dates:
        cumulative += portfolio_history[date]
        cumulative_values.append(round(cumulative, 2))  # округлим до 2 знаков

    leaderboard = (
        Portfolio.objects
        .values('user__username')
        .annotate(total=models.Sum(F('quantity') * F('asset__current_price')))
        .order_by('-total')[:10]
    )

    return render(request, 'dashboard.html', {
        'accounts': accounts,
        'portfolio': portfolio,
        'transactions': transactions,
        'leaderboard': leaderboard,
        'portfolio_dates': json.dumps(sorted_dates),
        'portfolio_values': json.dumps(cumulative_values),
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # или куда хочешь перенаправлять