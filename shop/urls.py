
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="ShopHome"),
    path("about/", views.about,name="About"),
    path("contact/", views.contact,name="Contact"),
    path("tracker/", views.tracker,name="TrakingStatus"),
    path("search/", views.search,name="Search"),
    path("products/<int:id>", views.prodview,name="Productview"),
    path("checkout/", views.checkout,name="Checkout"),
]
