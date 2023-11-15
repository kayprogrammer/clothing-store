from django.shortcuts import render
from django.views import View
from apps.accounts.models import User

from apps.shop.models import Category, Product, Review


# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()[:6]
        categories = Category.objects.all()
        context = {
            "products": products,
            "categories": categories,
            "rating_range": range(5),
        }
        return render(request, "shop/home.html", context)
