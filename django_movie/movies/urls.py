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
    # path('external_api/<str:pk>/<str:pk1>/', views.create_insta_acc),
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
]
