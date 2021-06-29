from django.db import models
from core.models import TimeStampModel, User

# Create your models here.


class Product(TimeStampModel):
    Category_choice = (
        ("Category 1", "Category 1"),
        ("Category 2", "Category 2"),
        ("Category 3", "Category 3"),
        ("Category 4", "Category 4"),
        ("Category 6", "Category 6"),
        ("Category 7", "Category 7"),
        ("Category 8", "Category 8"),
        ("Category 9", "Category 9"),
    )
    name = models.CharField(max_length=100)
    category_name = models.CharField(choices=Category_choice, max_length=20)
    image = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    in_stock = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=5)
    product_price = models.DecimalField(max_digits=10, decimal_places=5)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_user", null=True
    )
    last_updated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}---{self.sale_price}"


class ProductView(TimeStampModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_view"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    view_count = models.IntegerField(default=0)
    last_viewed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product}--{self.user}--{self.view_count}"
