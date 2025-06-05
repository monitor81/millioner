from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Transaction, Asset

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['asset', 'quantity', 'is_purchase']
        labels = {
            'asset': 'Актив',
            'quantity': 'Количество',
            'is_purchase': 'Тип сделки (покупка — галочка)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()