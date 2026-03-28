from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register , name='register'),
    path('userinfo/', views.currentUser , name='userinfo'),
    path('userinfo/updata', views.updata_User , name='updata_User'),
]
