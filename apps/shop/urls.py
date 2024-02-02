from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path("cart/", views.CartView.as_view(), name="cart"),
]
