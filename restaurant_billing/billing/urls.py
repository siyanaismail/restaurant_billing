# from django.urls import path
# from . import views

# urlpatterns = [
#     path('export/pdf/<int:order_id>/', views.export_pdf, name='export_pdf'),
#     path('export/csv/<int:order_id>/', views.export_csv, name='export_csv'),
# ]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('billing.urls')),  # connect billing app
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('export/pdf/<int:order_id>/', views.export_pdf, name='export_pdf'),
    path('export/csv/<int:order_id>/', views.export_csv, name='export_csv'),
    path('report/', views.sales_report, name='sales_report'),
]
