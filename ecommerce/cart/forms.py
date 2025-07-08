from django import forms
from cart.models import Order


class OrderForm(forms.ModelForm):
    payment_choices = [
        ('razorpay', 'Razorpay'),
        ('cod', 'COD'),
    ]
    payment_method = forms.ChoiceField(choices=payment_choices, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['address', 'phone_number', 'payment_method']
