from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('addtocart/<int:pk>/', views.AddToCartView.as_view(), name='addtocart'),
    path('cartview/', views.CartView.as_view(), name='cartview'),
    path('cartdecrement/<int:pk>/', views.Cart_decrementView.as_view(), name='cartdecrement'),
    path('cartremove/<int:pk>/', views.CartremoveView.as_view(), name='cartremove'),
    path('orderform/', views.OrderFormView.as_view(), name='orderform'),
    path('paymentsuccess/<str:pk>/', views.PaymentSuccessView.as_view(), name='paymentsuccess'),
    path('ordersummary/', views.OrderSummaryView.as_view(), name='ordersummary'),
]


if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
