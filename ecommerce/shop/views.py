from django.shortcuts import render
from django.views import View
from unicodedata import category

from .models import Category, Product


# Create your views here.

class CategoryView(View):
    def get(self, request):
        category = Category.objects.all()
        return render(request, 'categories.html', {'categories': category})

class ProductView(View):
    def get(self, request,pk):
        category = Category.objects.get(pk=pk)
        product = category.products.all()
        return render(request, 'products.html',{'products': product})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'product_detail.html', {'product': product})