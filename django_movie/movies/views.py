from django.db import models
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics, filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q, Count, Avg
import requests
from django.conf import settings
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)



from .models import (
    Category, Promo, NotificationToken, MobileDocuments, Products, ProductVariant,
    Slider, Review, MainPage, New, Clients, Orders, Brand, OrderProduct, Stories,
    Manufacturer, MaterialType, MaterialGrade, TechnicalStandard, ApplicationArea,
    EquipmentType, UnitOfMeasure
)

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
    PromoSeralizer,
    # Building Materials Serializers
    MaterialTypeSerializer,
    MaterialGradeSerializer,
    TechnicalStandardSerializer,
    ApplicationAreaSerializer,
    EquipmentTypeSerializer,
    UnitOfMeasureSerializer,
    ManufacturerSerializer,
    ProductVariantSerializer,
    ProductVariantCreateSerializer,
    BuildingMaterialsProductSerializer,
    BuildingMaterialsProductCreateSerializer,
    MaterialTypeListSerializer,
    EquipmentTypeListSerializer,
    ManufacturerListSerializer,
    ProductListSerializer,
    ProductStatsSerializer,
    InventoryReportSerializer
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
    serializer_class = ReviewAddSeralizer
    
    def get_queryset(self):
        return Review.objects.select_related('product', 'user').filter(is_approved=True)
    
    def perform_create(self, serializer):
        try:
            serializer.save()
            # Clear related caches
            if serializer.instance.product:
                cache.delete(f'product_reviews_{serializer.instance.product.id}')
        except Exception as e:
            logger.error(f"Error creating review: {e}")
            raise
    
    
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
    """Optimized order creation view"""
    serializer_class = OrdersSeralizer
    
    def get_queryset(self):
        return Orders.objects.select_related('user_id').order_by('-created_at')
    
    def perform_create(self, serializer):
        try:
            order = serializer.save()
            
            # Send notification asynchronously (if Celery is available)
            self._send_order_notification(order)
            
            # Clear related caches
            if order.user_id:
                cache.delete(f'user_orders_{order.user_id.id}')
                
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
    
    def _get_payment_text(self, payment_type, order_status=1):
        """Get payment type description"""
        payment_types = {
            1: "наличными, не оплачен",
            3: {
                1: "Payme (ожидание оплаты)",
                2: "Payme (оплачено)",
                3: "Payme (оплата не прошла)"
            },
            4: {
                1: "Click (ожидание оплаты)",
                2: "Click (оплачено)",
                3: "Click (оплата не прошла)"
            },
            5: {
                1: "Humo & Uzcard (ожидание оплаты)",
                2: "Humo & Uzcard (оплачено)",
                3: "Humo & Uzcard (оплата не прошла)"
            }
        }
        
        if payment_type == 1:
            return payment_types[1]
        elif payment_type in [3, 4, 5]:
            return payment_types[payment_type].get(order_status, "Payment Online")
        else:
            return "Payment Online"
    
    def _send_order_notification(self, order):
        """Send Telegram notification for new order"""
        try:
            payment_text = self._get_payment_text(order.payment_type, 1)
            
            message = (
                f"<b>Новый заказ!</b>\n\n"
                f"<b>Номер заказа:</b> {order.id}\n"
                f"<b>Клиент:</b> {order.name} {order.surname}\n"
                f"<b>Адрес:</b> {order.address}\n"
                f"<b>Сумма:</b> {order.all_sum} сум\n"
                f"<b>Доставка:</b> {order.delivery_sum} сум\n"
                f"<b>Оплата:</b> {payment_text}\n"
                f"<b>Дата доставки:</b> {order.delivery_date}\n"
                f"<b>Телефон:</b> {order.phone}"
            )
            
            order_url = f"http://osmaadmin.academytable.ru/order_product_server/{order.id}/{order.status}/"
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Открыть заказ", "url": order_url}]
                ]
            }
            
            # Get from environment variables
            bot_token = settings.TELEGRAM_BOT_TOKEN if hasattr(settings, 'TELEGRAM_BOT_TOKEN') else 'bot_token'
            chat_id = settings.TELEGRAM_CHAT_ID if hasattr(settings, 'TELEGRAM_CHAT_ID') else '-chat_id'
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML',
                "reply_markup": json.dumps(keyboard)
            }
            
            # Send notification asynchronously
            requests.post(url, data=payload, timeout=10)
            
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
    
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
    
@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
@method_decorator(vary_on_headers('User-Agent'), name='dispatch')
class ProductsDetailView(generics.ListAPIView):
    """Optimized products list view with caching and query optimization"""
    search_fields = ['title_ru', 'title_uz', 'title_eng', 'brand__name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering_fields = ['price', 'created_at', 'title_ru']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'product_type_id',
            'material_type_id', 'material_grade_id', 'technical_standard_id',
            'application_area_id', 'equipment_type_id', 'unit_of_measure'
        ).prefetch_related(
            Prefetch('reviews', queryset=Review.objects.filter(is_approved=True)),
            Prefetch('variants', queryset=ProductVariant.objects.filter(is_available=True))
        ).filter(stock__gt=0, is_available=True)
    
@method_decorator(cache_page(60 * 30), name='dispatch')  # Cache for 30 minutes
class ProductsIDDetailView(generics.ListAPIView):
    """Optimized single product view"""
    serializer_class = ProductsDataSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['pk']
        cache_key = f'product_detail_{product_id}'
        
        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
            
        queryset = Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'product_type_id',
            'material_type_id', 'material_grade_id', 'technical_standard_id',
            'application_area_id', 'equipment_type_id', 'unit_of_measure'
        ).prefetch_related(
            Prefetch('reviews', queryset=Review.objects.filter(is_approved=True).select_related('user')),
            Prefetch('variants', queryset=ProductVariant.objects.filter(is_available=True))
        ).filter(id=product_id)
        
        # Cache the result
        cache.set(cache_key, queryset, 60 * 30)
        return queryset
        
        
    
@method_decorator(cache_page(60 * 10), name='dispatch')  # Cache for 10 minutes
class ProductsCategoryIDDetailView(generics.ListAPIView):
    """Optimized products by category view"""
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering = ['-created_at']
    
    def get_queryset(self):
        category_ids = self.kwargs.get('pk', None)
        
        if not category_ids:
            return Products.objects.none()
        
        try:
            # Handle comma-separated category IDs
            if isinstance(category_ids, str):
                category_ids = [int(id.strip()) for id in category_ids.split(',')]
            else:
                category_ids = [int(category_ids)]
            
            cache_key = f'products_category_{"_".join(map(str, category_ids))}'
            cached_result = cache.get(cache_key)
            
            if cached_result:
                return cached_result
            
            queryset = Products.objects.select_related(
                'categoty_id', 'brand', 'manufacturer', 'product_type_id',
                'material_type_id', 'equipment_type_id'
            ).filter(
                categoty_id__id__in=category_ids,
                stock__gt=0,
                is_available=True
            ).order_by('-created_at')
            
            # Cache the result
            cache.set(cache_key, queryset, 60 * 10)
            return queryset
            
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid category IDs: {category_ids}, error: {e}")
            return Products.objects.none()
        
        
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


class ProductsByMaterialTypeView(generics.ListAPIView):
    """Products filtered by material type"""
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering = ['-created_at']
    
    def get_queryset(self):
        material_type_id = self.kwargs.get('pk')
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'material_type_id'
        ).filter(
            material_type_id=material_type_id,
            stock__gt=0,
            is_available=True
        )

class ProductsByEquipmentTypeView(generics.ListAPIView):
    """Products filtered by equipment type"""
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering = ['-created_at']
    
    def get_queryset(self):
        equipment_type_id = self.kwargs.get('pk')
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'equipment_type_id'
        ).filter(
            equipment_type_id=equipment_type_id,
            stock__gt=0,
            is_available=True
        )

class ProductsByManufacturerView(generics.ListAPIView):
    """Products filtered by manufacturer"""
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering = ['-created_at']
    
    def get_queryset(self):
        manufacturer_id = self.kwargs.get('pk')
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer'
        ).filter(
            manufacturer=manufacturer_id,
            stock__gt=0,
            is_available=True
        )

class ProfessionalProductsView(generics.ListAPIView):
    """Professional grade products"""
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = ProductsDataSerializer
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer'
        ).filter(
            is_professional=True,
            stock__gt=0,
            is_available=True
        )

class LowStockProductsView(generics.ListAPIView):
    """Products with low stock levels"""
    serializer_class = ProductsDataSerializer
    ordering = ['stock']
    
    def get_queryset(self):
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer'
        ).filter(
            stock__lte=models.F('min_stock_level'),
            is_available=True
        )

class ProductVariantListView(generics.ListAPIView):
    """List variants for a specific product"""
    serializer_class = ProductVariantSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return ProductVariant.objects.select_related('product').filter(
            product_id=product_id,
            is_available=True
        )

# ============================================================================
# BUILDING MATERIALS CRUD API VIEWS
# ============================================================================

# MaterialType CRUD Views
class MaterialTypeListCreateView(generics.ListCreateAPIView):
    """List all material types or create a new one"""
    queryset = MaterialType.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MaterialTypeListSerializer
        return MaterialTypeSerializer

class MaterialTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a material type"""
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer

# MaterialGrade CRUD Views
class MaterialGradeListCreateView(generics.ListCreateAPIView):
    """List all material grades or create a new one"""
    queryset = MaterialGrade.objects.all()
    serializer_class = MaterialGradeSerializer

class MaterialGradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a material grade"""
    queryset = MaterialGrade.objects.all()
    serializer_class = MaterialGradeSerializer

# TechnicalStandard CRUD Views
class TechnicalStandardListCreateView(generics.ListCreateAPIView):
    """List all technical standards or create a new one"""
    queryset = TechnicalStandard.objects.all()
    serializer_class = TechnicalStandardSerializer

class TechnicalStandardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a technical standard"""
    queryset = TechnicalStandard.objects.all()
    serializer_class = TechnicalStandardSerializer

# ApplicationArea CRUD Views
class ApplicationAreaListCreateView(generics.ListCreateAPIView):
    """List all application areas or create a new one"""
    queryset = ApplicationArea.objects.all()
    serializer_class = ApplicationAreaSerializer

class ApplicationAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an application area"""
    queryset = ApplicationArea.objects.all()
    serializer_class = ApplicationAreaSerializer

# EquipmentType CRUD Views
class EquipmentTypeListCreateView(generics.ListCreateAPIView):
    """List all equipment types or create a new one"""
    queryset = EquipmentType.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EquipmentTypeListSerializer
        return EquipmentTypeSerializer

class EquipmentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an equipment type"""
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer

# UnitOfMeasure CRUD Views
class UnitOfMeasureListCreateView(generics.ListCreateAPIView):
    """List all units of measure or create a new one"""
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer

class UnitOfMeasureDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a unit of measure"""
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer

# Manufacturer CRUD Views
class ManufacturerListCreateView(generics.ListCreateAPIView):
    """List all manufacturers or create a new one"""
    search_fields = ['name', 'country_ru', 'country_uz', 'country_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['name']
    
    def get_queryset(self):
        return Manufacturer.objects.prefetch_related('products')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ManufacturerListSerializer
        return ManufacturerSerializer

class ManufacturerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a manufacturer"""
    queryset = Manufacturer.objects.prefetch_related('products')
    serializer_class = ManufacturerSerializer

# ProductVariant CRUD Views
class ProductVariantListCreateView(generics.ListCreateAPIView):
    """List all product variants or create a new one"""
    search_fields = ['variant_name_ru', 'variant_name_uz', 'variant_name_eng', 'sku']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_at']
    
    def get_queryset(self):
        return ProductVariant.objects.select_related('product').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductVariantSerializer
        return ProductVariantCreateSerializer

class ProductVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a product variant"""
    queryset = ProductVariant.objects.select_related('product')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'POST']:
            return ProductVariantCreateSerializer
        return ProductVariantSerializer

# Enhanced Products CRUD Views
class BuildingMaterialsProductListCreateView(generics.ListCreateAPIView):
    """List all building materials products or create a new one"""
    search_fields = [
        'title_ru', 'title_uz', 'title_eng', 'brand__name',
        'manufacturer__name', 'material_composition', 'sku'
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'material_type_id',
            'material_grade_id', 'technical_standard_id', 'application_area_id',
            'equipment_type_id', 'unit_of_measure'
        ).prefetch_related('variants', 'reviews').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return BuildingMaterialsProductCreateSerializer

class BuildingMaterialsProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a building materials product"""
    
    def get_queryset(self):
        return Products.objects.select_related(
            'categoty_id', 'brand', 'manufacturer', 'material_type_id',
            'material_grade_id', 'technical_standard_id', 'application_area_id',
            'equipment_type_id', 'unit_of_measure'
        ).prefetch_related('variants', 'reviews')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'POST']:
            return BuildingMaterialsProductCreateSerializer
        return BuildingMaterialsProductSerializer

# Specialized Product Views
class ProfessionalProductsListView(generics.ListAPIView):
    """List professional-grade products"""
    serializer_class = ProductListSerializer
    search_fields = ['title_ru', 'title_uz', 'title_eng']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(is_professional=True, is_available=True)

class FeaturedProductsListView(generics.ListAPIView):
    """List featured products"""
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(is_featured=True, is_available=True)

class NewArrivalsListView(generics.ListAPIView):
    """List new arrival products"""
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(is_new_arrival=True, is_available=True)

class OnSaleProductsListView(generics.ListAPIView):
    """List products on sale"""
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(is_on_sale=True, is_available=True)

# Inventory Management Views
class LowStockProductsListView(generics.ListAPIView):
    """List products with low stock"""
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(
            stock__lte=models.F('min_stock_level'),
            is_available=True
        ).order_by('stock')

class OutOfStockProductsListView(generics.ListAPIView):
    """List out of stock products"""
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        return Products.objects.select_related(
            'brand', 'manufacturer', 'categoty_id'
        ).filter(stock=0)

# Statistics and Reports Views
class ProductStatsView(APIView):
    """Get product statistics"""
    
    def get(self, request):
        stats = {
            'total_products': Products.objects.count(),
            'in_stock_products': Products.objects.filter(stock__gt=0).count(),
            'low_stock_products': Products.objects.filter(
                stock__lte=models.F('min_stock_level'), stock__gt=0
            ).count(),
            'professional_products': Products.objects.filter(is_professional=True).count(),
            'featured_products': Products.objects.filter(is_featured=True).count(),
            'total_categories': Category.objects.count(),
            'total_brands': Brand.objects.count(),
            'total_manufacturers': Manufacturer.objects.count(),
        }
        
        serializer = ProductStatsSerializer(stats)
        return Response(serializer.data)

class InventoryReportView(APIView):
    """Get inventory report"""
    
    def get(self, request):
        products = Products.objects.select_related('brand', 'manufacturer').all()
        
        inventory_data = []
        for product in products:
            if product.stock <= product.min_stock_level:
                status = 'Low Stock' if product.stock > 0 else 'Out of Stock'
            else:
                status = 'In Stock'
            
            inventory_data.append({
                'product_id': product.id,
                'title': product.title_ru or product.title_uz or product.title_eng,
                'current_stock': product.stock,
                'min_stock_level': product.min_stock_level,
                'stock_status': status,
                'last_updated': product.updated_at
            })
        
        serializer = InventoryReportSerializer(inventory_data, many=True)
        return Response(serializer.data)

# Bulk Operations Views
class BulkUpdateStockView(APIView):
    """Bulk update stock levels"""
    
    def post(self, request):
        updates = request.data.get('updates', [])
        
        if not updates:
            return Response(
                {'error': 'No updates provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_products = []
        
        for update in updates:
            product_id = update.get('product_id')
            new_stock = update.get('stock')
            
            if not product_id or new_stock is None:
                continue
            
            try:
                product = Products.objects.get(id=product_id)
                product.stock = new_stock
                product.save()
                updated_products.append({
                    'product_id': product_id,
                    'title': product.title_ru,
                    'new_stock': new_stock
                })
            except Products.DoesNotExist:
                continue
        
        return Response({
            'message': f'Updated {len(updated_products)} products',
            'updated_products': updated_products
        })

class BulkUpdatePricesView(APIView):
    """Bulk update product prices"""
    
    def post(self, request):
        updates = request.data.get('updates', [])
        
        if not updates:
            return Response(
                {'error': 'No updates provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_products = []
        
        for update in updates:
            product_id = update.get('product_id')
            new_price = update.get('price')
            
            if not product_id or new_price is None:
                continue
            
            try:
                product = Products.objects.get(id=product_id)
                product.price = new_price
                product.save()
                updated_products.append({
                    'product_id': product_id,
                    'title': product.title_ru,
                    'new_price': new_price
                })
            except Products.DoesNotExist:
                continue
        
        return Response({
            'message': f'Updated {len(updated_products)} products',
            'updated_products': updated_products
        })

