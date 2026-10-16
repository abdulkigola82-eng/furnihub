from django.urls import path
from . import views
from . import seller_views

urlpatterns = [
    path("muuzaji/jisajili/", seller_views.seller_register, name="seller_register"),
    path("muuzaji/ingia/", seller_views.seller_login, name="seller_login"),
    path("muuzaji/dashibodi/", seller_views.seller_dashboard, name="seller_dashboard"),
    path("muuzaji/bidhaa/ongeza/", seller_views.seller_add_product, name="seller_add_product"),
    path("muuzaji/toka/", seller_views.seller_logout, name="seller_logout"),

    path("", views.home, name="home"),
    path("bidhaa/<int:product_id>/", views.product_detail, name="product_detail"),
    path("oda/<int:product_id>/", views.order_product, name="order_product"),
    path("oda/imepokelewa/<int:order_id>/", views.order_success, name="order_success"),
]
