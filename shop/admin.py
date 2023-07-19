from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Kunde)
admin.site.register(Artikel)
admin.site.register(Bestellung)
admin.site.register(BestellteArtikel)
admin.site.register(Adresse)