from django.shortcuts import redirect, render
from .decorators import group_required
from django.contrib.auth import get_user_model, login, logout, authenticate 
from .forms import SignUpForm, ProfileForm, SignForm,SellerVerificationForm,AddressForm,StoreForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .decorators import user_not_authenticated
from django.contrib.auth.decorators import permission_required
from .models import UserAddress
# Create your views here.

@user_not_authenticated
def SignView(request):
    if request.method == 'GET':
        form = SignForm()
        context = {
            'form': form,
            'tittle': 'AdvanteYouth'
        }
        return render(request, 'accounts/sign.html', context)
        
    if request.method == 'POST':
        form = SignForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('home')  # Replace with the name of your home URL
            else:
                messages.error(request, "you not have accounts.")
        else:
            messages.error(request, "invalid username or password")
        
        return render(request, 'accounts/sign.html', {'form': form})



@group_required('buyer')
def SignOutView(request):
     logout(request)
     return redirect('sign')


@user_not_authenticated
def SignUpView(request):
    if request.method == 'GET':
        form = SignUpForm()
        context = {
            'form': form
        }
        return render (request, 'accounts/signup.html', context)

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
            login(request, user)
            return redirect ('home')
        else: 
            context = {
                'form': form
            }
            return render(request, 'accounts/signup.html', context)

    


@group_required('buyer')
def ProfileView(request, username):
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f"{user_form.username}, your profile has been updated!")
            return redirect ('profile', user_form.username)
        
        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username= username).first()
    if user:
        form = ProfileForm(instance=user)
        context = {
            'form' : form
        }   
        return render (request, 'accounts/profile.html', context)
    
    return redirect('home')


@group_required('buyer')
def seller_verification(request):
    if request.method == 'POST':
        form = SellerVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            verification = form.save(commit=False)
            verification.user_id = request.user
            verification.save()
            
            return redirect('home')
    else:
        form = SellerVerificationForm()
    return render(request, 'accounts/verification.html', {'form': form})




@group_required('buyer')
def AddressView(request):
    if request.method == 'GET':
        form = AddressForm()
        context = {
            'form': form,
        }
        return render (request, 'accounts/useraddress.html',context)
    if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                user_address = form.save(commit=False)
                user_address.UserAddressId = request.user  # Asumsi Anda ingin mengaitkan alamat dengan pengguna yang sedang masuk
                user_address.save()
                return redirect('address_list')
            else:
                context = {'form': form}
                return render(request, 'accounts/useraddress.html', context)

@group_required('buyer')
def list_address(request):
    if request.method == 'GET':
        form = UserAddress.objects.filter(UserAddressId = request.user)

        context = {
            'form': form,
        }
        return render (request, 'accounts/list_address.html',context)


def add_store(request):
    # Periksa apakah pengguna sudah memiliki toko
    if request.user.has_store:
        return redirect('store')  # Redirect jika sudah memiliki toko

    else:
        if request.method == 'POST':
            form = StoreForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.store_seller_id = request.user  # Assign pengguna ke toko
                data.save()
                
                # Set has_store menjadi True setelah toko dibuat
                request.user.has_store = True
                request.user.save()
                
                return redirect('seller_dashboard')
        else:
            form = StoreForm()

    return render(request, 'accounts/store.html', {'form': form})

