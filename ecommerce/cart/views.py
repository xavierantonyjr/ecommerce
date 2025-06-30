from django.shortcuts import render, redirect
from django.views import View


class AddToCartView(View):
    def get(self, request, pk):
        cart_items = request.session.get('cart_items', [])
        cart_items.append(pk)
        request.session['cart_items'] = cart_items
        return redirect('cart:cart')

class CartView(View):
    def get(self, request):
        cart_items = request.session.get('cart_items', [])
        context = {
            'cart_items': cart_items
        }
        return render(request, 'cart.html', context)