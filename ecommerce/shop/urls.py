from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'shop'

urlpatterns = [
    path('', views.CategoryView.as_view(), name='categories'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)