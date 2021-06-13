from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(reqest):
    return render(reqest, 'home.html',{'name':'Ashna'})

def add(reqest):

    val1 = int(reqest.POST['num1'])
    val2 = int(reqest.POST['num2'])
    res = val1 + val2
    return render(reqest, 'result.html',{'result': res})