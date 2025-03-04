from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def userpage(request):
    return HttpResponse("Hello, world. You're at the index page for the individual bee_pocket.")


def index_page(request):
    return render(request, 'base.html')
