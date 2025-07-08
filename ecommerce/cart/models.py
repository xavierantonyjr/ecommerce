from django.db import models
from authentication.models import CustomUser
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)
    order_id = models.CharField(null=True)
    is_ordered = models.CharField(default=False)
    amount = models.FloatField(null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Total: {self.total_amount}"

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.user.username} - {self.product.name} ({self.quantity})"
