# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import cartmodel  # Pastikan Anda mengimpor model cart yang sesuai
from products.models import product  # Pastikan Anda mengimpor model product yang sesuai
from django.http import HttpResponseRedirect

from decimal import Decimal  # Import Decimal


# ... kode lainnya ...

def checkout(request):
    user = request.user
    cartitem = cartmodel.objects.filter(cart_id=user)
    
    # Membuat daftar produk yang terkait dengan setiap item dalam keranjang belanja
    products = []
    for cart_item in cartitem:
        product_data = {
            'product': cart_item.cart_product_id,
            'quantity': cart_item.cart_quantity,
            'total_harga': cart_item.cart_total_harga,
        }
        products.append(product_data)

    total_harga = sum(item['total_harga'] for item in products)
    
    # Jika pengguna mengirimkan pesanan
    if request.method == 'POST':
        # Buat pesanan dan tambahkan produk yang dipesan ke dalamnya
        order = cartmodel.objects.create(user=user, total_harga=total_harga)
        for product_data in products:
            cartmodel.objects.create(
                order=order,
                product=product_data['product'],
                quantity=product_data['quantity'],
                total_harga=product_data['total_harga'],
            )
        
        # Hapus item keranjang belanja pengguna
        cartitem.delete()
        
        # Redirect pengguna ke halaman terima kasih atau halaman lain yang sesuai
        return redirect('thank_you')
    
    context = {
        'cartitem': cartitem,
        'total_harga': total_harga,
        'products': products,
    }
    
    return render(request, 'order/cart.html', context)


def tambah_cart(request, product_id):
    # Cek apakah ada entri keranjang yang sesuai dengan produk dan pengguna saat ini
    product_instance = get_object_or_404(product, id=product_id)
    cart_item, created = cartmodel.objects.get_or_create(
        cart_id=request.user,
        cart_product_id=product_instance,
        defaults={
            'cart_quantity': 1,
            'cart_total_harga': Decimal(product_instance.price),  # Konversi harga ke Decimal
        }
    )

    # Jika entri keranjang sudah ada, tambahkan satu unit ke jumlahnya
    if not created:
        cart_item.cart_quantity += 1
        cart_item.cart_total_harga += Decimal(product_instance.price)  # Konversi harga ke Decimal
        cart_item.save()

    # Ambil URL referer (halaman sebelumnya)
    referer = request.META.get('HTTP_REFERER', None)

    # Jika URL referer ada, arahkan pengguna kembali ke halaman tersebut
    if referer:
        return HttpResponseRedirect(referer)
    else:
        # Jika tidak ada URL referer, Anda dapat mengarahkan pengguna ke halaman keranjang atau halaman lain yang sesuai
        return redirect('cart')  # Redirect ke halaman keranjang atau halaman lain yang sesuai


from .models import cartmodel, OrderItem, Order
# ...

def cart(request):
    user = request.user
    try:
        cart = cartmodel.objects.get(cart_id=user)
        order_items = OrderItem.objects.filter(cartmodel=cart)

        total_harga = sum(item.subtotal() for item in order_items)

        context = {
            'order_items': order_items,
            'total_harga': total_harga,
        }

        return render(request, 'order/cart.html', context)

    except cartmodel.DoesNotExist:
        # Handle jika keranjang belanja pengguna tidak ditemukan
        # Anda bisa menambahkan pesan atau tindakan lain sesuai kebutuhan
        return render(request, 'order/empty_cart.html')  # Gantilah dengan template yang sesuai


def hapus_item(request, cart_item_id):
    # Cari item keranjang belanja berdasarkan cart_item_id
    try:
        cart_item = cartmodel.objects.get(cart_product_id = cart_item_id)

        # Pastikan item milik pengguna yang sedang masuk
        if cart_item.cart_id == request.user:
            # Hapus item dari keranjang belanja
            cart_item.delete()
    except cartmodel.DoesNotExist:
        pass

    # Redirect pengguna kembali ke halaman keranjang belanja
    return redirect('keranjang')
