import hashlib
import os
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 购物车
from AXF.models import *
from axf import settings


def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()


def cart(request):
    return render(request, 'cart/cart.html')

# 首页
def home(request):
    # 轮播图数据
    wheels = Wheel.objects.all()
    # print(len(wheels), len(navs), len(mustbuys))
    # 导航数据
    navs = Nav.objects.all()
    # 每日必购数据
    mustbuys = Mustbuy.objects.all()
    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体内容
    mainshows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows,
    }
    return render(request, 'home/home.html', data)


# 我的
def mine(request):
    # 获取用户信息
    token = request.session.get('token')

    responseData = {}

    if token:   # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['isLogin'] = 1
    else:   # 未登录
        responseData['name'] = '未登录'
        responseData['img'] = '/static/uploads/axf.png'

    return render(request, 'mine/mine.html', context=responseData)


# 闪购
def market(request, categoryid, childid, sortid):
    # 分类信息
    foodtypes = Foodtypes.objects.all()
    # 分类 点击 下标  >>>>  分类ID
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标 获取 对应 分类ID
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    # 将每个子类拆分出来
    childTypleList = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname': arr[0],  # 子类名称
            'childid': arr[1]  # 子类ID
        }
        childTypleList.append(dir)

    # 商品信息 - 根据分类id获取对应数据
    # goodsList = Goods.objects.all()[0:5]
    if childid == '0':  # 全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:  # 分类 下 子类
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)

    # 排序
    if sortid == '1':  # 销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2':  # 价格最低
        goodsList = goodsList.order_by('price')
    elif sortid == '3':  # 价格最高
        goodsList = goodsList.order_by(('-price'))

    data = {
        'foodtypes': foodtypes,  # 分类信息
        'goodsList': goodsList,  # 商品信息
        'childTypleList': childTypleList,  # 子类信息
        'categoryid': categoryid,  # 分类ID
        'childid': childid,  # 子类ID
    }
    return render(request, 'market/market.html', data)


# 注册
def registe(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
            user = User()
            user.account = request.POST.get('account')
            user.password = genarate_password(request.POST.get('password'))
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.addr = request.POST.get('addr')
            user.img = 'axf.png'

            # 头像
            imgName = user.account + '.png'
            imagePath = os.path.join(settings.MEDIA_ROOT, imgName)
            file = request.FILES.get('icon')
            with open(imagePath, 'wb') as fp:
                for data in file.chunks():
                    fp.write(data)
            user.img = imgName

            user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

            user.save()

            # 状态保持
            request.session['token'] = user.token

            # 重定向
            return redirect('axf:mine')


# 账号验证
def checkaccount(request):
    account = request.GET.get('account')

    responseData = {
        'msg': '账号可用',
        'status': 1 # 1标识可用，-1标识不可用
    }

    try:
        user = User.objects.get(account=account)
        responseData['msg'] = '账号已被占用'
        responseData['status'] = -1
        return JsonResponse(responseData)
    except:
        return JsonResponse(responseData)


# 退出
def logout(request):
    request.session.flush()
    return redirect('axf:mine')


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password):    # 登录成功

                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:   # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'mine/login.html', context={'acountErr':'账号不存在!'})


# 购物车加操作
def addcart(request):
    return HttpResponse("购物车加操作")


# 购物车减操作
def subcart(request):
    return HttpResponse("购物车减操作")