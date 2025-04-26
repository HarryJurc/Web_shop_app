from django.shortcuts import render
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно обработать данные (например, сохранить в БД или отправить на почту)
        messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо за обращение.')
        return render(request, 'contacts.html', {'form_submitted': True})
    return render(request, 'contacts.html')