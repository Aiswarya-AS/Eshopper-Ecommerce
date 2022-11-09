from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_to_cart/',views.add_cart,name='add_to_cart'),
    # path('remove_from_cart/',views.remove_from_cart,name='remove_from_cart'),
    path('update_cart/',views.update_cart,name='update_cart'),
    path('delete_cart_item/<int:product_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
]
