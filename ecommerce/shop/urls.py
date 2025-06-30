from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'shop'

urlpatterns = [
    path('', views.CategoryView.as_view(), name='categories'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('user/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('addcategory/', views.AddCategoryView.as_view(), name='add_category'),
    path('addproduct/', views.AddProductView.as_view(), name='add_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)