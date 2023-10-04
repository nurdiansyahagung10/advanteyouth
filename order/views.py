from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem,Order
from django.contrib import messages
from .forms import ShippingForm
from accounts.models import UserAddress
from django.shortcuts import render, redirect
from .models import Cart, UserAddress, Order
from .forms import ShippingForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from accounts.decorators import group_required
from django.urls import reverse

@group_required('buyer')
def payment(request, order_id):
    host = request.get_host()
    order = Order.objects.get(id=order_id)
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.total_price,
        'item_name': order.Cart,  # Ganti dengan atribut yang sesuai di model Order Anda
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('checkout_success', kwargs={'order_id': order_id})}",
        'cancel_url': f"http://{host}{reverse('checkout')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'order': order,
        'paypal': paypal_payment
    }

    return render(request, 'order/payment.html', context)

@group_required('buyer')
def checkout(request):
    cart, _ = Cart.objects.get_or_create(cart_user_id=request.user)
    total_quantity = sum([item.quantity for item in cart.items.all()])
    
    main_address = UserAddress.objects.filter(UserAddressId=request.user, Main_address=True).first()
    
    if request.method == 'POST':
        
        # Cek apakah pengguna sudah memiliki pesanan yang belum diselesaikan
        for item in cart.items.all():
            unfinished_orders = Order.objects.filter(user=request.user, Cart__items=item, order_succes=False)
            if unfinished_orders.exists():
                messages.error(request, f"Anda masih memiliki pesanan yang belum diselesaikan untuk produk {item.product_id.name_product}. Harap selesaikan atau batalkan pesanan tersebut sebelum melakukan pemesanan baru.")
                return redirect('checkout')

        # Jika tidak ada pesanan yang belum diselesaikan, lanjutkan dengan proses checkout seperti biasa
        shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            shipping = shipping_form.save()
            total_price = cart.total_price()
            order = Order.objects.create(
                user=request.user,
                Cart=cart,
                shipping=shipping,
                total_price=total_price
            )

            print(request.POST)

            for item in cart.items.all():
                item.order = order
                item.save()

            # Mengirim ID pesanan sebagai bagian dari argumen redirect
            return redirect('payment',  order_id=order.id)
    # ...


    else:
        # Get all addresses associated with the user and order by Main_address=True
        user_addresses = UserAddress.objects.filter(UserAddressId=request.user).order_by('-Main_address')
        
        # Create a list of choices for the dropdown with all addresses
# Buat list of choices untuk dropdown dengan ID alamat sebagai nilai dan teks tampilan sebagai label
        address_choices = [(address.address_id, str(address.full_name)) for address in user_addresses]
        
        # Check if there is a main address, and set it as the initial choice if available
        initial_address = main_address.UserAddressId if main_address else ''

        # Make sure the initial choice is selected in the dropdown
        shipping_form = ShippingForm(initial={'address': initial_address})
        
        # Update choices for the 'address' field to include all addresses
        shipping_form.fields['address'].choices = address_choices

    context = {
        'cart': cart,
        'shipping_form': shipping_form,
        'total_quantity': total_quantity,
    }
    return render(request, 'order/checkout.html', context)

@group_required('buyer')
def checkout_success(request, order_id):
    # Dapatkan pesanan terakhir pengguna
    order = Order.objects.filter(user=request.user).latest('id')
    print(order)
    # Kirim data pesanan ke template
    context = {
        'order': order,
    }
    return render(request, 'order/checkout_success.html', context)


@group_required('buyer')
def cart_view(request):
    if request.user.is_anonymous:
        messages.error(request, 'Anda harus login terlebih dahulu.')
        return redirect('sign')
    else:
        try:
            cart = Cart.objects.get(cart_user_id=request.user)
        except Cart.DoesNotExist:
            # Handle the case when the cart does not exist
            # For example, you might want to create a new cart
            cart = Cart.objects.create(cart_user_id=request.user)

        cart_items = CartItem.objects.filter(cart=cart)
        total_quantity = sum([item.quantity for item in cart_items])
        total_price = cart.total_price()

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }
    return render(request, 'order/cart.html', context)     

@group_required('buyer')
def order_history(request):
    # Pastikan pengguna sudah login
    if request.user.is_authenticated:
        # Dapatkan semua pesanan yang telah selesai
        finished_orders = Order.objects.filter(user=request.user, status='Selesai')

        # Dapatkan semua pesanan yang belum selesai
        unfinished_orders = Order.objects.filter(user=request.user).exclude(status='Selesai')

        return render(request, 'order/order.html', {
            'finished_orders': finished_orders,
            'unfinished_orders': unfinished_orders,
        })
    else:
        # Redirect pengguna yang belum login ke halaman login
        return redirect('login')  # Ganti 'login' dengan URL halaman login yang sesuai

@group_required('buyer')
def replace_order(request, item_id):
    item_to_replace = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        warna = request.POST.get('warna')  # Ambil warna dari form
        ukuran = request.POST.get('ukuran')  # Ambil ukuran dari form
        rasa = request.POST.get('rasa')  # Ambil rasa dari form

        print(request.POST)

        if quantity is not None and quantity.isdigit() and int(quantity) > 0:
            # Set quantity ke dalam CartItem
            item_to_replace.quantity = int(quantity)
            
            # Set warna, ukuran, dan rasa ke dalam CartItem
            item_to_replace.warna = warna
            item_to_replace.ukuran = ukuran
            item_to_replace.rasa = rasa
            item_to_replace.save()
            
            messages.success(request, 'Pesanan Anda telah berhasil diganti.')
            
    return redirect('cart')  # Ganti 'cart' dengan URL halaman keranjang yang sesuai


