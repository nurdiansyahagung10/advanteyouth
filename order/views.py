from django.shortcuts import render, redirect
from .models import Cart, CartItem,Order
from .forms import ShippingForm,PaymentForm


def checkout(request):
    cart, _ = Cart.objects.get_or_create(cart_user_id=request.user)
    total_quantity = sum([item.quantity for item in cart.items.all()])  # Memindahkan baris ini ke luar blok if
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if shipping_form.is_valid() and payment_form.is_valid():
            # Simpan informasi pengiriman dan pembayaran
            shipping = shipping_form.save()
            payment = payment_form.save()

            # Proses checkout
            # Buat objek Order baru
            order = Order.objects.create(user=request.user, shipping=shipping, payment=payment)

            # Pindahkan item dari Cart ke Order
            for item in cart.items.all():
                item.order = order
                item.cart = None
                item.save()

            # Kosongkan Cart
            cart.delete()

            return redirect('checkout_success')
    else:
        shipping_form = ShippingForm()
        payment_form = PaymentForm()
    context = {
        'cart': cart,
        'shipping_form': shipping_form,
        'payment_form': payment_form,
        'total_quantity': total_quantity,  # Sekarang total_quantity selalu didefinisikan
    }
    return render(request, 'order/checkout.html', context)


    
def cart_view(request):
    cart = Cart.objects.get(cart_user_id=request.user)
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
