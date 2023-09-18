from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from .models import UserAddress,Store


class StoreForm(forms.ModelForm):
    store_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    store_open = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'format': '%H:%M'}))
    store_closed = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'format': '%H:%M'}))
    class Meta:
        model = Store
        fields = [
            'PhoneNumber',
            'email',
            'store_name',
            'store_description',
            'Province',
            'city',
            'district',
            'post_code',
            'store_open',
            'store_closed',
        ]

        def clean_PhoneNumber(self):
            phone_number = self.cleaned_data['PhoneNumber']
            if len(str(phone_number)) >= 10  and len(str(phone_number)) <= 13:  # Contoh validasi sederhana, sesuaikan dengan kebutuhan Anda
                raise forms.ValidationError("Nomor telepon harus terdiri dari 10 digit.")
            return phone_number
        
class SignUpForm (UserCreationForm):
    email = forms.EmailField(help_text='please using valid email address' ,required=True, widget=forms.EmailInput(attrs={'class':'form-control    border-1 ','aria-describedby':'emailHelp','placeholder':'Email'}))
    username = forms.CharField(label='Username' ,required=True, widget=forms.TextInput(attrs={'class':'form-control    border-1 ','placeholder':'Username'}))
    password1 = forms.CharField(label='Password' ,required=True, widget=forms.PasswordInput(attrs={'class':'form-control    border-1 ','placeholder':'Password'}))
    password2 = forms.CharField(label='Confirm Password' ,required=True, widget=forms.PasswordInput(attrs={'class':'form-control    border-1 ','placeholder':'Password verification'}))
    first_name = forms.CharField(label='First Name' ,required=True, widget=forms.TextInput(attrs={'class':'form-control    border-1 ','placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name' ,required=True, widget=forms.TextInput(attrs={'class':'form-control    border-1 ','placeholder':'Last Name'}))
    captcha = ReCaptchaField(widget = ReCaptchaV3(), label = '')
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','username','email','password1','password2']

    def save(self, commit = True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.username = user.username.lower()  # Ubah username menjadi lowercase sebelum disimpan
            user.save()
        return user  

class ProfileForm (forms.ModelForm):
    email = forms.EmailField( label='Email' , widget=forms.EmailInput(attrs={'class':'form-control','id':'InputEmail','aria-describedby':'emailHelp','placeholder':''}),label_suffix='')
    username = forms.CharField(label='Username' ,required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'InputUsername','placeholder':''}),label_suffix='')
    first_name = forms.CharField(label='First Name' ,required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'InputFirstName','placeholder':''}),label_suffix='')
    last_name = forms.CharField(label='Last Name' ,required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'InputLastName','placeholder':''}),label_suffix='')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','username','email','date_of_birth']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

class SignForm(AuthenticationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control  border-1 ', 'placeholder': 'Username or Email'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control  border-1 ', 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(label='Remember Me', required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV3(), label='')

    def __init__(self, *args, **kwargs):
        super(SignForm, self).__init__(*args, **kwargs)

from django import forms
from .models import SellerVerification

class SellerVerificationForm(forms.ModelForm):
    class Meta:
        model = SellerVerification
        fields = ['verification_image']

class AddressForm (forms.ModelForm):
    Province = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'provinsi'}))
    city  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'kota'}))
    district  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'kecamatan'}))
    pos_code  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'kodePos'}))
    street  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control','id':'alamat'}))
    address_for = forms.ChoiceField(
        choices=[('kantor', 'Kantor'), ('rumah', 'Rumah')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = UserAddress
        fields = ['PhoneNumber','detail','Province','city','district','pos_code','street','address_for','Main_address']




