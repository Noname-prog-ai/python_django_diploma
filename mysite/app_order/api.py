from rest_framework.response import Response
from rest_framework.views import APIView
import json
from app_auth.models import ProfileUser
from app_order.models import Order, Basket
from app_order.serializers import OrderSerializer, PaymentSerializer, UpdateOrdersSerializer
from app_shop.models import Product
from app_order.serializers import BasketSerializer, BasketUpdateSerializer


class BasketListView(APIView):
    def get(self, request):
        basket = Basket.objects.all()
        out = list()
        for bask in basket:
            prod = Product.objects.filter(id=bask.product_id).first()
            prod.count = bask.count
            serializer = BasketSerializer(prod)
            out.append(serializer.data)
        return Response(out)

    def post(self, request):
        serializer = BasketUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            basket = Basket.objects.filter(product_id=serializer.data["id"]).first()
            price = Product.objects.filter(id=serializer.data["id"]).first().price

            new_prod, created = Basket.objects.update_or_create(
                defaults={"count": serializer.data["count"], "price": price},
                product_id=serializer.data["id"],
            )
            if not created:
                basket.count = basket.count + serializer.data["count"]
                basket.save()

            basket = Basket.objects.all()
            out = list()
            for bask in basket:
                prod = Product.objects.filter(id=bask.product_id).first()
                prod.count = bask.count
                serializer = BasketSerializer(prod)
                out.append(serializer.data)
            return Response(out, status=200)
        return Response(data=serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        serializer = BasketUpdateSerializer(data=body)
        if serializer.is_valid(raise_exception=True):
            basket = Basket.objects.filter(product_id=serializer.data["id"]).first()

            if basket.count == serializer.data["count"]:
                print("delete ", serializer.data["id"])
                Basket.objects.filter(product_id=serializer.data["id"]).delete()
            else:
                basket.count = basket.count - serializer.data["count"]
                basket.save()

            basket = Basket.objects.all()
            out = list()
            for bask in basket:
                prod = Product.objects.filter(id=bask.product_id).first()
                prod.count = bask.count
                serializer = BasketSerializer(prod)
                out.append(serializer.data)
            return Response(out, status=200)
        return Response(data=serializer.errors, status=400)


class OrderCreateView(APIView):
    def get(self, request):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BasketSerializer(data=request.data, many=True)

        if serializer.is_valid(raise_exception=True):
            profile = ProfileUser.objects.get(pk=self.request.user.pk)
            # print(profile)
            basket = Basket.objects.all()
            totalCost = 0
            for prod in basket:
                totalCost += prod.price * prod.count

            new_order = Order.objects.create(
                user=profile,
                fullName=profile.fullName,
                email=profile.email,
                phone=profile.phone,
                totalCost=totalCost,
            )
            # print(serializer.data)

            for prod in basket:
                new_order.products.add(prod.product)

            payload = {"orderId": new_order.id}
            return Response(payload, status=200)
        return Response(data=serializer.errors, status=400)


class OrdersView(APIView):
    def get(self, request, pk):
        order = Order.objects.filter(id=pk).first()
        serializer = OrderSerializer(order)

        od = serializer.data["products"]

        for elem in od:
            count = Basket.objects.filter(product_id=elem.get("id")).first()
            elem.update({"count": count.count})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = UpdateOrdersSerializer(data=request.data)

        if serializer.is_valid():
            order = Order.objects.filter(id=pk).first()
            order.deliveryType = serializer.data["deliveryType"]
            order.address = serializer.data["address"]
            order.city = serializer.data["city"]
            order.email = serializer.data["email"]
            order.fullName = serializer.data["fullName"]
            order.paymentType = serializer.data["paymentType"]
            order.phone = serializer.data["phone"]
            order.status = serializer.data["status"]
            order.totalCost = serializer.data["totalCost"]
            order.save()

        payload = {"orderId": pk}
        return Response(payload, status=200)


class PaymentListView(APIView):
    def post(self, request, pk):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        Basket.objects.all().delete()
            # return Response(status=200)
        return Response(status=200)
