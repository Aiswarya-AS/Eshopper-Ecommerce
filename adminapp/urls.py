from django.urls import path,include
from . import views
urlpatterns = [

    path('',views.admin_login,name='adminlogin'),

    path('dashboard/',views.admin_home,name='admin-home'),

    path('users/',views.show_users,name='users'),
    path('block-user/<int:id>/',views.block_user,name='block-user'),

    path('category/',views.category,name='category'),
    path('subcategory/',views.subcategory,name='subcategory'),
    path('products/',views.products,name='products'),

    path('addcategory/',views.add_category,name='addcategory'),
    path('deletecategory/<int:id>/',views.delete_category,name='deletecategory'),
    path('editcategory/<int:id>/',views.edit_category,name='editcategory'),

    path('addsubcategory/',views.add_subcategory,name='addsubcategory'),
    path('deletesubcategory/<int:id>/',views.delete_subcategory,name='deletesubcategory'),
    path('editsubcategory/<int:id>/',views.edit_subcategory,name='editsubcategory'),

    path('addingproduct',views.adding_product,name='addingproduct'),
    path('addproduct/',views.add_product,name='addproduct'),
    path('subcataddproduct/<int:catid>/',views.load_subcategory,name='load-subcategory'),
    
    path('deleteproduct/<int:id>/',views.delete_product,name='deleteproduct'),

    path('logout',views.admin_logout,name='logout'),


    path('orders/',views.orders,name='orders'),
    path('order_items/',views.order_items,name='order_items'),



    path('add_size/',views.add_size,name='add_size'),
    path('add_color/',views.add_color,name='add_color'),
    path('variations/',views.variations,name='variations'),
    path('add_variations/<int:id>/',views.add_variations,name='add_variations'),
    path('load_size/',views.load_size,name='load_size'),


    path('product_report/',views.product_report,name='product_report'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('product_csv/',views.product_csv,name='product_csv'),
    path('generateProductPdf',views.generateProductPdf.as_view(),name='generateProductPdf'),
    path('product_excel',views.product_excel,name='product_excel')
]
