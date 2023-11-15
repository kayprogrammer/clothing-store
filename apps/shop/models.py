from django.db import models
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


class Product(BaseModel):
    name = models.CharField(max_length=100)
    desc = models.TextField(_("Description"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    @property
    def avg_rating(self):
        reviews = self.reviews.values_list("rating", flat=True)
        avg = round(mean(list(reviews)))  # Mean
        return avg

    class Meta:
        ordering = ["-created_at"]

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
