from .models import OrderItem
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_totals(sender, instance, **kwargs):
    order = instance.order
    total_tax = 0.0
    total_price = 0.0

    for item in order.items.all():
        tax_amount = item.menu_item.tax_amount
        total_tax += tax_amount * item.quantity
        total_price += item.get_total_price()

    order.total_tax = round(total_tax, 2)
    order.total_price = round(total_price, 2)
    order.total_before_tax = round((total_price - total_tax), 2)
    order.save()