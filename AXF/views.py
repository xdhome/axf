from django.shortcuts import render

# Create your views here.
# 购物车
def cart(request):
    return None

# 首页
def home(request):
    return render(request, 'home/home.html')

# 我的
def mine(request):
    return None

# 闪购
def market(request):
    return None