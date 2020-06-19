from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='car-home'),
    path('about/', views.about, name='car-about'),
    path('gallery/', views.gallery, name='car-gallery'),
    path('contact/', views.contact, name='car-contact'),
    path('carlist/', views.carlist, name='car-carlist'),
    path('reserve/<int:id>', views.reserve, name='reserve'),
    path('report/', views.report, name='report'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.pay, name='pay'),
    path('details/<int:pk>/', views.detail, name='detail'),
    path('shop_review/', views.shop_review, name='shop_review'),
]
