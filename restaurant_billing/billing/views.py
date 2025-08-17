# Create your views here.

from django.shortcuts import render, redirect
from .models import MenuItem, Order, OrderItem
from django.db.models import Sum

def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'billing/menu.html', {'items': items})


def create_order(request):
    if request.method == 'POST':
        order_type = request.POST['order_type']
        payment_method = request.POST['payment_method']
        selected_items = request.POST.getlist('items')  # list of item ids
        quantities = request.POST.getlist('quantities')

        order = Order.objects.create(
            order_type=order_type,
            payment_method=payment_method,
            total_amount=0,
            gst_amount=0,
        )

        total = 0
        gst_total = 0
        for idx, item_id in enumerate(selected_items):
            item = MenuItem.objects.get(id=item_id)
            qty = int(quantities[idx])
            price = item.price * qty
            gst_val = (price * item.gst) / 100

            OrderItem.objects.create(order=order, menu_item=item, quantity=qty, price=price)
            total += price
            gst_total += gst_val

        order.total_amount = total + gst_total
        order.gst_amount = gst_total
        order.save()

        return redirect('order_detail', order_id=order.id)

    items = MenuItem.objects.all()
    return render(request, 'billing/create_order.html', {'items': items})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'billing/order_detail.html', {'order': order})

def sales_report(request):
    report = Order.objects.values('created_at__date').annotate(
        total_sales=Sum('total_amount')
    )
    return render(request, 'billing/report.html', {'report': report})

from fpdf import FPDF
from django.http import HttpResponse
import csv

def export_pdf(request, order_id):
    from .models import Order
    order = Order.objects.get(id=order_id)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Bill - Order {order.id}", ln=True, align='C')

    for item in order.items.all():
        pdf.cell(200, 10, txt=f"{item.menu_item.name} x {item.quantity} = {item.price}", ln=True)

    pdf.cell(200, 10, txt=f"GST: {order.gst_amount}", ln=True)
    pdf.cell(200, 10, txt=f"Total: {order.total_amount}", ln=True)

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{order.id}.pdf"'
    return response


def export_csv(request, order_id):
    from .models import Order
    order = Order.objects.get(id=order_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="bill_{order.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item', 'Quantity', 'Price'])
    for item in order.items.all():
        writer.writerow([item.menu_item.name, item.quantity, item.price])

    writer.writerow(['GST', '', order.gst_amount])
    writer.writerow(['Total', '', order.total_amount])

    return response

from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    ...

from django.core.mail import send_mail

def email_bill(request, order_id):
    order = Order.objects.get(id=order_id)
    message = f"Order ID: {order.id}\nTotal: {order.total_amount}"
    send_mail(
        subject=f"Bill for Order {order.id}",
        message=message,
        from_email="yourrestaurant@gmail.com",
        recipient_list=["customer@gmail.com"]
    )
    return HttpResponse("Bill emailed!")
