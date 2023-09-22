# models.py
from django.db import models
from accounts.models import Store
from django.utils.text import slugify

class product(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    CATEGORY_CHOICES = (
        ('', ''),
        ('food', 'Food'),
        ('fashion', 'Fashion'),
        ('electronics', 'Electronics'),
        ('vehicles', 'Vehicles and Accessories'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='')
    warna = models.TextField(null=True)
    ukuran = models.TextField(null=True)
    rasa = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True,editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_product)
        super(product, self).save(*args, **kwargs)

    def __str__(self):
        return"{}. {}".format(self.id_produk, self.name_product)
    

    def __str__(self):
        return self.name_product

    def set_warna(self, warna_list):
        self.warna = ','.join(warna_list)

    def get_warna(self):
        return self.warna.split(',')

    def set_ukuran(self, ukuran_list):
        self.ukuran = ','.join(ukuran_list)

    def get_ukuran(self):
        return self.ukuran.split(',')

    def set_rasa(self, rasa_list):
        self.rasa = ','.join(rasa_list)

    def get_rasa(self):
        return self.rasa.split(',')


class ProductImage(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
            return f"Image for {self.product.name_product}"

