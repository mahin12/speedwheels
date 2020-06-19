from django import template

from car.models import Reservation

register = template.Library()


@register.simple_tag(name="check_reserved")
def check_reserved(id):
    if Reservation.objects.filter(product_id=id, is_reserved=True):
        return True
    else:
        return False
