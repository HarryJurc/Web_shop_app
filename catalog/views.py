from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно обработать данные (например, сохранить в БД или отправить на почту)
        messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо за обращение.')
        return render(request, 'contacts.html', {'form_submitted': True})
    return render(request, 'contacts.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})