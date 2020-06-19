from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.TextField()
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(null=True)
    summary = models.TextField(default='test')
    total_review = models.IntegerField(default=0)
    total_review_sum = models.IntegerField(default=0)
    avg_rating = models.FloatField(max_length=20, default=0)

    def __str__(self):
        return self.title



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', default=None)
    description = models.CharField(max_length=999, blank=True, null=True)
    rating = models.IntegerField()
    
    def __str__(self):
        return self.description
    

class ShopReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=999)
    rating = models.IntegerField()

    def __str__(self):
        return self.name