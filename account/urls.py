from django.urls import path, re_path
from . import views


urlpatterns = [
    path('register/', views.register , name='register'),
    path('userinfo/', views.currentUser , name='userinfo'),
    path('userinfo/updata', views.updata_User , name='updata_User'),
    path('forgot_password/', views.forgot_password , name='forgot_password'),
    re_path(r'^reset_password/(?P<token>.*)/$', views.reset_password, name='reset_password'),
]
