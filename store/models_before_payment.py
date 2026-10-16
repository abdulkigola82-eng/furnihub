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
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
