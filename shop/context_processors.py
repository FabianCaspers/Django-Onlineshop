from . models import Bestellung, BestellteArtikel

def warenkorb_anzahl(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung = Bestellung.objects.get(kunde=kunde, erledigt=False)
        
        if bestellung:
            menge = bestellung.get_gesamtmenge
        else:
            megen = 0
        
    else:
        menge = 0
        
    return {'menge': menge}