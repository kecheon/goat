from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item
# Create your views here.


def home_page(request):
    new_item = Item()
    if request.method == 'POST':
        new_item.text = request.POST.get('item_text')
        new_item.save()
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'home.html', {'items':items})
