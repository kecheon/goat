from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_page(request):
    res = "<html><title>TODO</title></html>"
    return HttpResponse(res)