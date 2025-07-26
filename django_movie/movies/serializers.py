from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from PIL import Image
from collections import defaultdict
from io import BytesIO
import requests

from .models import ProductColor, MobileDocuments, Promo, NotificationToken, Category, Products, ProductBundle, Hairtype, Slider, Review, Skintype, Forwhom, MainPage,New,ProductType, Clients, Orders, Brand, OrderProduct, Actual, Stories



class QuillFieldSerializer(serializers.Field):
    def to_representation(self, value):
        return value.html if value else ""

    def to_internal_value(self, data):
        return data  # assumes data is HTML
        
class PromoSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = "__all__"
        
class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = "__all__"

class ForwhomSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Forwhom
        fields = "__all__"
        
class NotificationTokenSeralizer(serializers.ModelSerializer):
    class Meta:
        model = NotificationToken
        fields = "__all__"

class SkintypeSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Skintype
        fields = "__all__"
        
class HairtypeSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Hairtype
        fields = "__all__"


class BrandSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        
class ClientsSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"
        
class ReviewSeralizer(serializers.ModelSerializer):
    user = ClientsSeralizer(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"
        
class ReviewAddSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        






class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        

class MobileDocumentsDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MobileDocuments
        fields = "__all__"
        
        
class ProductTypeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"
        
class ProductsData2Serializer(serializers.ModelSerializer):
    product_color = ProductColorSerializer(read_only=True)
    class Meta:
        model = Products
        fields = "__all__"
        
class ProductBundleDataSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductBundle
        fields = "__all__"

    def get_products(self, obj):
        products = Products.objects.filter(product_bundle_id=obj.id)
        return ProductsData2Serializer(products, many=True).data
        
class ProductsDataSerializer(serializers.ModelSerializer):
    product_type_id = ProductTypeDataSerializer(read_only=True)
    brand = BrandSeralizer(read_only=True)
    for_whom_id = ForwhomSeralizer(read_only=True)
    product_color = ProductColorSerializer(read_only=True)
    hair_type_id = HairtypeSeralizer(read_only=True)
    skin_type_id = SkintypeSeralizer(read_only=True)
    reviews = ReviewSeralizer(many=True, read_only=True) 
    product_bundle_id = ProductBundleDataSerializer(read_only=True) 
    class Meta:
        model = Products
        fields = "__all__"
        
class OrderProductDetailSeralizer(serializers.ModelSerializer):
    product = ProductsDataSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"
        
class OrderMobileUserSeralizer(serializers.ModelSerializer):
    product = ProductsDataSerializer(read_only=True)
    class Meta:
        model = Orders
        fields = "__all__"

        


        

        
        
class ActualDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Actual
        fields = "__all__"
        
class StoriesDetailSeralizer(serializers.ModelSerializer):
    actual_id = ActualDetailSeralizer(read_only=True)
    class Meta:
        model = Stories
        fields = "__all__"

class OrderProductSeralizer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = "__all__"
        


        
class SliderDataSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    product = ProductsDataSerializer(read_only=True)

    class Meta:
        model = Slider
        fields = "__all__"  # Или перечисли явно, если хочешь
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_colors(self, obj):
        try:
            # Полный URL изображения
            request = self.context.get('request')
            if request:
                image_url = request.build_absolute_uri(obj.image.url)
            else:
                image_url = obj.image.url

            # Загружаем изображение
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content)).convert("RGB")

            # Считаем цвета
            by_color = defaultdict(int)
            for pixel in image.getdata():
                by_color[pixel] += 1

            # Сортируем и возвращаем топ-5
            top_colors = sorted(by_color.items(), key=lambda x: x[1], reverse=True)[:1]
            return [color for color, count in top_colors]
        
        except Exception as e:
            print("⚠️ Ошибка при анализе цвета:", e)
            return []
        
class MainPageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPage
        fields = "__all__"
        
class OrdersDetailSeralizer(serializers.ModelSerializer):
    user_id  = ClientsSeralizer(read_only=True)
    class Meta:
        model = Orders
        fields = "__all__"
        
class OrdersSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = "__all__"
        

class OrderUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class NewDataSerializer(serializers.ModelSerializer):
    
    products = ProductsDataSerializer(read_only=True, many=True)
    

    

    
    class Meta:
        model = New
        fields = "__all__"
        