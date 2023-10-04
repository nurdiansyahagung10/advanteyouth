# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import product,ProductImage
from django.contrib.auth.decorators import login_required 
from .forms import ProductForm
from .models import product
from accounts.decorators import group_required
from order.models import Cart,CartItem
from rest_framework import viewsets
from .serializers import ProductSerializer
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe

@group_required('seller')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)

            # Mengakses data tambahan warna dari form
            warna_data = []
            for key, value in request.POST.items():
                if key.startswith('extra_field_warna_'):
                    warna_data.append(value)

            # Mengakses data tambahan ukuran dari form
            ukuran_data = []
            for key, value in request.POST.items():
                if key.startswith('extra_field_ukuran_'):
                    ukuran_data.append(value)

            # Mengakses data tambahan rasa dari form
            rasa_data = []
            for key, value in request.POST.items():
                if key.startswith('extra_field_rasa_'):
                    rasa_data.append(value)

            # Menyimpan data tambahan ke dalam model atau struktur data yang sesuai
            product_instance.set_warna(warna_data)
            product_instance.set_ukuran(ukuran_data)
            product_instance.set_rasa(rasa_data)

            # Ambil toko dari pengguna yang sedang login
            store = request.user.store
            product_instance.store_id = store

            product_instance.save()

            # Tangani file-file yang diunggah
            for uploaded_file in request.FILES.getlist('image_product'):
                product_image = ProductImage(product=product_instance, image=uploaded_file)
                product_image.save()

            return redirect('seller_dashboard')  # Ganti 'seller_dashboard' dengan URL yang sesuai
    else:
        form = ProductForm()

    return render(request, 'products/add_products.html', {'form': form})


@group_required('buyer')
def databarang(request, slug):
    products = get_object_or_404(product, slug=slug)
    cart, _ = Cart.objects.get_or_create(cart_user_id=request.user)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        warna = request.POST.get('warna')  # Ambil warna dari form
        ukuran = request.POST.get('ukuran')  # Ambil ukuran dari form
        rasa = request.POST.get('rasa')  # Ambil rasa dari form
        
        request.session['post_data'] = request.POST
        # Cek apakah pengguna sudah memiliki item ini dalam keranjang
        existing_item = CartItem.objects.filter(cart=cart, product_id=products).first()
        if existing_item:
            return render(request, 'order/confirm_replace_order.html', {
                'existing_item': existing_item,
                'quantity' : quantity,
                'warna' : warna,  # Ambil warna dari form
                'ukuran' : ukuran,  # Ambil ukuran dari form
                'rasa' : rasa  # Ambil rasa dari form
            })
        else:

            if quantity is not None and quantity.isdigit() and int(quantity) > 0:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product_id=products, defaults={'quantity': int(quantity)}
                )
                if not created:
                    cart_item.quantity += int(quantity)
                
                # Set warna, ukuran, dan rasa ke dalam CartItem
                cart_item.warna = warna
                cart_item.ukuran = ukuran
                cart_item.rasa = rasa
                cart_item.save()
                
                # Redirect back to the previous page (referrer)
                return redirect(request.META.get('HTTP_REFERER', 'detailbarang'))

    context = {
        'product': products,
    }
    return render(request, 'products/databarang.html', context)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()  # Define the queryset to fetch all products
    serializer_class = ProductSerializer
    lookup_field = 'category'  # The field to filter on (category in this case)


def filtered_products(request, category):
    # Assuming you have a 'category' field in your Product model
    # Filter products based on the specified category
    filtered_products = product.objects.filter(category=category)

    # You can pass this filtered queryset to your template
    context = {
        'products': filtered_products,
    }

    return render(request, 'products/list_products.html', context)
