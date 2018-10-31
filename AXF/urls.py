from django.conf.urls import url

from AXF import views

urlpatterns = [
    url(r'^cart/$', views.cart, name="cart"),
    url(r'^home/$', views.home, name="home"),
    url(r'^mine/$', views.mine, name="mine"),
    url(r'^market/$', views.market, name="market"),

]