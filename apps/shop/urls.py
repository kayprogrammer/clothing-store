from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("products/<slug:slug>/", views.ProductView.as_view(), name="product-detail"),
    path("categories/", views.CategoriesView.as_view(), name="categories"),
    path(
        "categories/<slug:slug>",
        views.CategoryProductsView.as_view(),
        name="category_products",
    ),
    path("cart/", views.CartView.as_view(), name="cart"),
]
