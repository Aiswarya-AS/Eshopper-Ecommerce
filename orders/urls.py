from django.urls import path
from . import views
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('order_summary/',views.order_summary,name='order_summary'),
    path('orderview/<int:id>',views.orderview,name='orderview'),
    path('order_cancel/<int:id>',views.order_cancel,name='order_cancel'),
]
