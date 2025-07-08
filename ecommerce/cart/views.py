from http.client import responses

from django.shortcuts import render, redirect
from django.views import View
from cart.models import Cart, Order_item
from pyexpat.errors import messages
from shop.models import Product
from cart.forms import OrderForm
import razorpay
from django.contrib import messages


class AddToCartView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('cart:cartview')


class CartView(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            item.subtotal = item.product.price * item.quantity

        total = sum(item.subtotal for item in cart_items)

        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total': total,
        })


class Cart_decrementView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        try:
            cart_item = Cart.objects.get(user=user, product=product)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except Cart.DoesNotExist:
            pass
        return redirect('cart:cartview')


class CartremoveView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        Cart.objects.filter(user=user, product=product).delete()
        return redirect('cart:cartview')


def check_stock(cart_items):
    stock = True
    for item in cart_items:
        if item.product.stock < item.quantity:
            stock = False
            break
    return stock

class OrderFormView(View):
    def get(self, request):
        form = OrderForm()
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)

        return render(request, 'orderform.html', {
            'form': form,
            'cart_items': cart_items,
            'total': total,
        })

    def post(self, request):
        form = OrderForm(request.POST)
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.product.price * item.quantity for item in cart_items)
        response_payment = None  # Initialize to avoid UnboundLocalError

        stock = check_stock(cart_items)

        if stock:
            # Validate the form and check if there are items in the cart
            if form.is_valid() and cart_items.exists():
                order = form.save(commit=False)
                order.user = user
                order.amount = total
                order.save()

                for item in cart_items:
                    Order_item.objects.create(order=order, product=item.product, quantity=item.quantity)

                if order.payment_method == 'razorpay':
                    client = razorpay.Client(auth=('rzp_test_UOrEDbUenBCHmF', 'oc4EoEFImxmRz078wqktzCNG'))
                    response_payment = client.order.create(dict(amount=int(total * 100), currency='INR'))
                    print(response_payment)

                    order.order_id = response_payment['id']
                    order.is_ordered = False
                    order.save()

                elif order.payment_method == 'cod':
                    order.is_ordered = True
                    order.save()
                    response_payment = {'id':'cod_payment','status': 'success'}
                    Cart.objects.filter(user=user).delete()
                    return render(request, 'paymentsuccess.html', {'payment':response_payment,'name': user.username})
                else:
                    pass

                return render(request, 'payment.html', {'payment': response_payment,'name':user.username})
        else:
            messages.error(request,"Currently item not available in stock")
            return render(request,'payment.html')

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.views import View
from cart.models import Order, Order_item
from authentication.models import CustomUser

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(View):
    def post(self, request, pk):

        # Validate the request method
        user = CustomUser.objects.get(username=pk)
        login(request, user)

        # Get the response from Razorpay
        response = request.POST
        print(response)

        # Validate the response from Razorpay
        order = Order.objects.get(order_id=responses['razorpay_order_id'])
        order.is_ordered = True
        order.save()

        # Update stock for each product in the order
        items = Order_item.objects.filter(order=order)
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart for the user after successful payment
        Cart.objects.filter(user=user).delete()

        return render(request, 'paymentsuccess.html')

class OrderSummaryView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user, is_ordered=True).prefetch_related('items__product').order_by('-id')
        return render(request, 'ordersummary.html', {'orders': orders})
