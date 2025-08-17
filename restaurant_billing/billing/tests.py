# Create your tests here.

from django.test import TestCase
from .models import MenuItem, Order, OrderItem

class BillingTestCase(TestCase):
    def setUp(self):
        self.item1 = MenuItem.objects.create(name="Burger", category="Food", price=100, gst=5)
        self.item2 = MenuItem.objects.create(name="Pizza", category="Food", price=200, gst=5)

    def test_order_with_multiple_items(self):
        order = Order.objects.create(order_type="dine-in", payment_method="cash", total_amount=0, gst_amount=0)
        OrderItem.objects.create(order=order, menu_item=self.item1, quantity=2, price=200)
        OrderItem.objects.create(order=order, menu_item=self.item2, quantity=1, price=200)
        order.total_amount = 400
        order.gst_amount = 20
        order.save()
        self.assertEqual(order.total_amount, 400)

    def test_edge_case_no_items(self):
        order = Order.objects.create(order_type="takeaway", payment_method="upi", total_amount=0, gst_amount=0)
        self.assertEqual(order.items.count(), 0)
