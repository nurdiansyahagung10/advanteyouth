from django.shortcuts import render
from products.models import product, ProductImage

def home(request):
    # Mengambil semua objek produk
    products = product.objects.all().order_by('-upload_date')
    # Mengambil objek gambar terkait dengan setiap produk
    product_images = ProductImage.objects.filter(product__in=products)

    return render(request, 'index.html', {'products': products, 'product_images': product_images})

def search_products(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')  # Mendapatkan teks pencarian dari query string 'q'
        products = product.objects.filter(name_product__icontains=query)  # Mengambil produk yang cocok dengan nama

        context = {
            'products': products,
            'query': query,
        }
        return render(request, 'searchresults.html', context)