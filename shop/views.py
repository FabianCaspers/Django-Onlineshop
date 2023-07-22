from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from . forms import EigeneUserCreationForm
import uuid
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

# Create your views here.
def shop(request):
    artikels = Artikel.objects.all()
    ctx = {'artikels':artikels}
    return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel.all()
    else:
        
        try:
            warenkorb = json.loads(request.COOKIES['warenkorb'])
        except:
            warenkorb = {}
            
        artikels = []
        bestellung = {'get_gesamtpreis':0, 'get_gesamtmenge':0}
        menge = bestellung['get_gesamtmenge']
        
        for i in warenkorb:
            menge += warenkorb[i]["menge"]
            artikel = Artikel.objects.get(id=i)
            gesamtpreis = (artikel.preis * warenkorb[i]['menge'])
            bestellung['get_gesamtpreis'] += gesamtpreis
            
            artikel = {
                'artikel': {
                    'id':artikel.id,
                    'name':artikel.name,
                    'preis':artikel.preis,
                    'bild':artikel.bild 
                    },
                'menge':warenkorb[i]['menge'],
                'get_summe':gesamtpreis
            }
            artikels.append(artikel)
        
        
    ctx = {"artikels": artikels, "bestellung": bestellung}
    return render(request, 'shop/warenkorb.html', ctx)

def kasse(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel.all()
    else:
        artikels = []
        bestellung = []
        
    ctx = {"artikels": artikels, "bestellung": bestellung}
    return render(request, 'shop/kasse.html', ctx)


def artikelBackend(request):
    daten = json.loads(request.body)
    artikelID = daten['artikelID']
    action = daten['action']
    kunde = request.user.kunde
    artikel = Artikel.objects.get(id=artikelID)
    bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
    bestellteArtikel, created = BestellteArtikel.objects.get_or_create(bestellung=bestellung, artikel=artikel)
    
    if action == 'bestellen':
        bestellteArtikel.menge = (bestellteArtikel.menge +1)
        messages.success(request, 'Artikel wurde zum Warenkorb hinzugefügt.')
    elif action == 'entfernen':
        bestellteArtikel.menge = (bestellteArtikel.menge -1)
        messages.warning(request, 'Artikel wurde aus dem Warenkorb entfernt.')
        
    bestellteArtikel.save()
    
    if bestellteArtikel.menge <= 0:
        bestellteArtikel.delete()

    return JsonResponse("Artikel hinzugefügt", safe=False)


def loginSeite(request):
    seite = 'login'
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        password = request.POST['password']
        
        benutzer = authenticate(request, username=benutzername, password=password)
        
        if benutzer is not None:
            login(request, benutzer)
            return redirect('shop')
        else:
            messages.error(request, "Benutzername oder Passwort nicht korrekt.")
            
    return render(request, 'shop/login.html', {'seite': seite})

def logoutBenutzer(request):
    logout(request)
    return redirect('shop')

def regBenutzer(request):
    seite = 'reg'
    form = EigeneUserCreationForm
    
    if request.method == 'POST':
        form = EigeneUserCreationForm(request.POST)
        if form.is_valid():
           benutzer =  form.save(commit=False)
           benutzer.save()
           
           kunde = Kunde(name=request.POST['username'], benutzer=benutzer)
           kunde.save()
           bestellung = Bestellung(kunde=kunde)
           bestellung.save()
           
           login(request, benutzer)
           return redirect('shop')
        else:
            messages.error(request, "Fehlerhafte Eingabe!")
    
    
    ctx = {'form': form, 'seite': seite}
    return render(request, 'shop/login.html', ctx)

def bestellen(request):
    auftrags_id = uuid.uuid4()
    daten = json.loads(request.body)
    
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        gesamtpreis = float(daten['benutzerDaten']['gesamtpreis'])
        bestellung.auftrags_id = auftrags_id
        bestellung.erledigt = True
        bestellung.save()
        
        Adresse.objects.create(
            kunde=kunde,
            bestellung=bestellung,
            adresse=daten['lieferAdresse']['Adresse'],
            plz=daten['lieferAdresse']['plz'],
            stadt=daten['lieferAdresse']['stadt'],
            land=daten['lieferAdresse']['land'],
        )
        
    else:
        print("nicht eingeloggt")
    
    auftragsUrl = str(auftrags_id)
    messages.success(request, mark_safe("Vielen Dank für Ihre <a href='/bestellung/"+auftragsUrl+"'>Bestellung: "+auftragsUrl+"</a>"))
    return JsonResponse('Bestellung erfolgreich', safe=False)

@login_required(login_url='login')
def bestellung(request, id):
    bestellung = Bestellung.objects.get(auftrags_id=id)
    
    if bestellung and str(request.user) == str(bestellung.kunde):
        bestellung = Bestellung.objects.get(auftrags_id=id)
        artikels = bestellung.bestellteartikel.all()
        ctx = {'artikels':artikels, 'bestellung':bestellung}
        return render(request, 'shop/bestellung.html',ctx)
    else:
        return redirect('shop')
    
    
def fehler404(request, exception):
    return render(request, 'shop/404.html')