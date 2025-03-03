from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def create_item(request):
    return HttpResponse("This is the create item page.")
