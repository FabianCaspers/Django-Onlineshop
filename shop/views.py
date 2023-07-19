from django.shortcuts import render

# Create your views here.
def shop(request):
    return render(request, 'shop/shop.html')

def warenkorb(request):
    return render(request, 'shop/warenkorb.html')

def kasse(request):
    return render(request, 'shop/kasse.html')