from django.urls import path
from . import views

urlpatterns = [
     path('', views.shop, name = "shop"),
     path('warenkorb/', views.warenkorb, name = "warenkorb"),
     path('kasse/', views.kasse, name = "kasse"),
     path('artikel_backend/', views.artikelBackend, name="artikel_backend"),
     path('login/', views.loginSeite, name = "login"),
     path('logout/', views.logoutBenutzer, name = "logout"),
     path('reg/', views.regBenutzer, name = "reg"),
     path('bestellen/', views.bestellen, name = "bestellen"),
     
]
