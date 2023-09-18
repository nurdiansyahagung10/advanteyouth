from django.shortcuts import render
from products.models import product, ProductImage

def home(request):
    # Mengambil semua objek produk
    products = product.objects.all()

    # Mengambil objek gambar terkait dengan setiap produk
    product_images = ProductImage.objects.filter(product__in=products)

    return render(request, 'index.html', {'products': products, 'product_images': product_images})
