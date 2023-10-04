from django import forms
from .models import ShippingModel  # Import your ShippingModel here

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingModel  # Replace 'ShippingModel' with your actual shipping model
        fields = ['address']


