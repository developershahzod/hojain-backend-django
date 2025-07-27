from django.urls import path

from . import views


urlpatterns = [
    path('mainpage/', views.MainPageDetailView.as_view()),
    path('categories/', views.CategorytDetailView.as_view()),
    path('products/', views.ProductsDetailView.as_view()),
    path('news/', views.NewDetailView.as_view()),
    path('news_id/<int:pk>/', views.NewDetaiIDlView.as_view()),
    path('slider/', views.SliderDetailView.as_view()),
    
    path('editpromo/', views.EditPromoSeralizerSeralizerCreateView.as_view()),
    
    path('promo/change-status/', views.ChangeStatePromoByID.as_view(), name='change_promo_status'),
    
    
    path('checkpromo/', views.CheckPromoByIdNumberView.as_view()),
    
    path('stories/', views.StoriesetailView.as_view()),
    
    path('mobile/', views.MobileDocumentsDetailView.as_view()),
    
     path('clients/', views.UserAllDetailView.as_view()),
     
     path('edit_product/<int:pk>/', views.EditProductSeralizerSeralizerCreateView.as_view()),
    
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view()),
    
    path('reviews_user/<int:pk>/<int:pk2>/', views.ReviewUserDetailView.as_view()),
    
    path('products/<int:pk>/stock/', views.UpdateProductStockView.as_view(), name='update-product-stock'),
    
    path('add_review/', views.AddReviewSeralizerCreateView.as_view()),
    
     path('review_all/', views.ReviewDetaiAlllView.as_view()),
    
    path('order_product/<int:pk>/', views.OrdersProductDetailView.as_view()),
    
    path('edit_order/<int:pk>/', views.OrderEditDetailView.as_view()),
    
    path('edit_review/<int:pk>/', views.EditReviewSeralizerCreateView.as_view()),
    
    path('order_user/<int:pk>/', views.OrderUserDetailView.as_view()),
    
    path('notif_by_user/<int:pk>/', views.NotificationTokenUserView.as_view()),
    
    path('notif_all/', views.NotificationTokenAlllView.as_view()),
    
    path('notif_add_token/', views.AddNotificationToket.as_view()),
    
    path('order_user_mobile/<int:pk>/', views.OrderUserMobileDetailView.as_view()),
    
    path('order_product_user/<int:pk>/', views.OrdersUserProductDetailView.as_view()),
    
    path('orders/<int:pk>/', views.OrdersDetailView.as_view()),
    
    path('orders_d/<int:pk>/', views.OrdersMDetailView.as_view()),
    
     path('orders_all/', views.AllOrdersDetailView.as_view()),
    
    path('brand/', views.BrandDetailView.as_view()),
    
    path('products_top_id/<int:pk>/', views.ProductsTopIDDetailView.as_view()),
    
    
    path('products_brand_id/<int:pk>/', views.ProductsBrandIDDetailView.as_view()),
    
    path('products_bundle_id/<int:pk>/', views.ProductsBandleDDetailView.as_view()),
    
    path('products_category_id/<str:pk>/', views.ProductsCategoryIDDetailView.as_view()),
    path("product_id/<int:pk>/", views.ProductsIDDetailView.as_view()),
    
    path("add_client/", views.AddUserCreateView.as_view()),
    
    path("order/", views.AddOrdersSeralizerCreateView.as_view()),
    
     path("order_products/", views.AddOrderProductSeralizerSeralizerCreateView.as_view()),
    
    path("get_client/<str:pk>/", views.UserPhoneDetailView.as_view()),
    
    path("user_data/<int:pk>/", views.UserIDDetailView.as_view()),
    
    path("user_phone_check/<str:pk>/", views.UserPhoneDetailView.as_view()),
    
     path("edit_user_data/<int:pk>/", views.ClientEditDetailView.as_view()),
     
     path('orders/<int:order_id>/recommendations/', views.OrderRecommendationsAPIView.as_view(), name='order-recommendations'),
     
         path('users/<int:user_id>/recommendations/', views.UserRecommendationsAPIView.as_view(), name='user-recommendations'),
    # path('add_account_data/', views.AccountDataCreateView.as_view()),
    # path('add_follow_account/', views.FollowAccountCreateView.as_view()),
    # path('add_follow_count/', views.FollowCountCreateView.as_view()),
    # path('external_<str:pk>/<str:pk1>/', views.create_insta_acc),
    # path('follow/<str:pk>/<str:pk1>/<str:pk2>/', views.follow_user_main),
    
    # path('visit_list/', views.VisitAlllView.as_view()),
    # path('visit_add/', views.VisitCreateView.as_view()),
    # path('visit_id/<int:pk>/', views.VisitIDView.as_view()),
    
    # path('entertament_list/', views.EntertainmentAlllView.as_view()),
    # path('entertament_add/', views.EntertainmentCreateView.as_view()),
    # path('entertament_id/<int:pk>/', views.EntertainmentIDView.as_view()),
    
    # path('student_list/', views.StudentAlllView.as_view()),
    # path('student_add/', views.StudentCreateView.as_view()),
    # path('student_id/<int:pk>/', views.StudentIDView.as_view()),
    # ============================================================================
    # BUILDING MATERIALS API ENDPOINTS
    # ============================================================================
    
    # Material Types CRUD
    path('material-types/', views.MaterialTypeListCreateView.as_view(), name='material-types-list-create'),
    path('material-types/<int:pk>/', views.MaterialTypeDetailView.as_view(), name='material-type-detail'),
    
    # Material Grades CRUD
    path('material-grades/', views.MaterialGradeListCreateView.as_view(), name='material-grades-list-create'),
    path('material-grades/<int:pk>/', views.MaterialGradeDetailView.as_view(), name='material-grade-detail'),
    
    # Technical Standards CRUD
    path('technical-standards/', views.TechnicalStandardListCreateView.as_view(), name='technical-standards-list-create'),
    path('technical-standards/<int:pk>/', views.TechnicalStandardDetailView.as_view(), name='technical-standard-detail'),
    
    # Application Areas CRUD
    path('application-areas/', views.ApplicationAreaListCreateView.as_view(), name='application-areas-list-create'),
    path('application-areas/<int:pk>/', views.ApplicationAreaDetailView.as_view(), name='application-area-detail'),
    
    # Equipment Types CRUD
    path('equipment-types/', views.EquipmentTypeListCreateView.as_view(), name='equipment-types-list-create'),
    path('equipment-types/<int:pk>/', views.EquipmentTypeDetailView.as_view(), name='equipment-type-detail'),
    
    # Units of Measure CRUD
    path('units-of-measure/', views.UnitOfMeasureListCreateView.as_view(), name='units-of-measure-list-create'),
    path('units-of-measure/<int:pk>/', views.UnitOfMeasureDetailView.as_view(), name='unit-of-measure-detail'),
    
    # Manufacturers CRUD
    path('manufacturers/', views.ManufacturerListCreateView.as_view(), name='manufacturers-list-create'),
    path('manufacturers/<int:pk>/', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    
    # Product Variants CRUD
    path('product-variants/', views.ProductVariantListCreateView.as_view(), name='product-variants-list-create'),
    path('product-variants/<int:pk>/', views.ProductVariantDetailView.as_view(), name='product-variant-detail'),
    path('products/<int:pk>/variants/', views.ProductVariantListView.as_view(), name='product-variants-by-product'),
    
    # Enhanced Building Materials Products CRUD
    path('building-materials/', views.BuildingMaterialsProductListCreateView.as_view(), name='building-materials-list-create'),
    path('building-materials/<int:pk>/', views.BuildingMaterialsProductDetailView.as_view(), name='building-material-detail'),
    
    # Specialized Product Lists
    path('products/professional/', views.ProfessionalProductsListView.as_view(), name='professional-products'),
    path('products/featured/', views.FeaturedProductsListView.as_view(), name='featured-products'),
    path('products/new-arrivals/', views.NewArrivalsListView.as_view(), name='new-arrivals'),
    path('products/on-sale/', views.OnSaleProductsListView.as_view(), name='on-sale-products'),
    
    # Inventory Management
    path('products/low-stock/', views.LowStockProductsListView.as_view(), name='low-stock-products'),
    path('products/out-of-stock/', views.OutOfStockProductsListView.as_view(), name='out-of-stock-products'),
    
    # Enhanced filtering by building materials attributes
    path('products/material-type/<int:pk>/', views.ProductsByMaterialTypeView.as_view(), name='products-by-material-type'),
    path('products/equipment-type/<int:pk>/', views.ProductsByEquipmentTypeView.as_view(), name='products-by-equipment-type'),
    path('products/manufacturer/<int:pk>/', views.ProductsByManufacturerView.as_view(), name='products-by-manufacturer'),
    
    # Statistics and Reports
    path('stats/products/', views.ProductStatsView.as_view(), name='product-stats'),
    path('reports/inventory/', views.InventoryReportView.as_view(), name='inventory-report'),
    
    # Bulk Operations
    path('bulk/update-stock/', views.BulkUpdateStockView.as_view(), name='bulk-update-stock'),
    path('bulk/update-prices/', views.BulkUpdatePricesView.as_view(), name='bulk-update-prices'),
    
    # ============================================================================
    # API v2 - RESTful endpoints with better naming
    # ============================================================================
    
    # Core Resources
    path('v2/categories/', views.CategorytDetailView.as_view(), name='v2-categories'),
    path('v2/brands/', views.BrandDetailView.as_view(), name='v2-brands'),
    path('v2/products/', views.BuildingMaterialsProductListCreateView.as_view(), name='v2-products'),
    path('v2/products/<int:pk>/', views.BuildingMaterialsProductDetailView.as_view(), name='v2-product-detail'),
    
    # Orders and Clients
    path('v2/orders/', views.AddOrdersSeralizerCreateView.as_view(), name='v2-orders'),
    path('v2/orders/<int:pk>/', views.OrderEditDetailView.as_view(), name='v2-order-detail'),
    path('v2/clients/', views.AddUserCreateView.as_view(), name='v2-clients'),
    path('v2/clients/<int:pk>/', views.ClientEditDetailView.as_view(), name='v2-client-detail'),
    
    # Reviews
    path('v2/reviews/', views.AddReviewSeralizerCreateView.as_view(), name='v2-reviews'),
    path('v2/reviews/<int:pk>/', views.EditReviewSeralizerCreateView.as_view(), name='v2-review-detail'),
    path('v2/products/<int:pk>/reviews/', views.ReviewDetailView.as_view(), name='v2-product-reviews'),
]
