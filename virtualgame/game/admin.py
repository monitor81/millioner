from django.contrib import admin
from .models import User, Currency, Asset, Account, Portfolio, Transaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_active')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'exchange_rate')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'current_price')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'quantity')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'quantity', 'is_purchase', 'timestamp')