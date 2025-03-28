from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, count):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': count,
                                       'price': str(product.price)}
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def remove(self, product, count):
        product_id = str(product.id)
        if product_id in self.cart:
            if count == 1 and self.cart[product_id]['count'] > 1:
                self.cart[product_id]['count'] -= int(count)
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(
            id__in=products_ids
        )
        cart = self.cart.copy()
        for product in products:
            self.cart[str(products.id)]['product'] =  product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
            yield item

    def total_count(self):
        return sum(item['count'] for item in self.cart.values())
    
    def total_price(self):
        return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True