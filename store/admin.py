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


from .seller_models import SellerProfile, SellerWallet, WalletTransaction


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "user",
        "phone",
        "approved",
        "created_at",
    )
    list_filter = ("approved", "created_at")
    search_fields = ("business_name", "phone", "user__username", "user__email")
    list_editable = ("approved",)
    readonly_fields = ("created_at",)


@admin.register(SellerWallet)
class SellerWalletAdmin(admin.ModelAdmin):
    list_display = ("seller", "created_at")
    search_fields = ("seller__business_name", "seller__phone")
    readonly_fields = ("seller", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "wallet",
        "transaction_type",
        "amount",
        "created_at",
    )
    list_filter = ("transaction_type", "created_at")
    search_fields = ("reference", "wallet__seller__business_name")
    readonly_fields = (
        "wallet",
        "transaction_type",
        "amount",
        "reference",
        "description",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
