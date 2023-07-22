from . models import Bestellung, BestellteArtikel
import json

def warenkorb_anzahl(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(kunde=kunde, erledigt=False)
        
        if bestellung:
            menge = bestellung.get_gesamtmenge
        else:
            menge = 0
        
    else:
        menge = 0
        try:
            warenkorb = json.loads(request.COOKIES['warenkorb'])
        except:
            warenkorb = {}
        for i in warenkorb:
            menge += warenkorb[i]["menge"]
        
    return {'menge': menge}