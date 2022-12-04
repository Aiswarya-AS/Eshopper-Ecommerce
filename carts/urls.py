from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_cart,name='add_to_cart'),
    path('delete_cart_item/<int:cart_item_id>/<int:product_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('decrease_quantity/',views.decrease_quantity,name="decrease_quantity"),
    path('increase_quantity/',views.increase_quantity,name="increase_quantity"),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    path('checkout/',views.checkout,name='checkout'),
]
