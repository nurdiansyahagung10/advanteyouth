from django.db import models
from accounts.models import CustomUser
from products.models import product

class OrderItem(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.quantity * self.price

class cartmodel(models.Model):
    cart_id = models.OneToOneField(CustomUser,  on_delete=models.CASCADE)
    OrderItem_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.cart_id.username

    
class Order(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    OrderItem_id = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} on {self.created_at}"

