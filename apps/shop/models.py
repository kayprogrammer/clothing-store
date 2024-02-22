from django.db import models
from django.urls import reverse
from apps.accounts.models import User

from apps.common.models import BaseModel
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from statistics import mean


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse("category_products", args=[str(self.slug)])


class Product(BaseModel):
    name = models.CharField(max_length=100)
    desc = models.TextField(_("Description"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    image = models.ImageField(default="fallback.jpg", upload_to="products/")
    featured = models.BooleanField(default=False)
    flash_deals = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = "https://st2.depositphotos.com/47577860/47705/v/450/depositphotos_477051800-stock-illustration-cloth-shirt-fashion-icon-filled.jpg"
        return url

    @property
    def avg_rating(self):
        reviews = [review.rating for review in self.reviews.all()]
        avg = 0
        if len(reviews) > 0:
            avg = round(mean(list(reviews)))  # Mean
        return avg

    class Meta:
        ordering = ["-created_at"]


class OrderItem(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orderitems", null=True, blank=True
    )
    session_key = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orderitems"
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total(self):
        return self.quantity * self.product.price
    
RATING_CHOICES = ((5, 5), (4, 4), (3, 3), (2, 2), (1, 1))


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.SmallIntegerField(choices=RATING_CHOICES)
    text = models.TextField()

    def __str__(self):
        return self.user.full_name
