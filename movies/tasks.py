from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_order_notification(order_id):
    """Send Telegram notification for new order"""
    try:
        from .models import Orders
        order = Orders.objects.get(id=order_id)
        
        payment_types = {
            1: "наличными, не оплачен",
            3: "Payme",
            4: "Click", 
            5: "Humo & Uzcard"
        }
        
        payment_text = payment_types.get(order.payment_type, "Payment Online")
        
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
        
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', 'bot_token')
        chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '-chat_id')
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            "reply_markup": json.dumps(keyboard)
        }
        
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
        
    except Exception as e:
        logger.error(f"Error sending order notification: {e}")
        return False


@shared_task
def send_email_notification(subject, message, recipient_list):
    """Send email notification"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


@shared_task
def update_product_cache(product_id):
    """Update product cache after changes"""
    try:
        from .models import Products
        from .serializers import ProductsDataSerializer
        
        product = Products.objects.select_related(
            'categoty_id', 'brand', 'product_type_id'
        ).get(id=product_id)
        
        serializer = ProductsDataSerializer(product)
        cache_key = f'product_detail_{product_id}'
        cache.set(cache_key, serializer.data, 60 * 30)  # 30 minutes
        
        return True
    except Exception as e:
        logger.error(f"Error updating product cache: {e}")
        return False


@shared_task
def cleanup_old_data():
    """Clean up old data periodically"""
    try:
        from .models import SearchStory
        from django.utils import timezone
        from datetime import timedelta
        
        # Remove old search stories (older than 90 days)
        old_searches = SearchStory.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=90)
        )
        deleted_count = old_searches.count()
        old_searches.delete()
        
        logger.info(f"Cleaned up {deleted_count} old search records")
        return deleted_count
        
    except Exception as e:
        logger.error(f"Error cleaning up old data: {e}")
        return 0


@shared_task
def generate_product_recommendations(user_id):
    """Generate product recommendations for user"""
    try:
        from .models import Clients, Orders, OrderProduct, Products
        
        user_orders = Orders.objects.filter(user_id=user_id)
        order_products = OrderProduct.objects.filter(order__in=user_orders)
        product_ids = order_products.values_list('product_id', flat=True)
        
        if not product_ids:
            return []
        
        ordered_products = Products.objects.filter(id__in=product_ids)
        
        # Get similar products by brand and category
        brands = ordered_products.values_list('brand_id', flat=True)
        categories = ordered_products.values_list('categoty_id', flat=True)
        
        recommendations = Products.objects.filter(
            models.Q(brand_id__in=brands) | models.Q(categoty_id__in=categories)
        ).exclude(id__in=product_ids).distinct()[:10]
        
        cache_key = f'user_recommendations_{user_id}'
        cache.set(cache_key, list(recommendations.values_list('id', flat=True)), 60 * 60)  # 1 hour
        
        return list(recommendations.values_list('id', flat=True))
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return []