from django.shortcuts import render
from . models import *

# Create your views here.
def shop(request):
    artikels = Artikel.objects.all()
    ctx = {'artikels':artikels}
    return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
    return render(request, 'shop/warenkorb.html')

def kasse(request):
    return render(request, 'shop/kasse.html')