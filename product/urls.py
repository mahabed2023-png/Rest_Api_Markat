from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.get_all_prouducts , name='products'),
    path('products/<str:pk>/', views.get_id_prouducts , name='get_id'),
    path('products/new', views.new_prouduct , name='new_prouduct'),
    path('products/update/<str:pk>/', views.update_prouduct , name='update_prouduct'),
    path('products/delete/<str:pk>/', views.Delete_prouduct , name='Delete_prouduct'),
]
