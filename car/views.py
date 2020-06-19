import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy

from products.models import *

from .forms import *

posts = [
    {
        'author': 'Md Mahin',
        'title': 'Proton Preve',
        'content': 'Model 2020',
        'date_posted': 'December 1, 2019'
    },
    {
        'author': 'Md Mahin',
        'title': 'Perodua Bezza',
        'content': 'Model 2015',
        'date_posted': 'December 5, 2019'
    }
]


def home(request):
    # context = {
    #     'posts': posts
    # }
    # return render(request, 'car/home.html', context)
    return render(request, 'car/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'car/about.html', {'title': 'About'})


def gallery(request):
    return render(request, 'car/gallery.html', {'title': 'Gallery'})


def contact(request):
    return render(request, 'car/contact.html', {'title': 'Contact'})


def carlist(request):
    cars = Product.objects.all()
    return render(request, 'car/carlist.html', {'title': 'Contact', 'cars': cars})


@login_required
def reserve(request, id):
    if Reservation.objects.filter(product_id=id, is_reserved=True):
        messages.warning(request, "This car is already booked")
        return redirect(reverse_lazy("car-carlist"))
    form = ReserveForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            rent_from = form.cleaned_data['rent_from']
            rent_to = form.cleaned_data['rent_to']
            diff = rent_to - rent_from
            hours = diff.total_seconds() / 3600
            request.session['id'] = id
            request.session['hours'] = hours
            product = Product.objects.get(id=id)
            if product:
                form.instance.user = request.user
                form.instance.product = product
                form = form.save()
                request.session['reservation_id'] = form.id
                # we will update is_reserved to True after checkout
                return redirect("checkout")
            else:
                raise ValidationError("Invalid car")
    return render(request, 'car/booking.html', {'form': form})


@login_required
def report(request):
    form = ReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "You report successfully submitted to admin for review")
    return render(request, 'car/report.html', {'form': form})


@login_required
def pay(request):
    card_number = request.POST.get('card_number')
    if card_number == '00000':
        messages.warning(request, "Invalid card number. Please check card details")
        return redirect("checkout")
    total = request.session['total']
    reservation_id = request.session['reservation_id']
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.cost = total
    reservation.is_reserved = True
    reservation.save()
    messages.success(request, "You have successfully reserved the car")
    del request.session['id']
    del request.session['total']
    del request.session['hours']
    del request.session['reservation_id']
    return redirect("car-carlist")


@login_required
def checkout(request):
    id = request.session.get('id', 0)
    hours = request.session.get('hours', 0)
    total = 0
    product = None
    if id:
        product = Product.objects.get(id=id)
        total = round(hours * product.price, 2)
        request.session['total'] = total
    return render(request, 'car/checkout.html',
                  {'title': 'Checkout', 'hours': hours, 'product': product, 'total': total})


@login_required
def detail(request, pk):
    info = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product_id=pk)
    print(reviews)
    context = {
        'info': info,
        'reviews': reviews
    }
    if request.method == 'POST':
        description = request.POST.get('review') or None
        rating = request.POST.get('rating') or 0
        print('rating - ', rating)
        if description is None:
            render(request, 'car/details.html', {'info': info})
        info.total_review = info.total_review + 1
        info.total_review_sum = info.total_review_sum + int(rating)
        info.avg_rating = info.total_review_sum / info.total_review
        info.save()

        review = Review()
        review.description = description
        review.rating = int(rating)
        review.user = request.user
        review.product = info
        review.save()

        reviews = Review.objects.filter(product_id=pk)
        print(reviews)
        context = {
            'info': info,
            'reviews': reviews,
            'msg': 'Thanks for your review'
        }
        
        
    return render(request, 'car/details.html', context)


@login_required
def shop_review(request):
    context = {}
    if request.method == 'GET':
        shop_reviews = ShopReview.objects.all()
        context = {
            'reviews': shop_reviews
        }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('review')
        rating = request.POST.get('rating')

        print(name, ' ', description, ' ', rating)
        review_save = ShopReview()
        review_save.name = name
        review_save.description = description
        review_save.rating = int(rating)
        review_save.user = request.user
        review_save.save()

        context = {
            'reviews': ShopReview.objects.all(),
            'msg': 'Thanks for your review'
        }
    return render(request, 'car/shop_review.html', context)