# restaurant_billing/billing/models.py
# Create your models here.

from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)  # default GST %

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('dine-in', 'Dine-In'),
        ('takeaway', 'Takeaway'),
    ]
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI')
    ])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} ({self.order_type})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # per item price

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)
    current_order = models.OneToOneField(Order, null=True, blank=True, on_delete=models.SET_NULL)
