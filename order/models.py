from django.db import models
from accounts.models import CustomUser
from products.models import product  # ensure correct case for your model


class Cart(models.Model):
    cart_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.cart_user_id.username}'s Cart"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product_id.name_product} Cart Item"

    def subtotal(self):
        return self.product_id.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shipping = models.ForeignKey('ShippingModel', on_delete=models.CASCADE)
    payment = models.ForeignKey('PaymentModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add any other fields you need for your Order model

    def __str__(self):
        return f"Order #{self.id}"
    
class ShippingModel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class PaymentModel(models.Model):
    card_number = models.CharField(max_length=16)  # You may want to use a more secure field for card numbers
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)  # You may want to use a more secure field for CVV

    def __str__(self):
        return f"Payment with Card ending in {self.card_number[-4:]}"