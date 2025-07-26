from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

from PIL import Image
from collections import defaultdict
from io import BytesIO
import requests

from .models import (
    ProductColor, MobileDocuments, Promo, NotificationToken, Category, Products,
    ProductBundle, Slider, Review, MainPage, New, ProductType, Clients, Orders,
    Brand, OrderProduct, Actual, Stories, ProductVariant,
    # New building materials models
    MaterialType, MaterialGrade, TechnicalStandard, ApplicationArea,
    EquipmentType, UnitOfMeasure, Manufacturer
)



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

# class ForwhomSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model = Forwhom
#         fields = "__all__"
        
class NotificationTokenSeralizer(serializers.ModelSerializer):
    class Meta:
        model = NotificationToken
        fields = "__all__"

# class SkintypeSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model = Skintype
#         fields = "__all__"
        
# class HairtypeSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model = Hairtype
#         fields = "__all__"


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
    # for_whom_id = ForwhomSeralizer(read_only=True)
    product_color = ProductColorSerializer(read_only=True)
    # hair_type_id = HairtypeSeralizer(read_only=True)
    # skin_type_id = SkintypeSeralizer(read_only=True)
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

# ============================================================================
# BUILDING MATERIALS SERIALIZERS
# ============================================================================

class MaterialTypeSerializer(serializers.ModelSerializer):
    """Serializer for MaterialType model"""
    class Meta:
        model = MaterialType
        fields = "__all__"

class MaterialGradeSerializer(serializers.ModelSerializer):
    """Serializer for MaterialGrade model"""
    class Meta:
        model = MaterialGrade
        fields = "__all__"

class TechnicalStandardSerializer(serializers.ModelSerializer):
    """Serializer for TechnicalStandard model"""
    class Meta:
        model = TechnicalStandard
        fields = "__all__"

class ApplicationAreaSerializer(serializers.ModelSerializer):
    """Serializer for ApplicationArea model"""
    class Meta:
        model = ApplicationArea
        fields = "__all__"

class EquipmentTypeSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentType model"""
    class Meta:
        model = EquipmentType
        fields = "__all__"

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    """Serializer for UnitOfMeasure model"""
    class Meta:
        model = UnitOfMeasure
        fields = "__all__"

class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for Manufacturer model"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Manufacturer
        fields = "__all__"
    
    def get_products_count(self, obj):
        return obj.products.count()

class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariant model"""
    product_title = serializers.CharField(source='product.title_ru', read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = "__all__"

class ProductVariantCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating ProductVariant"""
    class Meta:
        model = ProductVariant
        fields = "__all__"

# Enhanced Products Serializer with Building Materials fields
class BuildingMaterialsProductSerializer(serializers.ModelSerializer):
    """Enhanced Products serializer for building materials with all relationships"""
    
    # Related objects
    categoty_id = CategoryDataSerializer(read_only=True)
    brand = BrandSeralizer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    material_type_id = MaterialTypeSerializer(read_only=True)
    material_grade_id = MaterialGradeSerializer(read_only=True)
    technical_standard_id = TechnicalStandardSerializer(read_only=True)
    application_area_id = ApplicationAreaSerializer(read_only=True)
    equipment_type_id = EquipmentTypeSerializer(read_only=True)
    unit_of_measure = UnitOfMeasureSerializer(read_only=True)
    product_type_id = ProductTypeDataSerializer(read_only=True)
    product_color = ProductColorSerializer(read_only=True)
    
    # Related collections
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ReviewSeralizer(many=True, read_only=True)
    
    # Computed fields
    average_rating = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    total_dimensions = serializers.ReadOnlyField()
    profit_margin = serializers.ReadOnlyField()
    
    class Meta:
        model = Products
        fields = "__all__"

class BuildingMaterialsProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating building materials products"""
    
    class Meta:
        model = Products
        fields = "__all__"
    
    def validate_price(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
    
    def validate(self, data):
        # Validate dimensions
        if data.get('length') and data.get('length') <= 0:
            raise serializers.ValidationError("Length must be greater than 0")
        if data.get('width') and data.get('width') <= 0:
            raise serializers.ValidationError("Width must be greater than 0")
        if data.get('height') and data.get('height') <= 0:
            raise serializers.ValidationError("Height must be greater than 0")
        if data.get('weight') and data.get('weight') <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        
        # Validate cost vs selling price
        if data.get('cost_price') and data.get('price'):
            if data['cost_price'] > data['price']:
                raise serializers.ValidationError("Cost price cannot be higher than selling price")
        
        return data

# Simplified serializers for list views
class MaterialTypeListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MaterialType
        fields = ['id', 'title_ru', 'title_uz', 'title_eng', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.count()

class EquipmentTypeListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentType
        fields = ['id', 'title_ru', 'title_uz', 'title_eng', 'is_power_tool', 'requires_certification', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.count()

class ManufacturerListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country_ru', 'website', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.count()

# Product list serializer (lightweight)
class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product lists"""
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    category_name = serializers.CharField(source='categoty_id.title_ru', read_only=True)
    material_type_name = serializers.CharField(source='material_type_id.title_ru', read_only=True)
    
    class Meta:
        model = Products
        fields = [
            'id', 'title_ru', 'title_uz', 'title_eng', 'price', 'stock',
            'product_type', 'unit_type', 'is_available', 'is_featured',
            'is_professional', 'main_image', 'brand_name', 'manufacturer_name',
            'category_name', 'material_type_name', 'created_at'
        ]

# Statistics serializers
class ProductStatsSerializer(serializers.Serializer):
    """Serializer for product statistics"""
    total_products = serializers.IntegerField()
    in_stock_products = serializers.IntegerField()
    low_stock_products = serializers.IntegerField()
    professional_products = serializers.IntegerField()
    featured_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_brands = serializers.IntegerField()
    total_manufacturers = serializers.IntegerField()

class InventoryReportSerializer(serializers.Serializer):
    """Serializer for inventory reports"""
    product_id = serializers.IntegerField()
    title = serializers.CharField()
    current_stock = serializers.IntegerField()
    min_stock_level = serializers.IntegerField()
    stock_status = serializers.CharField()
    last_updated = serializers.DateTimeField()
        