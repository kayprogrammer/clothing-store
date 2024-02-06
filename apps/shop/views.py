import random
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from apps.shop.models import Category, OrderItem, Product
from apps.shop.utils import get_session_key


# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()[:6]
        categories = Category.objects.all()
        context = {
            "products": products,
            "categories": categories,
        }
        return render(request, "shop/home.html", context)


class ProductsView(ListView):
    model = Product
    paginate_by = 5
    template_name = "shop/products.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[OrderItem]:
        products = Product.objects.prefetch_related("reviews")
        filter_value = self.request.GET.get("filter")
        if filter_value and (filter_value == "featured" or filter_value == "flash_deals"):
            filter_data = {filter_value: True}
            products = products.filter(**filter_data)
        return products

class CategoriesView(ListView):
    model = Category
    template_name = "shop/categories.html"
    context_object_name = "categories"


class CartView(ListView):
    model = Category
    template_name = "shop/cart.html"
    context_object_name = "orderitems"

    def get_queryset(self) -> QuerySet[OrderItem]:
        request = self.request
        user = request.user
        session_key = get_session_key(request)
        filter_data = session_key or user.id
        orderitems = OrderItem.objects.filter(
            Q(session_key=filter_data) | Q(user_id=filter_data)
        )
        return orderitems
