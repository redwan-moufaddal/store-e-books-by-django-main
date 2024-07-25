
from .models import Cart,Product


def cart(request):
    cart_items = Cart.objects.filter(user=request.user.id)  # Get all cart items for the current user
    products1 = []  
    price = []
    for item in cart_items:
        products1.append(item.product)
        price.append(item.product.price_new)
    somme = sum(price)
    count_item = len(products1)
    return {'sum1':somme,'products1':products1,'count_item':count_item}

