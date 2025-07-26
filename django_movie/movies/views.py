from django.db import models
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import requests
from django.conf import settings

import json

import urllib.parse

from django.shortcuts import get_object_or_404

from rest_framework import viewsets



from .models import Category,Promo,  NotificationToken, MobileDocuments, Products, Slider,Review, MainPage, New, Clients, Orders, Brand, OrderProduct, Stories

from .serializers import (
    CategoryDataSerializer,
    ProductsDataSerializer,
    SliderDataSerializer,
    MainPageDataSerializer,
    NewDataSerializer,
    ClientsSeralizer,
    OrdersSeralizer,
    OrderProductSeralizer,
    BrandSeralizer,
    OrderProductDetailSeralizer,
    OrdersDetailSeralizer,
    OrderUserSeralizer,
    StoriesDetailSeralizer,
    ReviewSeralizer,
    ReviewAddSeralizer,
    MobileDocumentsDataSerializer,
    OrderMobileUserSeralizer,
    NotificationTokenSeralizer,
    PromoSeralizer
)


class ChangeStatePromoByID(APIView):
    def post(self, request, *args, **kwargs):
        promo_id = request.data.get('promo_id')
        new_status = request.data.get('status')

        if not promo_id or new_status is None:
            return Response({'error': 'promo_id и status обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        promo = get_object_or_404(Promo, id=promo_id)
        promo.status = new_status
        promo.save()

        return Response({'success': True, 'message': f'Промо #{promo_id} обновлено', 'new_status': promo.status}, status=status.HTTP_200_OK)

class CheckPromoByIdNumberView(APIView):
    def post(self, request):
        id_number = request.data.get('id_number')
        if not id_number:
            return Response(
                {"valid": False, "error": "Поле 'id_number' обязательно"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            promo = Promo.objects.get(id_number=id_number)
            if promo.status == 1:
                return Response({
                    "id": promo.id,
                    "valid": True,
                    "name": promo.name,
                    "promo_type": promo.promo_type,
                    "promo_sum": promo.promo_sum,
                    "promo_percent": promo.promo_percent,
                    "promo_usage_type": promo.promo_usage_type
                })
            else:
                return Response({
                    "valid": False,
                    "error": "Промо найден, но он неактивен"
                })
        except Promo.DoesNotExist:
            return Response({
                "valid": False,
                "error": "Промо с таким ID не найден"
            }, status=status.HTTP_404_NOT_FOUND)

class EditPromoSeralizerSeralizerCreateView(generics.RetrieveUpdateDestroyAPIView):
    """Dobativ tip"""
    queryset = Promo.objects.all()
    serializer_class = PromoSeralizer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('product')
    serializer_class = ReviewAddSeralizer
    
    
class AddNotificationToket(generics.ListCreateAPIView):
    """Создание или обновление NotificationToken по token"""
    queryset = NotificationToken.objects.all()
    serializer_class = NotificationTokenSeralizer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        token = data.get('token')

        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Обработка client_id
        client_id = data.get('client_id')
        if client_id:
            try:
                client_instance = Clients.objects.get(id=client_id)
                data['client_id'] = client_instance
            except Clients.DoesNotExist:
                return Response({'error': 'Client not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['client_id'] = None

        # Обновляем или создаем
        instance, created = NotificationToken.objects.update_or_create(
            token=token,
            defaults={
                'phone_brand': data.get('phone_brand', ''),
                'os_name': data.get('os_name', ''),
                'client_id': data.get('client_id'),
            }
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
class NotificationTokenAlllView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = NotificationToken.objects.all()
    serializer_class = NotificationTokenSeralizer

class NotificationTokenUserView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = NotificationTokenSeralizer
    def get_queryset(self):
        return NotificationToken.objects.filter(client_id=self.kwargs['pk'])

class ReviewUserDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ReviewAddSeralizer
    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['pk'], user=self.kwargs['pk2'])

class ReviewDetaiAlllView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Review.objects.all()
    serializer_class = ReviewSeralizer     
        
class ReviewDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ReviewSeralizer
    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['pk'])
        
class NewDetaiIDlView(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = NewDataSerializer
    def get_queryset(self):
        return New.objects.filter(id=self.kwargs['pk'])
        
class AddReviewSeralizerCreateView(generics.ListCreateAPIView):
    """Dobativ tip"""
    queryset = Review.objects.all()
    serializer_class = ReviewAddSeralizer
    
class EditReviewSeralizerCreateView(generics.RetrieveUpdateDestroyAPIView):
    """Dobativ tip"""
    queryset = Review.objects.all()
    serializer_class = ReviewAddSeralizer

class OrderUserDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrderUserSeralizer
    def get_queryset(self):
        return Orders.objects.filter(user_id=self.kwargs['pk'])
        
class OrderUserMobileDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrderMobileUserSeralizer
    def get_queryset(self):
        return Orders.objects.filter(user_id=self.kwargs['pk'])

class OrdersProductDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrderProductDetailSeralizer
    def get_queryset(self):
        return OrderProduct.objects.filter(order_id=self.kwargs['pk'])
        
        
class OrdersUserProductDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrderProductDetailSeralizer
    def get_queryset(self):
        return OrderProduct.objects.filter(order_id=self.kwargs['pk'])

class BrandDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Brand.objects.all()
    serializer_class = BrandSeralizer
    
class MobileDocumentsDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = MobileDocuments.objects.all()
    serializer_class = MobileDocumentsDataSerializer
    

class AllOrdersDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Orders.objects.all()
    serializer_class = OrdersDetailSeralizer
    
    
class OrdersDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrdersDetailSeralizer
    def get_queryset(self):
        return Orders.objects.filter(status=self.kwargs['pk'])
        
        
class OrdersMDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = OrdersDetailSeralizer
    def get_queryset(self):
        return Orders.objects.filter(id=self.kwargs['pk'])
        



class AddOrdersSeralizerCreateView(generics.ListCreateAPIView):
    """Dobativ tip"""
    queryset = Orders.objects.all()
    serializer_class = OrdersSeralizer
    
    def perform_create(self, serializer):
        order = serializer.save()
        
        # Примерные данные:
        payment_type = order.payment_type  # 1 = нал, 3 = Payme, 4 = Click
        order_status = 1  # 1 = ожидание, 2 = оплачено, 3 = ошибка
        
        # Тип оплаты
        if payment_type == 1:
            payment_text = "наличными, не оплачен"
        elif payment_type == 3:
            if order_status == 1:
                payment_text = "Payme (ожидание оплаты)"
            elif order_status == 2:
                payment_text = "Payme (оплачено)"
            else:
                payment_text = "Payme (оплата не прошла)"
        elif payment_type == 4:
            if order_status == 1:
                payment_text = "Click (ожидание оплаты)"
            elif order_status == 2:
                payment_text = "Click (оплачено)"
            else:
                payment_text = "Click (оплата не прошла)"
                
        elif payment_type == 5:
            if order_status == 1:
                payment_text = "Humo & Uzcard (ожидание оплаты)"
            elif order_status == 2:
                payment_text = "Humo & Uzcard (оплачено)"
            else:
                payment_text = "Humo & Uzcard (оплата не прошла)"
        else:
            payment_text = "Payment Online"


        # Здесь формируем текст сообщения
        message = (
            f"<b>Новый заказ!</b>\n\n"
            f"<b>Номер заказа:</b> {order.id}\n"
            f"<b>Клиент:</b> {order.name} {order.surname}\n"
            f"<b>Адрес:</b> {order.adress}\n"
            f"<b>Сумма:</b> {order.all_sum} сум\n"
            f"<b>Доставка:</b> {order.delivery_sum} сум\n"
            f"<b>Оплата:</b> {payment_text}\n"
            f"<b>Дата доставки:</b> {order.delivery_date}\n"
            f"<b>Телефон:</b> {order.phone}"
        )
        
 
        
        
        order_url = f"http://osmaadmin.academytable.ru/order_product_server/{order.id}/{order.status}/"
        
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "Открыть заказ",
                        "url": order_url
                    }
                ]
            ]
        }
        
        # Данные Telegram
        bot_token = 'bot_token'
        chat_id = '-chat_id'

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            "reply_markup": json.dumps(keyboard)
        }

        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")
    
class AddOrderProductSeralizerSeralizerCreateView(generics.ListCreateAPIView):
    """Dobativ tip"""
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSeralizer
    
class EditProductSeralizerSeralizerCreateView(generics.RetrieveUpdateDestroyAPIView):
    """Dobativ tip"""
    queryset = Products.objects.all()
    serializer_class = ProductsDataSerializer
    
    
class UpdateProductStockView(APIView):
    """Увеличить или уменьшить stock товара"""

    def patch(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        change = request.data.get("change")

        if change is None or not isinstance(change, int):
            return Response({"error": "Передайте числовое значение 'change'"}, status=status.HTTP_400_BAD_REQUEST)

        product.stock += change
        product.save()
        return Response({"id": product.id, "new_stock": product.stock}, status=status.HTTP_200_OK)
        
#   queryset = Products.objects.all()
#     serializer_class = ProductsDataSerializer


class AddUserCreateView(generics.ListCreateAPIView):
    """Добавить клиента"""
    queryset = Clients.objects.all()
    serializer_class = ClientsSeralizer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if phone:
            try:
                client = Clients.objects.get(phone=phone)
                serializer = self.get_serializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Clients.DoesNotExist:
                return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)


class ClientEditDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Редактировать клиента по ID"""
    queryset = Clients.objects.all()
    serializer_class = ClientsSeralizer
    
    
class OrderEditDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersDetailSeralizer


class UserAllDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Clients.objects.all()
    serializer_class = ClientsSeralizer

class UserIDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ClientsSeralizer
    def get_queryset(self):
        return Clients.objects.filter(id=self.kwargs['pk'])

class UserPhoneDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ClientsSeralizer
    def get_queryset(self):
        # Clean the phone number (remove spaces)
        phone = self.kwargs['pk'].replace('%20', ' ')  # Removing spaces from the phone number
        return Clients.objects.filter(phone=phone)

# class AddUserCreateView(generics.ListCreateAPIView):
#     """Dobativ tip"""
#     queryset = Clients.objects.all()
#     serializer_class = ClientsSeralizer

class NewDetailView(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = New.objects.all()
    serializer_class = NewDataSerializer
    

class StoriesetailView(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Stories.objects.all()
    serializer_class = StoriesDetailSeralizer

class SliderDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Slider.objects.all()
    serializer_class = SliderDataSerializer
    

class StoriesDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Slider.objects.all()
    serializer_class = SliderDataSerializer

class MainPageDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = MainPage.objects.all()
    serializer_class = MainPageDataSerializer


class CategorytDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Category.objects.all()
    serializer_class = CategoryDataSerializer
    
class ProductsDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['title_ru', 'title_uz', 'brand__name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Products.objects.all()
    serializer_class = ProductsDataSerializer
    
class ProductsIDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    def get_queryset(self):
        return Products.objects.filter(id=self.kwargs['pk'])
        
        
    
class ProductsCategoryIDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    def get_queryset(self):
        # Get the 'category_id' from the URL (or query parameters, as needed)
        category_ids = self.kwargs.get('pk', None)
        
        if category_ids:
            # Check if category_ids is a single integer or a comma-separated string
            if isinstance(category_ids, str):
                # If it's a string, split by commas to get multiple category IDs
                category_ids = category_ids.split(',')
            else:
                # If it's a single integer, make it a list
                category_ids = [category_ids]
            
            # Convert the category_ids into integers to ensure we are working with valid IDs
            category_ids = [int(id) for id in category_ids]

            # Change `category_id` to `category__id` if `category` is a foreign key field
            return Products.objects.filter(categoty_id__id__in=category_ids)

        return Products.objects.all()
        
        
class ProductsBrandIDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    def get_queryset(self):
        return Products.objects.filter(brand=self.kwargs['pk'])
        
class ProductsBandleDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    def get_queryset(self):
        return Products.objects.filter(product_bundle_id=self.kwargs['pk'])
        
class ProductsTopIDDetailView(generics.ListAPIView):
    """Vvidvod predmetov"""
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    def get_queryset(self):
        return Products.objects.filter(top_type_id=self.kwargs['pk'])
        
        
class OrderRecommendationsAPIView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Orders, id=order_id)
        order_products = OrderProduct.objects.filter(order=order)

        # Собираем все ID заказанных продуктов
        product_ids = order_products.values_list('product_id', flat=True)
        ordered_products = Products.objects.filter(id__in=product_ids)

        # --- Первая группа: Дешевые товары (дополнения)
        cheap_recommendations = Products.objects.filter(price__gte=45000, price__lte=150000).exclude(id__in=product_ids).order_by('?')[:3]

        # --- Вторая группа: Схожие по бренду или категории
        brands = ordered_products.values_list('brand_id', flat=True)
        categories = ordered_products.values_list('categoty_id', flat=True)
        similar_recommendations = Products.objects.filter(
            models.Q(brand_id__in=brands) | models.Q(categoty_id__in=categories)
        ).exclude(id__in=product_ids).order_by('?')[:3]

        # --- Третья группа: Популярные/бестселлеры
        top_recommendations = Products.objects.filter(top_type_id=1).exclude(id__in=product_ids).order_by('?')[:3]

        data = {
            "cheap_add_ons": ProductsDataSerializer(cheap_recommendations, many=True).data,
            "similar_items": ProductsDataSerializer(similar_recommendations, many=True).data,
            "bestsellers": ProductsDataSerializer(top_recommendations, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)
        
        
class UserRecommendationsAPIView(APIView):
    def get(self, request, user_id):
        # Получаем все продукты, заказанные этим пользователем
        user_orders = Orders.objects.filter(user_id=user_id)
        order_products = OrderProduct.objects.filter(order__in=user_orders)
        product_ids = order_products.values_list('product_id', flat=True)

        if not product_ids.exists():
            return Response({
                "message": "Пользователь еще не делал заказы",
                "cheap_add_ons": [],
                "similar_items": [],
                "bestsellers": []
            })

        ordered_products = Products.objects.filter(id__in=product_ids)

        # Дешевые товары (не заказанные ранее)
        cheap_add_ons = Products.objects.filter(price__gte=45000, price__lte=150000).exclude(id__in=product_ids).order_by('?')[:3]

        # Похожие товары по бренду или категории
        brands = ordered_products.values_list('brand_id', flat=True)
        categories = ordered_products.values_list('categoty_id', flat=True)

        similar_items = Products.objects.filter(
            models.Q(brand_id__in=brands) | models.Q(categoty_id__in=categories)
        ).exclude(id__in=product_ids).distinct().order_by('?')[:3]

        # Часто покупаемые (по флагу, например top_type_id=1)
        bestsellers = Products.objects.filter(top_type_id=1).exclude(id__in=product_ids).order_by('?')[:3]

        data = {
            "cheap_add_ons": ProductsDataSerializer(cheap_add_ons, many=True).data,
            "similar_items": ProductsDataSerializer(similar_items, many=True).data,
            "bestsellers": ProductsDataSerializer(bestsellers, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)


    
    
# class SubjectIDDetailView(generics.ListAPIView):
#     """Vvidvod predmetov"""
#     search_fields = ['name']
#     filter_backends = (filters.SearchFilter, filters.OrderingFilter)
#     serializer_class = TimetableSerializer
#     ordering = ('end_date')
#     pagination_class = LargeResultsSetPagination
#     def get_queryset(self):
#         return Timetable.objects.filter(group_id=self.kwargs['pk'])


# from .serializers import (
#     GendersDataSerializer,
# )



# class GendersCreateView(generics.ListCreateAPIView):
#     queryset = Genders.objects.all()
#     serializer_class = GendersDataSerializer

