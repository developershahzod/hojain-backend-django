from django.db import models
from datetime import date
from django.db.models.signals import post_save


from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from ckeditor.fields import RichTextField





from django.urls import reverse


class Clients(models.Model):
    id = models.AutoField("id", primary_key=True)
    name =  models.CharField("Name", max_length=500, blank=True)
    surname =  models.CharField("surname", max_length=500, blank=True)
    gender_id = models.IntegerField("gender_id", blank=True)
    
    birth_data =  models.CharField("birth_data", max_length=500, blank=True)
    
    location =  models.CharField("city", max_length=500, blank=True)
    
    address =  models.CharField("address", max_length=500, blank=True)
    
    phone =  models.CharField("Phone", max_length=500, blank=True)
    
    lang =  models.CharField("lang", max_length=500, blank=True)

    
    
    client_type =  models.IntegerField("client_type", blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Clients" 
        verbose_name_plural = "Клиенты"  
    
    def __str__(self):
        return self.phone
        
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    
    number = models.IntegerField()
    
    
    title_uz =  models.CharField("title_uz", max_length=500, blank=True)
    
    title_ru =  models.CharField("title_ru", max_length=500, blank=True)
    
    title_eng =  models.CharField("title_eng", max_length=500, blank=True)
    
    
    
    sub_id = models.ForeignKey(
        'Category', verbose_name="Category ID", on_delete=models.CASCADE, blank=True, null=True 
    )
    icon =  models.CharField("icon", max_length=500, blank=True)
    
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category" 
        verbose_name_plural = "Категории" 
    
    def __str__(self):
        return self.title_ru

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
        
        
class Forwhom(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Forwhom" 
        verbose_name_plural = "Для кого" 

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
        

class Skintype(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Skintype" 
        verbose_name_plural = "Тип кожи" 

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
        
class Hairtype(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255,  blank=True, null=True)
    title_ru = models.CharField(max_length=255,  blank=True, null=True)
    title_eng = models.CharField(max_length=255,  blank=True, null=True)
    
    class Meta:
        verbose_name = "Hairtype" 
        verbose_name_plural = "Тип волос" 

    def __str__(self):
        return self.title_ru
        

class ProductArea(models.Model):
    id = models.AutoField(primary_key=True)
    title_uz = models.CharField(max_length=255,  blank=True, null=True)
    title_ru = models.CharField(max_length=255,  blank=True, null=True)
    title_eng = models.CharField(max_length=255,  blank=True, null=True)
    
    class Meta:
        verbose_name = "ProductArea" 
        verbose_name_plural = "Oбласть применения" 

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
    id = models.AutoField(primary_key=True)
    
    title_uz =  models.CharField("Название uz", max_length=500, blank=True)
    description_uz = models.TextField(blank=True, null=True)
    
    title_ru =  models.CharField("Название ru", max_length=500, blank=True)
    description_ru = models.TextField(blank=True, null=True)
    
    title_eng =  models.CharField("Название eng", max_length=500, blank=True)
    description_eng = models.TextField(blank=True, null=True)
    
    
    
    naznachenie_uz = models.TextField(blank=True, null=True)
    naznachenie_ru = models.TextField(blank=True, null=True)
    naznachenie_eng = models.TextField(blank=True, null=True)
    
    primeneniye_uz = models.TextField(blank=True, null=True)
    primeneniye_ru = models.TextField(blank=True, null=True)
    primeneniye_eng = models.TextField(blank=True, null=True)
    
    

    volume_name_ru =  models.CharField("объем", max_length=500, blank=True)
    
    VOLUME_TYPE_CHOICES = [
        ('МЛ', 'ОБЪЁМ / МЛ'),
        ('ШТ', 'КОЛИЧЕСТВО / ШТ'),
        ('Г', 'ВЕС / Г'),
    ]
    volume_type = models.CharField(
        max_length=10,
        choices=VOLUME_TYPE_CHOICES,
        default='МЛ',
         blank=True
    )


    
    
    # primechaniye_uz =  models.TextField()
    # primechaniye_ru =  models.TextField()
    # primechaniye_eng =  models.TextField()
    
    
    sostav =  models.CharField("sostav", max_length=1000, blank=True)

    
    

    
    
    
    price = models.DecimalField(max_digits=10, decimal_places=2,  blank=True)
    categoty_id = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE, blank=True
    )
    product_type_id = models.ForeignKey(
        ProductType, verbose_name="Тип продукта ", on_delete=models.CASCADE, blank=True, null=True
    )
    
    product_bundle_id = models.ForeignKey(
        ProductBundle, verbose_name="Связка товара ", on_delete=models.CASCADE, blank=True, null=True
    )
    
    product_color = models.ForeignKey(
        ProductColor, verbose_name="Product color ", on_delete=models.CASCADE, blank=True, null=True
    )
    
    product_color_type = models.BooleanField(default=False,  blank=True)
    
    
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.CASCADE, blank=True,null=True
    )
    
    ai = models.ForeignKey(
        AIforSales, verbose_name="ИИ для продаж", on_delete=models.CASCADE, blank=True, null=True
    )
    
    top_type_id = models.ForeignKey(
        TopTypes, verbose_name="Топ типы продукта ", on_delete=models.CASCADE, blank=True,null=True
    )
    
    
    for_whom_id = models.ForeignKey(
        Forwhom, verbose_name="Для кого ", on_delete=models.CASCADE, blank=True,null=True
    )
    
    skin_type_id = models.ForeignKey(
        Skintype, verbose_name="Тип Кожи", on_delete=models.CASCADE, blank=True,null=True
    )
    
    hair_type_id = models.ForeignKey(
        Hairtype, verbose_name="Тип волос", on_delete=models.CASCADE, blank=True,null=True
    )
    
    product_area_id = models.ForeignKey(
        ProductArea, verbose_name="Область применения", on_delete=models.CASCADE, blank=True,null=True
    )
    
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/', blank=True, null=True)
    image6 = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.IntegerField( blank=True)
    
    hit = models.BooleanField(default=False,  blank=True)
    
    bestsellers = models.BooleanField(default=False,  blank=True)
    
    gift_cart = models.BooleanField(default=False,  blank=True)
    
    brand_bestsellers = models.BooleanField(default=False,  blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Products" 
        verbose_name_plural = "Продукты"
    
    
    def __str__(self):
        return self.title_ru
        
class ParrentProduct(models.Model):
    id = models.AutoField(primary_key=True)
    
    product = models.ForeignKey(Products, related_name='product', on_delete=models.CASCADE)
    
    volume_name_uz =  models.CharField("volume_name_uz", max_length=500, blank=True)
    volume_name_ru =  models.CharField("volume_name_ru", max_length=500, blank=True)
    volume_name_eng =  models.CharField("volume_name_eng", max_length=500, blank=True)
    
    
    
    volume =  models.CharField("volume", max_length=500, blank=True)
    
    
    
    price = models.DecimalField(max_digits=10, decimal_places=2)

    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)

    
    stock = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "ParrentProduct" 
        verbose_name_plural = "Родительский Продукт"
    
    
    def __str__(self):
        return self.title_ru
        

class Review(models.Model):
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(Clients, related_name='reviews', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5
    image1 = models.ImageField(upload_to='review/', blank=True, null=True)
    image2 = models.ImageField(upload_to='review/', blank=True, null=True)
    image3 = models.ImageField(upload_to='review/', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review" 
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.comment
        
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
    id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey(
        Clients, verbose_name="Client ID", on_delete=models.CASCADE, blank=True
    )
    
    all_sum = models.DecimalField(max_digits=10, decimal_places=2,  blank=True)
    
    delivery_sum = models.DecimalField(max_digits=10, decimal_places=2,  blank=True)
    
    promocode_sum = models.DecimalField(max_digits=10, decimal_places=2,  blank=True)
    
    status = models.IntegerField(blank=True)
    
    adress = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    
    payment_type =  models.IntegerField("payment_type", blank=True, null=True)
    
    type_delivery_date =  models.IntegerField("type_delivery_date", blank=True, null=True)
    
    delivery_date =  models.CharField("delivery_date", max_length=500, blank=True, null=True)
    
    
    promo = models.ForeignKey(
        Promo, verbose_name="Promo ID", on_delete=models.CASCADE, blank=True, null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Orders" 
        verbose_name_plural = "Заказы"
    
    
    def __str__(self):
         return f"{self.user_id}"
        

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



    
        
        
        
