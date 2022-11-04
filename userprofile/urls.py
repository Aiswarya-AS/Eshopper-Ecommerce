from ctypes import addressof
from django.urls import path
from . import views
urlpatterns = [
    path('view_address/',views.view_address,name='view_address'),
    path('add_address/',views.add_address,name='add_address'),

]

# add address
# view address
# edit address
# delete adddress