from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),

]