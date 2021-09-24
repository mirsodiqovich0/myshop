from io import BytesIO
# from celery import task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from orders.models import Order


# @task
def payment_complated(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase. '
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")))
    pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), out, stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()
