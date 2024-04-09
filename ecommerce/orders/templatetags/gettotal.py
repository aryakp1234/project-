# custom_tags.py

from django import template

register = template.Library()

@register.filter(name='gettotal')
def gettotal(cart):
    total = 0
    for item in cart.added_items.all():
        total += item.quantity * item.product.price
    return total
