# views.py
from django.shortcuts import render, redirect
from .models import product,ProductImage
from django.contrib.auth.decorators import login_required 
from .forms import ProductForm
from django.contrib.auth.decorators import permission_required

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

            return redirect('my-form')  # Ganti 'my-form' dengan URL yang sesuai
    else:
        form = ProductForm()
    
    return render(request, 'products/add_products.html', {'form': form})


@login_required()
def databarang (request, slug):
    detailbarang = product.objects.get(slug=slug)
    context = {
        'slug' : detailbarang,
    }
    return render(request, 'products/databarang.html', context)

