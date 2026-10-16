from django.conf import settings
from django.db import models


class SellerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    business_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name


class SellerWallet(models.Model):
    seller = models.OneToOneField(
        SellerProfile,
        on_delete=models.PROTECT,
        related_name="wallet",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        credits = self.transactions.filter(
            transaction_type__in=["sale_credit", "refund_reversal"]
        ).aggregate(total=models.Sum("amount"))["total"] or 0

        debits = self.transactions.filter(
            transaction_type__in=["commission", "withdrawal", "adjustment_debit"]
        ).aggregate(total=models.Sum("amount"))["total"] or 0

        return credits - debits

    def __str__(self):
        return f"Pochi: {self.seller.business_name}"


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("sale_credit", "Mapato ya mauzo"),
        ("commission", "Kamisheni ya FurniHub"),
        ("withdrawal", "Kutoa fedha"),
        ("refund_reversal", "Marekebisho ya kurejesha fedha"),
        ("adjustment_debit", "Marekebisho ya kutoa fedha"),
    ]

    wallet = models.ForeignKey(
        SellerWallet,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPES,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.amount}"
