from django.shortcuts import render

# Create your views here.
# 购物车
from AXF.models import *


def cart(request):
    return render(request, 'cart/cart.html')

# 首页
def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()
    # print(len(wheels), len(navs), len(mustbuys))
    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
    }
    return render(request, 'home/home.html', data)

# 我的
def mine(request):
    return render(request, 'mine/mine.html')

# 闪购
def market(request):
    return render(request, 'market/market.html')