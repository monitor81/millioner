from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    exchange_rate = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Asset(models.Model):
    ASSET_TYPES = (
        ('currency', 'Currency'),
        ('stock', 'Stock'),
        ('metal', 'Precious Metal'),
    )
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    current_price = models.FloatField()

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

class Portfolio(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)

class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price_at_transaction = models.FloatField()
    is_purchase = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)