__author__ = 'eaura'
from django.shortcuts import render
def base(request):

    return render(request, 'base.html')