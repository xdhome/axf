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


    # 注册
    url(r'^registe/$', views.registe, name='registe'),
    # 账号验证
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    # 退出
    url(r'^logout/$', views.logout, name='logout'),
    # 登录
    url(r'^login/$', views.login, name='login'),
    # 添加购物车
    url(r'^addcart/$', views.addcart, name='addcart'),
    # 购物车减操作
    url(r'^subcart/$', views.subcart, name='subcart'),
]