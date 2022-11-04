from django.urls import path,include
from . import views
urlpatterns = [
    path('register/',views.user_register,name='register'),
    path('',views.home,name='home'),
    # path('',views.home,name='index'),
    
    path('logout/',views.user_logout,name='logout_user'),

    path('store/',views.store,name='store'),
    path('store/<slug:subcategory_slug>/',views.store,name='products_by_subcategory'),
    path('store/<slug:subcategory_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),

    path('search/',views.search,name='search'),

    path('login-otp/',views.login_otp,name='login-otp'),
    path('login-pass/',views.login_pass,name='login-pass'),
    path('login-page/',views.login_page,name='login-page'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('otp/',views.otp,name='otp'),


    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('user_wishlist/',views.user_wishlist,name="user_wishlist")



    






]
