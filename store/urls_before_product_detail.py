from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("oda/<int:product_id>/", views.order_product, name="order_product"),
    path("oda/imepokelewa/<int:order_id>/", views.order_success, name="order_success"),
]
