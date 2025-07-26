from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.admin import AdminSite

from .models import ProductColor, Forwhom, NotificationToken, MobileDocuments, Skintype, ProductArea, Clients, Category, ProductType,ProductBundle, TopTypes, Products,New, Slider, Stories, MainPage, Orders, OrderProduct, Review, Gift, AIforSales, Brand, SearchStory, Actual, ParrentProduct, Hairtype, Promo


admin.site.register(MobileDocuments)
admin.site.register(ProductColor)
admin.site.register(NotificationToken)

admin.site.register(Forwhom)
admin.site.register(Skintype)
admin.site.register(ProductArea)
admin.site.register(Promo)

admin.site.register(Actual)

admin.site.register(Hairtype)
admin.site.register(ProductBundle)

admin.site.register(Clients)


class OrderProductInline(admin.TabularInline):  # You can use StackedInline if you prefer
    model = OrderProduct
    extra = 0  # No extra empty forms

class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ['id', 'user_id', 'all_sum', 'delivery_date', 'status', 'created_at']
    search_fields = ['user_id__name', 'user_id__surname']
    list_filter = ['status', 'created_at']

admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderProduct) 

    



class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title_ru", "price", "categoty_id", "hit", "brand_bestsellers", "bestsellers", "product_type_id", "brand", "stock", "created_at"
    )  # Display key fields in the admin list view
    list_filter = (
        "categoty_id", "brand", "product_type_id", "top_type_id", "ai", "for_whom_id", "skin_type_id"
    )  # Filters for better navigation
    search_fields = (
        "title_uz", "title_ru", "title_eng",
    )  # Enables search functionality across multilingual fields
    ordering = ("-created_at",)  # Sorts by newest products
    list_editable = ("price", "stock", "hit", "brand_bestsellers", "bestsellers")  # Allows inline editing of price & stock
    readonly_fields = ("created_at", "updated_at")  # Prevent modification of timestamps

    fieldsets = (
        ("Basic Info", {
            "fields": ("title_uz", "title_ru", "title_eng", "description_uz", "description_ru", "description_eng")
        }),
        ("Details", {
            "fields": (
                "naznachenie_uz", "naznachenie_ru", "naznachenie_eng", 
                "primeneniye_uz", "primeneniye_ru", "primeneniye_eng",
                 "volume_name_ru", "volume_type", "sostav"
            )
        }),
       
        ("Pricing & Stock", {
            "fields": ("price", "stock")
        }),
        ("Categories & Types", {
            "fields": ("categoty_id", "product_type_id", "brand", "ai", "top_type_id", "for_whom_id", "skin_type_id" , "hair_type_id", "product_bundle_id", "hit", "bestsellers", "brand_bestsellers", "gift_cart", "product_color", "product_color_type")
        }),
        ("Media", {
            "fields": (
                "main_image", "image1", "image2", "image3", "image4", 
                "image5", "image6", "video"
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title_ru', 'sub_id', 'created_at')
    search_fields = ('title_uz', 'title_ru', 'title_eng')
    list_editable = ('number',)

admin.site.register(Category, CategoryAdmin)


admin.site.register(ProductType)
admin.site.register(TopTypes)

admin.site.register(ParrentProduct)
admin.site.register(New)
admin.site.register(Slider)
admin.site.register(Stories)
admin.site.register(MainPage)

admin.site.register(Review)
admin.site.register(Brand)
admin.site.register(AIforSales)
admin.site.register(Gift)
admin.site.register(SearchStory)

admin.site.site_title = "Osma App Admin"
admin.site.site_header = "Osma App Admin"