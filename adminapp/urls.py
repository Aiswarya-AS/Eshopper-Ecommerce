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
    path('editproduct/<int:id>/',views.edit_product,name='editproduct'),

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
    path('product_excel',views.product_excel,name='product_excel'),

    path('sales_csv/',views.sales_csv,name='sales_csv'),
    path('sales_excel/',views.sales_excel,name='sales_excel'),
    path('generateSalesPdf',views.generateSalesPdf.as_view(),name='generateSalesPdf'),

    path('category_offer',views.category_offer,name='category_offer'),
    path('subcategory_offer',views.subcategory_offer,name='subcategory_offer'),
    path('product_offer',views.product_offer,name='product_offer'),


    path('add_category_offer',views.add_category_offer,name='add_category_offer'),
    path('add_subcategory_offer',views.add_subcategory_offer,name='add_subcategory_offer'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),



    path('edit_category_offer',views.edit_category_offer,name='edit_category_offer'),
    path('edit_subcategory_offer',views.edit_subcategory_offer,name='edit_subcategory_offer'),
    path('edit_product_offer',views.edit_product_offer,name='edit_product_offer'),

    path('delete_category_offer',views.delete_category_offer,name='delete_category_offer'),
    path('delete_subcategory_offer',views.delete_subcategory_offer,name='delete_subcategory_offer'),
    path('delete_product_offer',views.delete_product_offer,name='delete_product_offer'),

    path('coupons/',views.coupons,name='coupons'),
    path('add_coupons/',views.add_coupons,name='add_coupons'),


    path('salesReport/',views.salesReport,name='salesReport'),
    path('by_date/',views.by_date,name='by_date'),
    path('generatesalesReportPdf',views.generatesalesReportPdf.as_view(),name='generatesalesReportPdf'),

]
