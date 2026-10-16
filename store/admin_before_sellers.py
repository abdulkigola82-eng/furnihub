from django.contrib import admin
from .models import Product, ProductImage, Order




class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ("image", "alt_text")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ("name", "category", "price", "available", "created_at")
    list_filter = ("category", "available")
    search_fields = ("name", "description", "material")
    list_editable = ("price", "available")



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "product",
        "quantity",
        "unit_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "color", "created_at")
    search_fields = (
        "customer_name",
        "customer_phone",
        "product__name",
    )
    list_editable = ("status",)
    readonly_fields = ("created_at",)
