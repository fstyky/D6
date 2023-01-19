from django.contrib import admin
from django.urls import path, include


urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   # path('accounts/', include('django.contrib.auth.urls')),
   path("accounts/", include("allauth.urls")),
   path('products/', include('simpleapp.urls')),
   path('news/', include('simpleapp.urlsNew')),

   #path('multiply/', include('simpleapp.view.multiply')),
]