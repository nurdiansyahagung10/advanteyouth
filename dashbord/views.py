from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import SellerVerification
from django.contrib.auth.decorators import permission_required
from accounts.models import Store
from products.forms import ProductForm
from products.models import product
# Create your views here.
@permission_required('accounts.change_seller_verification')
def approve_verification(request, pk):
    verification = get_object_or_404(SellerVerification, pk=pk)
    verification.approve_verification()
    return redirect('verification_list')


@permission_required('accounts.change_seller_verification')
def cancel_verification(request, pk):
    verification = get_object_or_404(SellerVerification, pk=pk)
    verification.cancel_verification()
    return redirect('verification_list')


@permission_required('accounts.view_seller_verification')
def verification_list(request):
    pending_verifications = SellerVerification.objects.filter(verification_status='pending')
    approved_verifications = SellerVerification.objects.filter(verification_status='approved')

    context = {
        'pending_verifications': pending_verifications,
        'approved_verifications': approved_verifications,    
    }
    return render(request, 'dashbord/verification_list.html', context)
        

def seller_dashboard(request):
    # Pastikan pengguna sudah login dan memiliki toko
    if request.user.is_authenticated and hasattr(request.user, 'store'):
        store = request.user.store
        products = product.objects.filter(store_id=store)

        return render(request, 'dashbord/seller_dashbord.html', {
            'store': store,
            'products': products,
        })
    else:
        # Redirect pengguna yang belum memiliki toko atau belum login ke halaman lain
        return redirect('home')  # Ganti 'home' dengan URL halaman yang sesuai
