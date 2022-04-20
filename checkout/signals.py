from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    This function updates the order total on lineitem update/create
    """
    instance.order.update_order()


@receiver(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    This function updates the order total on lineitem update/create
    """
    instance.order.update_order()
