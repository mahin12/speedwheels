from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cars")
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    postal_zip = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    rent_from = models.DateTimeField()
    rent_to = models.DateTimeField()
    note = models.TextField(null=True)
    is_reserved = models.BooleanField(default=False)
    cost = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


ACCEPT_REJECT_CHOICES = (
    ('ACCEPTED', 'Accept'),
    ('REJECTED', 'Reject'),
    ('NONE', 'None')
)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField()
    incident_time = models.DateTimeField()
    car_details = models.TextField()
    issued_by = models.TextField()
    location = models.CharField(max_length=200)
    nature = models.CharField(max_length=200)
    incident_details = models.TextField()
    shop_name = models.CharField(max_length=50, default='name')
    shop_number = models.CharField(max_length=30, default='number')
    status = models.CharField(max_length=20, choices=ACCEPT_REJECT_CHOICES, default='NONE')

    def __str__(self):
        return self.incident_details

