from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from apps.shop.forms import ReviewForm
from apps.shop.models import Category, OrderItem, Product
from apps.shop.utils import get_session_key, sort_filter_value, sort_products
from django.core.paginator import Paginator


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
    paginate_by = 15
    template_name = "shop/products.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[OrderItem]:
        products = Product.objects.prefetch_related("reviews")
        products = sort_products(self.request, products)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_filter_value(self.request, context)
        return context

class ProductView(View):
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.select_related("category").prefetch_related("reviews", "reviews__user").get(slug=kwargs["slug"])
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        form = ReviewForm()
        context = {
            "product": product,
            "form": form
        }
        return render(request, 'shop/product-detail.html', context)

class CategoriesView(ListView):
    model = Category
    template_name = "shop/categories.html"
    context_object_name = "categories"


class CategoryProductsView(View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs["slug"])
        products = Product.objects.filter(category=category).prefetch_related("reviews")
        products = sort_products(self.request, products)

        # Pagination config
        paginated = Paginator(products, 15)
        page_number = request.GET.get('page')
        page = paginated.get_page(page_number)
        is_paginated = True if page.paginator.num_pages > 1 else False

        context = {"category": category, "page_obj": page, "is_paginated": is_paginated}
        sort_filter_value(self.request, context)
        return render(request, "shop/category_products.html", context)

class CartView(ListView):
    model = Category
    template_name = "shop/cart.html"
    context_object_name = "orderitems"

    def get_queryset(self) -> QuerySet[OrderItem]:
        request = self.request
        user = request.user
        session_key = get_session_key(request)
        if user.is_authenticated:
            return OrderItem.objects.filter(user_id=user.id)
        else:
            return OrderItem.objects.filter(session_key=session_key)
