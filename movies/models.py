from django.db import models
from datetime import date
from django.db.models.signals import post_save


from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from ckeditor.fields import RichTextField





from django.urls import reverse


class Clients(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    ]
    
    CLIENT_TYPE_CHOICES = [
        (1, 'Regular'),
        (2, 'Premium'),
        (3, 'VIP'),
    ]
    
    LANGUAGE_CHOICES = [
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    
    id = models.AutoField("id", primary_key=True)
    name = models.CharField("Name", max_length=100, blank=True, db_index=True)
    surname = models.CharField("surname", max_length=100, blank=True, db_index=True)
    gender_id = models.IntegerField("gender_id", choices=GENDER_CHOICES, blank=True, null=True)
    
    birth_data = models.DateField("birth_data", blank=True, null=True)
    
    location = models.CharField("city", max_length=100, blank=True, db_index=True)
    
    address = models.TextField("address", blank=True)
    
    phone = models.CharField("Phone", max_length=20, blank=True, unique=True, db_index=True)
    
    lang = models.CharField("lang", max_length=5, choices=LANGUAGE_CHOICES, default='ru', blank=True)
    
    client_type = models.IntegerField("client_type", choices=CLIENT_TYPE_CHOICES, default=1, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Клиенты"
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['created_at']),
            models.Index(fields=['name', 'surname']),
        ]
    
    def __str__(self):
        return f"{self.name} {self.surname} ({self.phone})" if self.name else self.phone
        
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    
    number = models.PositiveIntegerField(db_index=True)
    
    title_uz = models.CharField("title_uz", max_length=200, blank=True, db_index=True)
    title_ru = models.CharField("title_ru", max_length=200, blank=True, db_index=True)
    title_eng = models.CharField("title_eng", max_length=200, blank=True, db_index=True)
    
    sub_id = models.ForeignKey(
        'self', verbose_name="Parent Category", on_delete=models.CASCADE,
        blank=True, null=True, related_name='subcategories'
    )
    icon = models.CharField("icon", max_length=100, blank=True)
    
    status = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Категории"
        ordering = ['number', 'title_ru']
        indexes = [
            models.Index(fields=['status', 'number']),
            models.Index(fields=['sub_id']),
        ]
    
    def __str__(self):
        return self.title_ru or self.title_uz or self.title_eng or f"Category {self.id}"

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description_uz = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_eng = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Brand" 
        verbose_name_plural = "Бренды" 

    def __str__(self):
        return self.name
        
        
class MaterialType(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "MaterialType"
        verbose_name_plural = "Тип материала"

    def __str__(self):
        return self.title_ru
        
class NotificationToken(models.Model):
    token = models.CharField(max_length=500, primary_key=True)
    phone_brand = models.CharField(max_length=500)
    os_name = models.CharField(max_length=500)
    client_id = models.ForeignKey(
        Clients, verbose_name="client_id", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "NotificationToken"
        verbose_name_plural = "NotificationToken"

    def __str__(self):
        return self.token
        

class MaterialGrade(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "MaterialGrade"
        verbose_name_plural = "Класс материала"

    def __str__(self):
        return self.title_ru
        
class MobileDocuments(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    title_bottom_uz =  models.CharField("title_bottom_uz", max_length=500, blank=True)
    description_uz = RichTextUploadingField(blank=True,  null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    title_bottom_ru =  models.CharField("title_bottom_ru", max_length=500, blank=True)
    description_ru = RichTextUploadingField(blank=True,  null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    title_bottom_eng =  models.CharField("title_bottom_eng", max_length=500, blank=True)
    description_eng = RichTextUploadingField(blank=True,  null=True)
    
    class Meta:
        verbose_name = "MobileDocuments" 
        verbose_name_plural = "MobileDocuments" 

    def __str__(self):
        return self.title_ru
        
class TechnicalStandard(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255,  blank=True, null=True)
    title_ru = models.CharField(max_length=255,  blank=True, null=True)
    title_eng = models.CharField(max_length=255,  blank=True, null=True)
    standard_code = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "TechnicalStandard"
        verbose_name_plural = "Технические стандарты"

    def __str__(self):
        return f"{self.title_ru} ({self.standard_code})" if self.standard_code else self.title_ru
        

class ApplicationArea(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255,  blank=True, null=True)
    title_ru = models.CharField(max_length=255,  blank=True, null=True)
    title_eng = models.CharField(max_length=255,  blank=True, null=True)
    
    class Meta:
        verbose_name = "ApplicationArea"
        verbose_name_plural = "Область применения"

    def __str__(self):
        return self.title_ru
        

class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country_uz = models.CharField(max_length=100, blank=True, null=True)
    country_ru = models.CharField(max_length=100, blank=True, null=True)
    country_eng = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name

class UnitOfMeasure(models.Model):
    id = models.AutoField(primary_key=True)
    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    name_eng = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = "UnitOfMeasure"
        verbose_name_plural = "Единицы измерения"

    def __str__(self):
        return f"{self.name_ru} ({self.symbol})"

class EquipmentType(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    is_power_tool = models.BooleanField(default=False)
    requires_certification = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "EquipmentType"
        verbose_name_plural = "Типы оборудования"

    def __str__(self):
        return self.title_ru

class AIforSales(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,  blank=True, null=True)
    status = models.CharField(max_length=255,  blank=True, null=True)
    
    class Meta:
        verbose_name = "AIforSales"
        verbose_name_plural = "ИИ для продаж"

    def __str__(self):
        return self.name
        

        
class Gift(models.Model):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    
    client_id = models.ForeignKey(
        Clients, verbose_name="Clients ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    # gift_type =  models.IntegerField(blank=True)
    
    gift_sum =  models.IntegerField(blank=True)
    
    class Meta:
        verbose_name = "Gift" 
        verbose_name_plural = "Подарочные карты" 

    def __str__(self):
        return self.name
        

class Promo(models.Model):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    
    client_id = models.ForeignKey(
        Clients, verbose_name="Clients ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    promo_type_choise = [
        (1, 'Промокод на доставку'),
        (2, 'Промокод на сумму товара'),
        (3, 'Промокод на % сумму товара'),
    ]
    
    promo_usage_type_choise = [
        (1, 'Единоразово'),
        (2, 'Бесконечный'),
    ]
    
    promo_type =  models.IntegerField(blank=True, choices=promo_type_choise, null=True, default=1)
    
    promo_sum =  models.IntegerField(blank=True, null=True)
    
    promo_percent =  models.IntegerField(blank=True, null=True)
    
    promo_usage_type =  models.IntegerField(blank=True, choices=promo_usage_type_choise, null=True, default=1) 
    
    status =  models.IntegerField(blank=True, null=True, default=1) 
    
    class Meta:
        verbose_name = "Promo" 
        verbose_name_plural = "Promo kod" 

    def __str__(self):
        return self.name
        
class ProductColor(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    color =  models.CharField("color", max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title_ru
        
class ProductBundle(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    
    icon =  models.CharField("icon", max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "ProductBundle" 
        verbose_name_plural = "Связка товара"
    
    def __str__(self):
        return self.title_ru
        
class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    categoty_id = models.ForeignKey(
        Category, verbose_name="Category ID", on_delete=models.CASCADE, blank=True
    )
    
    icon =  models.CharField("icon", max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "ProductType" 
        verbose_name_plural = "Типы продукта"
    
    def __str__(self):
        return self.title_ru
        
class TopTypes(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "TopTypes" 
        verbose_name_plural = "Топ типы товаров"
  
    def __str__(self):
        return self.title_ru
        
        
        
class Products(models.Model):
    UNIT_TYPE_CHOICES = [
        ('ШТ', 'ШТУКИ'),
        ('М', 'МЕТРЫ'),
        ('М2', 'КВАДРАТНЫЕ МЕТРЫ'),
        ('М3', 'КУБИЧЕСКИЕ МЕТРЫ'),
        ('КГ', 'КИЛОГРАММЫ'),
        ('Т', 'ТОННЫ'),
        ('Л', 'ЛИТРЫ'),
        ('УП', 'УПАКОВКИ'),
        ('КМП', 'КОМПЛЕКТЫ'),
    ]
    
    PRODUCT_TYPE_CHOICES = [
        ('MATERIAL', 'Строительный материал'),
        ('TOOL', 'Инструмент'),
        ('EQUIPMENT', 'Оборудование'),
        ('FASTENER', 'Крепеж'),
        ('CHEMICAL', 'Химические материалы'),
    ]
    
    id = models.AutoField(primary_key=True)
    
    # Multilingual titles with proper indexing
    title_uz = models.CharField("Название uz", max_length=300, blank=True, db_index=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru = models.CharField("Название ru", max_length=300, blank=True, db_index=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng = models.CharField("Название eng", max_length=300, blank=True, db_index=True)
    description_eng = models.TextField(blank=True, null=True)
    
    # Technical specifications
    specifications_uz = models.TextField("Технические характеристики uz", blank=True, null=True)
    specifications_ru = models.TextField("Технические характеристики ru", blank=True, null=True)
    specifications_eng = models.TextField("Технические характеристики eng", blank=True, null=True)
    
    installation_guide_uz = models.TextField("Руководство по установке uz", blank=True, null=True)
    installation_guide_ru = models.TextField("Руководство по установке ru", blank=True, null=True)
    installation_guide_eng = models.TextField("Руководство по установке eng", blank=True, null=True)
    
    # Dimensions and measurements
    length = models.DecimalField("Длина (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField("Ширина (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField("Высота (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField("Вес (кг)", max_digits=10, decimal_places=3, blank=True, null=True)
    
    # Unit and quantity
    unit_name_ru = models.CharField("единица измерения", max_length=100, blank=True)
    unit_type = models.CharField(
        max_length=10,
        choices=UNIT_TYPE_CHOICES,
        default='ШТ',
        blank=True
    )
    
    # Product classification
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='MATERIAL',
        blank=True
    )
    
    # Material properties
    material_composition = models.TextField("Состав материала", blank=True)
    color_options = models.CharField("Варианты цветов", max_length=500, blank=True)
    surface_finish = models.CharField("Отделка поверхности", max_length=200, blank=True)
    
    # Certification and standards
    certificate_number = models.CharField("Номер сертификата", max_length=100, blank=True)
    compliance_standards = models.CharField("Соответствие стандартам", max_length=300, blank=True)
    
    # Environmental and safety
    fire_resistance_class = models.CharField("Класс огнестойкости", max_length=50, blank=True)
    environmental_class = models.CharField("Экологический класс", max_length=50, blank=True)
    safety_requirements = models.TextField("Требования безопасности", blank=True)
    
    # Pricing and inventory
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_index=True)
    cost_price = models.DecimalField("Себестоимость", max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, db_index=True)
    min_stock_level = models.PositiveIntegerField("Минимальный остаток", default=0)
    
    # Foreign key relationships with proper indexing
    categoty_id = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE,
        blank=True, null=True, db_index=True, related_name='products'
    )
    product_type_id = models.ForeignKey(
        ProductType, verbose_name="Тип продукта", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    product_bundle_id = models.ForeignKey(
        ProductBundle, verbose_name="Связка товара", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    product_color = models.ForeignKey(
        ProductColor, verbose_name="Цвет продукта", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.CASCADE,
        blank=True, null=True, db_index=True, related_name='products'
    )
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name="Производитель", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    ai = models.ForeignKey(
        AIforSales, verbose_name="ИИ для продаж", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    top_type_id = models.ForeignKey(
        TopTypes, verbose_name="Топ типы продукта", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    material_type_id = models.ForeignKey(
        MaterialType, verbose_name="Тип материала", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    material_grade_id = models.ForeignKey(
        MaterialGrade, verbose_name="Класс материала", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    technical_standard_id = models.ForeignKey(
        TechnicalStandard, verbose_name="Технический стандарт", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    application_area_id = models.ForeignKey(
        ApplicationArea, verbose_name="Область применения", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    equipment_type_id = models.ForeignKey(
        EquipmentType, verbose_name="Тип оборудования", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, verbose_name="Единица измерения", on_delete=models.CASCADE,
        blank=True, null=True, related_name='products'
    )
    
    # Media files
    video = models.FileField(upload_to='products/videos/%Y/%m/', blank=True, null=True)
    main_image = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image1 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    image6 = models.ImageField(upload_to='products/images/%Y/%m/', blank=True, null=True)
    
    # Boolean flags with indexing for filtering
    is_featured = models.BooleanField("Рекомендуемый", default=False, blank=True, db_index=True)
    is_new_arrival = models.BooleanField("Новинка", default=False, blank=True, db_index=True)
    is_bestseller = models.BooleanField("Хит продаж", default=False, blank=True, db_index=True)
    is_on_sale = models.BooleanField("Акция", default=False, blank=True, db_index=True)
    is_professional = models.BooleanField("Профессиональный", default=False, blank=True)
    requires_delivery = models.BooleanField("Требует доставки", default=True, blank=True)
    is_hazardous = models.BooleanField("Опасный груз", default=False, blank=True)
    is_fragile = models.BooleanField("Хрупкий", default=False, blank=True)
    
    # Availability and delivery
    is_available = models.BooleanField("Доступен", default=True, blank=True, db_index=True)
    delivery_days = models.PositiveIntegerField("Дни доставки", default=1, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Строительные материалы и оборудование"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
            models.Index(fields=['categoty_id', 'price']),
            models.Index(fields=['brand', 'price']),
            models.Index(fields=['manufacturer']),
            models.Index(fields=['is_featured', 'is_bestseller']),
            models.Index(fields=['product_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['title_ru', 'title_uz']),
            models.Index(fields=['material_type_id']),
            models.Index(fields=['equipment_type_id']),
        ]
    
    def __str__(self):
        return self.title_ru or self.title_uz or self.title_eng or f"Product {self.id}"
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock_level
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def total_dimensions(self):
        """Calculate total volume in cubic meters"""
        if self.length and self.width and self.height:
            # Convert from mm to m and calculate volume
            return (self.length / 1000) * (self.width / 1000) * (self.height / 1000)
        return None
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.price and self.cost_price:
            return ((self.price - self.cost_price) / self.price) * 100
        return None
        
class ProductVariant(models.Model):
    """Product variants for different sizes, colors, specifications"""
    id = models.AutoField(primary_key=True)
    
    product = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    
    # Variant specifications
    variant_name_uz = models.CharField("Название варианта uz", max_length=500, blank=True)
    variant_name_ru = models.CharField("Название варианта ru", max_length=500, blank=True)
    variant_name_eng = models.CharField("Название варианта eng", max_length=500, blank=True)
    
    # Dimensions for this variant
    length = models.DecimalField("Длина (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField("Ширина (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField("Высота (мм)", max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField("Вес (кг)", max_digits=10, decimal_places=3, blank=True, null=True)
    
    # Color and finish
    color = models.CharField("Цвет", max_length=100, blank=True)
    finish = models.CharField("Отделка", max_length=100, blank=True)
    
    # Pricing and inventory for this variant
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price = models.DecimalField("Себестоимость", max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    
    # SKU for this variant
    sku = models.CharField("Артикул", max_length=100, blank=True, unique=True)
    
    # Images for this variant
    main_image = models.ImageField(upload_to='product_variants/%Y/%m/', blank=True, null=True)
    image1 = models.ImageField(upload_to='product_variants/%Y/%m/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_variants/%Y/%m/', blank=True, null=True)
    
    # Availability
    is_available = models.BooleanField("Доступен", default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "ProductVariant"
        verbose_name_plural = "Варианты продукта"
        unique_together = ['product', 'variant_name_ru']
    
    def __str__(self):
        return f"{self.product.title_ru} - {self.variant_name_ru}" if self.variant_name_ru else f"Variant {self.id}"
    
    @property
    def is_in_stock(self):
        return self.stock > 0
        

class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(Clients, related_name='reviews', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, db_index=True)
    comment = models.TextField(blank=True, null=True)
    
    # Review images
    image1 = models.ImageField(upload_to='reviews/%Y/%m/', blank=True, null=True)
    image2 = models.ImageField(upload_to='reviews/%Y/%m/', blank=True, null=True)
    image3 = models.ImageField(upload_to='reviews/%Y/%m/', blank=True, null=True)
    
    # Moderation fields
    is_approved = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'rating']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['is_approved', 'rating']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_user_product_review')
        ]

    def __str__(self):
        return f"Review by {self.user} for {self.product} - {self.rating}/5"
        
class SearchStory(models.Model):
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Clients, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "SearchStory" 
        verbose_name_plural = "История поиска"

    def __str__(self):
        return self.text
        
        
class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"
        

        
class Orders(models.Model):
    STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Confirmed'),
        (3, 'Processing'),
        (4, 'Shipped'),
        (5, 'Delivered'),
        (6, 'Cancelled'),
        (7, 'Refunded'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        (1, 'Cash'),
        (2, 'Card'),
        (3, 'Payme'),
        (4, 'Click'),
        (5, 'Humo & Uzcard'),
    ]
    
    DELIVERY_TYPE_CHOICES = [
        (1, 'Standard'),
        (2, 'Express'),
        (3, 'Pickup'),
    ]
    
    id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey(
        Clients, verbose_name="Client", on_delete=models.CASCADE,
        blank=True, null=True, db_index=True, related_name='orders'
    )
    
    # Financial fields
    all_sum = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, db_index=True)
    delivery_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promocode_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    
    # Order status and type
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    payment_type = models.IntegerField("payment_type", choices=PAYMENT_TYPE_CHOICES, blank=True, null=True)
    type_delivery_date = models.IntegerField("type_delivery_date", choices=DELIVERY_TYPE_CHOICES, blank=True, null=True)
    
    # Delivery information
    address = models.TextField("address", blank=True)
    phone = models.CharField(max_length=20, blank=True, db_index=True)
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    delivery_date = models.DateTimeField("delivery_date", blank=True, null=True)
    
    # Promo code
    promo = models.ForeignKey(
        Promo, verbose_name="Promo", on_delete=models.SET_NULL,
        blank=True, null=True, related_name='orders'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['payment_type']),
            models.Index(fields=['delivery_date']),
        ]
    
    def __str__(self):
        return f"Order #{self.id} - {self.name} {self.surname}"
    
    @property
    def total_amount(self):
        return (self.all_sum or 0) + (self.delivery_sum or 0) - (self.promocode_sum or 0)
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')
        

class OrderProduct(models.Model):
    id = models.AutoField(primary_key=True)
    
    
    order_id = models.ForeignKey(
        Orders, verbose_name="Orders ID", on_delete=models.CASCADE, blank=True
    )
    
    product = models.ForeignKey(
        Products, verbose_name="Products ID", on_delete=models.CASCADE, blank=True
    )
    
    amount = models.IntegerField(blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "OrderProduct" 
        verbose_name_plural = "Список заказанных продуктов"
    
    
    def __str__(self):
        return f"{self.order_id}"
        
        
class New(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    title_bottom_uz =  models.CharField("title_bottom_uz", max_length=500, blank=True)
    description_uz = RichTextUploadingField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    title_bottom_ru =  models.CharField("title_bottom_ru", max_length=500, blank=True)
    description_ru = RichTextUploadingField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    title_bottom_eng =  models.CharField("title_bottom_eng", max_length=500, blank=True)
    description_eng = RichTextUploadingField(blank=True, null=True)
    
    
    image = models.ImageField(upload_to='news/')
    
    products = models.ManyToManyField(
        Products,
        verbose_name="Список продуктов",
        blank=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "New" 
        verbose_name_plural = "Новости"
    
    def __str__(self):
        return self.title_ru
        
class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    header_ru =  models.CharField("header_ru", max_length=500, blank=True)
    header_eng =  models.CharField("header_eng", max_length=500, blank=True)
    header_uz =  models.CharField("header_uz", max_length=500, blank=True)
    
    
    product = models.ForeignKey(
        Products, verbose_name="Products ID", on_delete=models.CASCADE, blank=True, null=True
    )
    categoty_id = models.ForeignKey(
        Category, verbose_name="Category ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    brand_id = models.ForeignKey(
        Brand, verbose_name="Brand ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    news = models.ForeignKey(
        New, verbose_name="News ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    image = models.ImageField(upload_to='slider/')
    
    get_color = models.BooleanField(default=True)
    
    text_color_white = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Slider" 
        verbose_name_plural = "Слайдер"
    
    def __str__(self):
        return self.title_ru
        
class Actual(models.Model):
    id = models.AutoField(primary_key=True)
    
    count =  models.CharField("count", max_length=500, blank=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    image = models.ImageField(upload_to='actual/')
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Actual" 
        verbose_name_plural = "Актуальные"
    
    def __str__(self):
        return self.title_ru
        
class Stories(models.Model):
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    actual_id = models.ForeignKey(
        Actual, verbose_name="Actual ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    brand_id = models.ForeignKey(
        Brand, verbose_name="Brand ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    product = models.ForeignKey(
        Products, verbose_name="Products ID", on_delete=models.CASCADE, blank=True, null=True
    )
    categoty_id = models.ForeignKey(
        Category, verbose_name="Category ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    image = models.ImageField(upload_to='stories/')
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Stories" 
        verbose_name_plural = "Сторисы"
    
    def __str__(self):
        return self.title_ru
        
class MainPage(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    categoty_id = models.ForeignKey(
        Category, verbose_name="Category ID", on_delete=models.CASCADE, blank=True,  null=True
    )
    top_type_id = models.ForeignKey(
        TopTypes, verbose_name="TopTypes ID", on_delete=models.CASCADE, blank=True,  null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "MainPage" 
        verbose_name_plural = "Настройка главной страницы приложения "

    def __str__(self):
        return self.title_ru



    
        
        
        
