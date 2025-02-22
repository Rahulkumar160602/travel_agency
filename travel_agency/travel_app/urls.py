from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from travel_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("services/", views.services, name="services"),
    path("destinations/", views.destinations, name="destinations"),
    path("contact/", views.contact, name="contact"),
    path('trip_planing/', views.trip_planing, name='trip_planing'),
    path('custom_itineraries/', views.custom_itineraries, name='custom_itineraries'),
    path('group_discounts/', views.group_discounts, name='group_discounts'),
    path('travel_insurance/', views.travel_insurance, name='travel_insurance'),
    path('visa_assistance/', views.visa_assistance, name='visa_assistance'),
    path('customer_support/', views.customer_support, name='customer_support'),
    path('paris/', views.paris, name="paris"),
    path('rome/', views.rome, name="rome"),
    path('tokyo/', views.tokyo, name="tokyo"),
    path('newyork/', views.newyork, name="newyork"),
    path('sydney/', views.sydney, name="sydney"),
    path('capetown/', views.capetown, name="capetown"),
    path('dubai/', views.dubai, name="dubai"),
    path('bali/', views.bali, name="bali"),
    path('book/', views.book, name='book'),
    path('submit-booking', views.submit_booking, name='submit_booking'),
    path('login/', views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('explore-destinations/', views.explore_destinations, name='explore_destinations'),
    path('test-write/', views.test_file_write, name='test_write'),
    path('effiel/',views.effiel,name="effiel"),
    path('louvre/',views.louvre,name="louvre"),
    path("contact/", views.contact, name="contact"),
    
] 

# Media file handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
