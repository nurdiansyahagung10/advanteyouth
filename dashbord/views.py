from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import SellerVerification
from accounts.decorators import group_required,admin_required
from products.forms import ProductForm
from products.models import product
from order.models import Order,Cart,CartItem

# Create your views here.
@admin_required('admin')
def approve_verification(request, pk):
    verification = get_object_or_404(SellerVerification, pk=pk)
    verification.approve_verification()
    return redirect('verification_list')


@admin_required('admin')
def cancel_verification(request, pk):
    verification = get_object_or_404(SellerVerification, pk=pk)
    verification.cancel_verification()
    return redirect('verification_list')


@admin_required('admin')
def verification_list(request):
    pending_verifications = SellerVerification.objects.filter(verification_status='pending')
    approved_verifications = SellerVerification.objects.filter(verification_status='approved')

    context = {
        'pending_verifications': pending_verifications,
        'approved_verifications': approved_verifications,    
    }
    return render(request, 'dashbord/verification_list.html', context)
        
@group_required('seller')
def seller_dashboard(request):
    # Pastikan pengguna sudah login dan memiliki toko
    if request.user.is_authenticated and hasattr(request.user, 'store'):
        store = request.user.store
        products = product.objects.filter(store_id=store)

        # Dapatkan semua item keranjang yang berisi produk dari penjual ini
        seller_cart_items = CartItem.objects.filter(product_id__in=products)

        # Dapatkan semua pesanan yang berisi item keranjang dari penjual ini
        seller_orders = Order.objects.filter(Cart__items__in=seller_cart_items).distinct()

        return render(request, 'dashbord/seller_dashbord.html', {
            'store': store,
            'orders': seller_orders,
            'products': products,
        })
    else:
        # Redirect pengguna yang belum memiliki toko atau belum login ke halaman lain
        return redirect('home')

@group_required('seller')
def approve_order(request, order_id):
        order = Order.objects.get(id=order_id)
        order.approved_by_seller = True
        order.status = 'menunggu pembayaran'
        order.save()
        return redirect('seller_dashboard')