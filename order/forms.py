from django import forms
from .models import ShippingModel,PaymentModel  # Import your ShippingModel here

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingModel  # Replace 'ShippingModel' with your actual shipping model
        fields = ['name', 'address', 'city', 'postal_code', 'country']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentModel  # Replace 'PaymentModel' with your actual payment model
        fields = ['card_number', 'expiry_date', 'cvv']
