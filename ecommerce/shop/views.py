from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .forms import CategoryForm, ProductForm
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

class GalleryView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'gallery.html', {'products': products})


class UserProfileView(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None
            products = []
            return render(request, 'profile.html', {'error': 'User not found', 'products': products})

        products = Product.objects.filter(user=user)
        return render(request, 'profile.html', {'user': user, 'products': products})



class AddCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'addcategory.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST,request.FILES)
        if not form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('shop:categories')
        else:
            messages.error(request, 'Error adding category. Please try again.')
            form = CategoryForm()
            return render(request, 'addcategory.html', {'form': form})

class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('shop:products')
        else:
            messages.error(request, 'Error adding product. Please try again.')
            form = ProductForm()
            return render(request, 'add_product.html', {'form': form})

class HelloView(View):
    def get(self, request):
        return render(request, 'hello.html', {'message': 'Hello, World!'})
