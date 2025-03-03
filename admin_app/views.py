from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def manage_account(request):
    return HttpResponse("This is the manage account page.")
