from django import forms
from .models import product
from multiupload.fields import MultiFileField

class ProductForm(forms.ModelForm):
    warna = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ukuran = forms.CharField(required=False, widget=forms.TextInput())
    rasa = forms.CharField(required=False, widget=forms.TextInput())
    category = forms.ChoiceField(widget=forms.Select(), choices=product.CATEGORY_CHOICES)
    image_product = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5,)

    class Meta:
        model = product
        fields = ['name_product', 'description', 'category', 'warna', 'ukuran', 'rasa', 'price']


    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        super().__init__(*args, **kwargs)

        for index in range(int(extra_fields)):
            self.fields[f'extra_field_{index}'] = forms.CharField()

    def extra_fields(self):
        for field_name in self.fields:
            if field_name.startswith('extra_field_'):
                yield self[field_name]