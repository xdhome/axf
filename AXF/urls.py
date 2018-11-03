from django.conf.urls import url

from AXF import views

urlpatterns = [
    # 购物车
    url(r'^cart/$', views.cart, name="cart"),
    # 首页
    url(r'^home/$', views.home, name="home"),
    # 我的
    url(r'^mine/$', views.mine, name="mine"),
    # 闪购
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name="market"),

]