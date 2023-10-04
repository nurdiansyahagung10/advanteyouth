from django.db import models
from accounts.models import CustomUser
from products.models import product  # ensure correct case for your model
from accounts.models import UserAddress


class Cart(models.Model):
    cart_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.cart_user_id.username}'s Cart"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping = models.ForeignKey('ShippingModel', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default='Menunggu Konfirmasi')  # Status pesanan, defaultnya "Menunggu Konfirmasi"
    approved_by_seller = models.BooleanField(default=False)  # Kolom untuk menandai apakah pesanan sudah disetujui oleh penjual
    order_succes = models.BooleanField(default=False)  # Kolom untuk menandai apakah pesanan sudah disetujui oleh penjual
    # Add any other fields you need for your Order model

    def __str__(self):
        return f"Order #{self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)  # Tambahkan baris ini
    warna = models.CharField(max_length=255, null=True)
    ukuran = models.CharField(max_length=255, null=True)
    rasa = models.CharField(max_length=255, null=True)


    def __str__(self):
        return f"{self.product_id.name_product} Cart Item"

    def subtotal(self):
        return self.product_id.price * self.quantity

class ShippingModel(models.Model):
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)

    def __str__(self):
        return self.address.street
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)  # misalnya 'GoPay', 'DANA', dll.
    status = models.CharField(max_length=20)  # misalnya 'Pending', 'Paid', dll.

    def __str__(self):
        return f"Payment #{self.id} by {self.user.username}"
