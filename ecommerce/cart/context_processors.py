from cart.models import Cart

def count_items(request):
    """
    Context processor to count the number of items in the user's cart.
    """
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        item_count = 0
        for item in cart_items:
            item_count += item.quantity
    else:
        item_count = 0
    return {'item_count': item_count}