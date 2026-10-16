from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("sofa", "Sofa"),
        ("bed", "Vitanda"),
        ("chair", "Viti"),
        ("table", "Meza"),
        ("cabinet", "Makabati"),
        ("other", "Samani nyingine"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    material = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    PAYMENT_METHOD_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("mixx", "Mixx by Yas"),
        ("airtel", "Airtel Money"),
        ("tpesa", "T-Pesa"),
    ("halopesa", "HaloPesa"),
        ("bank", "Benki"),
        ("other", "Njia nyingine"),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="mpesa",
        verbose_name="Njia ya malipo",
    )
    payment_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Namba ya malipo au akaunti",
    )
    payment_account_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Jina la mwenye akaunti",
    )
    deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Kiasi cha malipo ya awali (TSh)",
    )
    production_time = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Muda wa kutengeneza bidhaa",
        help_text="Mfano: Siku 7-14",
    )
    balance_payment_terms = models.CharField(
        max_length=200,
        default="Baada ya kupokea bidhaa",
        verbose_name="Masharti ya kulipa salio",
    )

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance_amount(self):
        return max(self.price - self.deposit_amount, 0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Oda mpya"),
        ("confirmed", "Imethibitishwa"),
        ("making", "Inatengenezwa"),
        ("ready", "Tayari kwa ajili ya delivery"),
        ("delivered", "Imewasilishwa"),
        ("cancelled", "Imeghairiwa"),
    ]

    COLOR_CHOICES = [
        ("black", "Nyeusi"),
        ("grey", "Kijivu"),
        ("brown", "Kahawia"),
        ("cream", "Cream"),
        ("blue", "Bluu"),
        ("green", "Kijani"),
        ("other", "Rangi nyingine"),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default="other")
    fabric = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"Oda #{self.pk} - {self.customer_name}"

    class Meta:
        ordering = ["-created_at"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picha ya ziada - {self.product.name}"
