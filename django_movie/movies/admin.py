from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.admin import AdminSite

from .models import (
    # Core models
    Products, ProductVariant, Category, Brand, Clients, Orders, OrderProduct, Review,
    # Building materials specific models
    MaterialType, MaterialGrade, TechnicalStandard, ApplicationArea, 
    EquipmentType, UnitOfMeasure, Manufacturer,
    # Legacy models (keeping for compatibility)
    ProductColor, NotificationToken, MobileDocuments, ProductType, ProductBundle, 
    TopTypes, New, Slider, Stories, MainPage, Gift, AIforSales, SearchStory, 
    Actual, Promo
)

# ============================================================================
# BUILDING MATERIALS ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_uz', 'title_eng', 'products_count')
    search_fields = ('title_ru', 'title_uz', 'title_eng')
    ordering = ('title_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(MaterialGrade)
class MaterialGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_uz', 'title_eng', 'products_count')
    search_fields = ('title_ru', 'title_uz', 'title_eng')
    ordering = ('title_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(TechnicalStandard)
class TechnicalStandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'standard_code', 'products_count')
    search_fields = ('title_ru', 'title_uz', 'title_eng', 'standard_code')
    list_filter = ('standard_code',)
    ordering = ('title_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(ApplicationArea)
class ApplicationAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'title_uz', 'title_eng', 'products_count')
    search_fields = ('title_ru', 'title_uz', 'title_eng')
    ordering = ('title_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'is_power_tool', 'requires_certification', 'products_count')
    search_fields = ('title_ru', 'title_uz', 'title_eng')
    list_filter = ('is_power_tool', 'requires_certification')
    ordering = ('title_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'symbol', 'products_count')
    search_fields = ('name_ru', 'name_uz', 'name_eng', 'symbol')
    ordering = ('name_ru',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_ru', 'website_link', 'products_count')
    search_fields = ('name', 'country_ru', 'country_uz', 'country_eng')
    list_filter = ('country_ru',)
    ordering = ('name',)
    
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return '-'
    website_link.short_description = 'Веб-сайт'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

# ============================================================================
# ENHANCED PRODUCTS ADMIN
# ============================================================================

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('variant_name_ru', 'length', 'width', 'height', 'weight', 'color', 'price', 'stock', 'sku', 'is_available')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Products)
class BuildingMaterialsProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    
    list_display = (
        'id', 'title_ru', 'product_type', 'price', 'stock', 'stock_status', 
        'manufacturer', 'brand', 'is_available', 'is_professional', 'created_at'
    )
    
    list_filter = (
        'product_type', 'is_available', 'is_professional', 'is_featured', 
        'is_new_arrival', 'is_on_sale', 'categoty_id', 'manufacturer', 
        'brand', 'material_type_id', 'equipment_type_id'
    )
    
    search_fields = (
        'title_uz', 'title_ru', 'title_eng', 'material_composition',
        'certificate_number', 'brand__name', 'manufacturer__name'
    )
    
    ordering = ('-created_at',)
    
    
    readonly_fields = ('created_at', 'updated_at', 'profit_margin_display', 'total_dimensions_display')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_uz', 'title_ru', 'title_eng', 'description_uz', 'description_ru', 'description_eng')
        }),
        ('Технические характеристики', {
            'fields': (
                'specifications_uz', 'specifications_ru', 'specifications_eng',
                'installation_guide_uz', 'installation_guide_ru', 'installation_guide_eng',
                'material_composition', 'color_options', 'surface_finish'
            )
        }),
        ('Размеры и вес', {
            'fields': ('length', 'width', 'height', 'weight', 'total_dimensions_display')
        }),
        ('Цены и склад', {
            'fields': ('price', 'cost_price', 'profit_margin_display', 'stock', 'min_stock_level')
        }),
        ('Классификация', {
            'fields': (
                'product_type', 'unit_type', 'unit_name_ru',
                'categoty_id', 'product_type_id', 'brand', 'manufacturer'
            )
        }),
        ('Строительные материалы', {
            'fields': (
                'material_type_id', 'material_grade_id', 'technical_standard_id',
                'application_area_id', 'equipment_type_id', 'unit_of_measure'
            )
        }),
        ('Сертификация и безопасность', {
            'fields': (
                'certificate_number', 'compliance_standards', 'fire_resistance_class',
                'environmental_class', 'safety_requirements'
            )
        }),
        ('Флаги и статусы', {
            'fields': (
                'is_available', 'is_featured', 'is_new_arrival', 'is_bestseller',
                'is_on_sale', 'is_professional', 'requires_delivery', 'is_hazardous', 'is_fragile'
            )
        }),
        ('Доставка', {
            'fields': ('delivery_days',)
        }),
        ('Медиа файлы', {
            'fields': (
                'main_image', 'image1', 'image2', 'image3', 'image4', 
                'image5', 'image6', 'video'
            )
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red;">Нет в наличии</span>')
        elif obj.stock <= obj.min_stock_level:
            return format_html('<span style="color: orange;">Мало на складе</span>')
        else:
            return format_html('<span style="color: green;">В наличии</span>')
    stock_status.short_description = 'Статус склада'
    
    def profit_margin_display(self, obj):
        if obj.profit_margin:
            return f"{obj.profit_margin:.2f}%"
        return '-'
    profit_margin_display.short_description = 'Маржа прибыли'
    
    def total_dimensions_display(self, obj):
        if obj.total_dimensions:
            return f"{obj.total_dimensions:.3f} м³"
        return '-'
    total_dimensions_display.short_description = 'Общий объем'

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'variant_name_ru', 'price', 'stock', 'sku', 'is_available')
    search_fields = ('variant_name_ru', 'variant_name_uz', 'variant_name_eng', 'sku', 'product__title_ru')
    list_filter = ('is_available', 'color', 'finish')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock', 'is_available')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('product', 'variant_name_uz', 'variant_name_ru', 'variant_name_eng')
        }),
        ('Размеры и характеристики', {
            'fields': ('length', 'width', 'height', 'weight', 'color', 'finish')
        }),
        ('Цены и склад', {
            'fields': ('price', 'cost_price', 'stock', 'sku')
        }),
        ('Изображения', {
            'fields': ('main_image', 'image1', 'image2')
        }),
        ('Статус', {
            'fields': ('is_available',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

# ============================================================================
# ENHANCED ORDERS ADMIN
# ============================================================================

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ('product', 'amount', 'price')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ['id', 'user_id', 'all_sum', 'delivery_date', 'status_display', 'payment_type_display', 'created_at']
    search_fields = ['user_id__name', 'user_id__surname', 'phone', 'address']
    list_filter = ['status', 'payment_type', 'type_delivery_date', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ('total_amount_display', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('user_id', 'name', 'surname', 'phone')
        }),
        ('Доставка', {
            'fields': ('address', 'delivery_date', 'type_delivery_date')
        }),
        ('Финансы', {
            'fields': ('all_sum', 'delivery_sum', 'promocode_sum', 'total_amount_display', 'promo')
        }),
        ('Статус и оплата', {
            'fields': ('status', 'payment_type')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def status_display(self, obj):
        return obj.status_display
    status_display.short_description = 'Статус'
    
    def payment_type_display(self, obj):
        payment_types = dict(Orders.PAYMENT_TYPE_CHOICES)
        return payment_types.get(obj.payment_type, 'Не указано')
    payment_type_display.short_description = 'Тип оплаты'
    
    def total_amount_display(self, obj):
        return f"{obj.total_amount} сум"
    total_amount_display.short_description = 'Общая сумма'

admin.site.register(OrderProduct)

# ============================================================================
# ENHANCED CATEGORY ADMIN
# ============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title_ru', 'sub_id', 'status', 'products_count', 'created_at')
    search_fields = ('title_uz', 'title_ru', 'title_eng')
    list_filter = ('status', 'sub_id')
    list_editable = ('number', 'status')
    ordering = ('number', 'title_ru')
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

# ============================================================================
# CLIENTS AND REVIEWS ADMIN
# ============================================================================

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'location', 'client_type', 'created_at')
    search_fields = ('name', 'surname', 'phone', 'location')
    list_filter = ('client_type', 'gender_id', 'lang', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Личная информация', {
            'fields': ('name', 'surname', 'gender_id', 'birth_data')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'location', 'address')
        }),
        ('Настройки', {
            'fields': ('lang', 'client_type')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'is_approved', 'is_featured', 'created_at')
    search_fields = ('product__title_ru', 'user__name', 'comment')
    list_filter = ('rating', 'is_approved', 'is_featured', 'created_at')
    list_editable = ('is_approved', 'is_featured')
    ordering = ('-created_at',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website_link', 'products_count')
    search_fields = ('name', 'description_ru', 'description_uz', 'description_eng')
    ordering = ('name',)
    
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return '-'
    website_link.short_description = 'Веб-сайт'
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество продуктов'

# ============================================================================
# LEGACY MODELS (keeping for compatibility)
# ============================================================================

admin.site.register(MobileDocuments)
admin.site.register(ProductColor)
admin.site.register(NotificationToken)
admin.site.register(ProductType)
admin.site.register(ProductBundle)
admin.site.register(TopTypes)
admin.site.register(New)
admin.site.register(Slider)
admin.site.register(Stories)
admin.site.register(MainPage)
admin.site.register(Gift)
admin.site.register(AIforSales)
admin.site.register(SearchStory)
admin.site.register(Actual)
admin.site.register(Promo)

# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

admin.site.site_title = "Строительные материалы и оборудование - Админ"
admin.site.site_header = "Админ панель магазина стройматериалов"
admin.site.index_title = "Управление магазином строительных материалов"

# Custom admin actions
def make_available(modeladmin, request, queryset):
    queryset.update(is_available=True)
make_available.short_description = "Сделать доступными"

def make_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)
make_unavailable.short_description = "Сделать недоступными"

def mark_as_professional(modeladmin, request, queryset):
    queryset.update(is_professional=True)
mark_as_professional.short_description = "Отметить как профессиональные"

def mark_as_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
mark_as_featured.short_description = "Отметить как рекомендуемые"

# Add actions to Products admin
BuildingMaterialsProductAdmin.actions = [make_available, make_unavailable, mark_as_professional, mark_as_featured]