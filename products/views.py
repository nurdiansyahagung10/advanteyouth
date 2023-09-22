# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import product,ProductImage
from django.contrib.auth.decorators import login_required 
from .forms import ProductForm
from django.contrib.auth.decorators import permission_required
from order.models import Cart,CartItem

@permission_required('products.add_product', login_url=None, raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            warna = form.cleaned_data.get('warna')
            ukuran = form.cleaned_data.get('ukuran')
            rasa = form.cleaned_data.get('rasa')
            product_instance.set_warna(warna)
            product_instance.set_ukuran(ukuran)
            product_instance.set_rasa(rasa)
            
            # Ambil toko dari pengguna yang sedang login
            store = request.user.store
            product_instance.store_id = store
            
            product_instance.save()

            # Tangani file-file yang diunggah
            for uploaded_file in request.FILES.getlist('image_product'):
                product_image = ProductImage(product=product_instance, image=uploaded_file)
                product_image.save()

            return redirect('store')  # Ganti 'my-form' dengan URL yang sesuai
    else:
        form = ProductForm()
    
    return render(request, 'products/add_products.html', {'form': form})


@login_required()
def databarang(request, slug):
    products = get_object_or_404(product, slug=slug)
    cart, _ = Cart.objects.get_or_create(cart_user_id=request.user)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is not None:
            quantity = int(quantity)
            if quantity > 0:
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=products, defaults={'quantity': quantity})
                if not created:
                    cart_item.quantity += quantity
                cart_item.save()
                
                # Redirect back to the previous page (referrer)
                return redirect(request.META.get('HTTP_REFERER', 'detailbarang'))
    
    context = {
        'product': products,
    }
    return render(request, 'products/databarang.html', context)

