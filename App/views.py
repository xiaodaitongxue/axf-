import uuid

from alipay import AliPay
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, AXFUser, FoodType, Goods, Cart, Order, \
    OrderGoods
from App.views_constant import HTTP_USER_EXIST, HTTP_OK, ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, \
    ORDER_SALE_UP, ORDER_SALE_DOWN, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND
from App.views_helper import hash_str, send_email_activate, get_total_price
from GPAXF.settings import MEDIA_KEY_PREFIX, APP_PPIVATE_KEY, ALIPAY_PUBLIC_KEY, ALIPAY_APPID


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    data = {
        "title": "首页",
        "main_wheels": main_wheels,
        'main_navs': main_navs,
        "main_mustbuys": main_mustbuys,
        "main_shop0_1": main_shop0_1,
        "main_shop1_3": main_shop1_3,
        "main_shop3_7": main_shop3_7,
        "main_shop7_11": main_shop7_11,
        "main_shows": main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={
        'typeid': 104747,
        'childcid': 0,
        'order_rule':0,
    }))


def market_with_params(request, typeid, childcid, order_rule):

    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)
    if childcid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")
    foodtype = foodtypes.get(typeid=typeid)

    foodtypechildnames = foodtype.childtypenames
    foodtypechildname_list = foodtypechildnames.split("#")
    foodtype_childname_list=[]
    for foodtypechildnames in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildnames.split(':'))
    order_rule_list =[
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]
    data = {
        'title':'闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': int(typeid),
        'foodtype_childname_list':foodtype_childname_list,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_view': order_rule

    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)
    is_all_select =not carts.filter(c_is_select=False).exists()
    data = {
        'title':'购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price()
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')
    data={
        'title':'我的',
        'is_login': False,
    }
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['username']=user.u_username
        data['icon']=MEDIA_KEY_PREFIX+user.u_icon.url
        data['is_login']=True
        data['order_not_pay']=Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive']=Order.objects.filter(o_user=user).filter(o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method =="GET":
        data = {
            "title": "注册"
        }
        return render(request, "user/register.html", context=data)
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")
        print(password)

        # password = hash_str(password)
        password = make_password(password)

        user = AXFUser()
        user.u_username= username
        user.u_password= password
        user.u_email= email
        user.u_icon= icon
        print(user.u_password)

        user.save()
        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60*60*24)
        print(u_token)

        send_email_activate(username, email, u_token)

        # return HttpResponse("注册成功")
        return redirect(reverse("axf:login"))

def login(request):
    if request.method =="GET":
        error_message =request.session.get('error_message')
        data = {
            "title":"登录"
        }
        if error_message:
            del request.session['error_message']
            data['error_message']=error_message
        return render(request, "user/login.html", context=data)
    elif request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(password)


        users = AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            print(password)
            print(user.u_password)
            print(check_password(password, user.u_password))
            print(check_password(make_password(password), user.u_password))
            print(check_password(user.u_password, make_password(password)))
            print(check_password(user.u_password, password))
            # if password == user.u_password:
            if check_password(password, user.u_password):
                if user.is_active:
                    request.session["user_id"] = user.id
                    # print('密码正确')
                    return redirect(reverse('axf:mine'))
                else:
                    print('not activate')
                    request.session['error_message']='not activate'
                    return redirect(reverse('axf:login'))

            else:
                print("密码错误")
                request.session['error_message'] = 'password error'
                return redirect(reverse('axf:login'))
        print("用户不存在")
        request.session['error_message'] = 'user does not exist'
        return redirect(reverse('axf:login'))

def check_user(request):
    username = request.GET.get("username")
    users = AXFUser.objects.filter(u_username=username)

    data = {
        "status": HTTP_OK,
        "msg": "user can use"
    }
    if users.exists():
        data['status']= HTTP_USER_EXIST
        data['msg']="user already exist"
    else:
        pass
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))

# def send_email(request):
#     subject = 'AXF Activate'
#     message = '<h1>hello</h1>'
#     from_email = '15228308807@163.com'
#     recipient_list = ['1224181554@qq.com']
#     data={
#         'username': 'tom',
#         'activate_url': 'http://www.1000phone.com'
#     }
#     html_message = loader.get_template('user/activate.html').render(data)
#
#     send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email, recipient_list=recipient_list)
#     return HttpResponse('Send Success')


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        cache.delete(u_token)
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect(reverse('axf:login'))

    return render(request, 'user/activate_fail.html')


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    # user_id = request.GET.get('user_id')
    # if user_id:
    #     return HttpResponse("Add Success")
    # else:
    #
    #     data = {
    #         'status': 302,
    #         'msg': 'not login'
    #     }
    #
    # return JsonResponse(data)
    # print(Cart.c_user)
    # print(Cart.c_goods_id)
    # print(request.user)
    # print(goodsid)
    carts=Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num=cart_obj.c_goods_num+1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user
    cart_obj.save()

    data = {
            'status': 200,
            'msg': 'add success',
            'c_goods_num': cart_obj.c_goods_num
        }
    return JsonResponse(data=data)

def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')
    # user_id = request.GET.get('user_id')
    # if user_id:
    #     return HttpResponse("Add Success")
    # else:
    #
    #     data = {
    #         'status': 302,
    #         'msg': 'not login'
    #     }
    #
    # return JsonResponse(data)
    # print(Cart.c_user)
    # print(Cart.c_goods_id)
    # print(request.user)
    # print(goodsid)
    carts=Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num=cart_obj.c_goods_num-1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user
    cart_obj.save()

    data = {
            'status': 200,
            'msg': 'sub success',
            'c_goods_num': cart_obj.c_goods_num
        }
    return JsonResponse(data=data)


def change_cart_state(request):
    cart_id = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cart_id)
    cart_obj.c_is_select = not cart_obj.c_is_select
    cart_obj.save()
    data={
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'total_price': get_total_price()
    }
    return JsonResponse(data=data)


def sub_shopping(request):
    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cartid)
    data = {
        'status':200 ,
        'msg':'ok',
    }
    if cart_obj.c_goods_num>1:
        cart_obj.c_goods_num=cart_obj.c_goods_num-1
        cart_obj.save()
        data['c_goods_num']=cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0
        data['total_price']: get_total_price()
    return JsonResponse(data=data)


def add_shopping(request):
    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cartid)
    data = {
        'status': 200,
        'msg': 'ok',
    }

    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()
    data['c_goods_num'] = cart_obj.c_goods_num
    data['total_price']: get_total_price()
    return JsonResponse(data=data)


def all_select(request):
    cart_list = request.GET.get('cart_list')
    cart_list = cart_list.split("#")
    carts = Cart.objects.filter(id__in=cart_list)
    for cart_obj in carts:
        cart_obj.c_is_select=not cart_obj.c_is_select
        cart_obj.save()
    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
    data={
        'status':200,
        'msg': 'ok',
        'is_all_select': is_all_select,
        'total_price': get_total_price()
    }
    return JsonResponse(data=data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    order  =Order()
    order.o_user = request.user
    order.o_price = get_total_price()
    order.save()

    for cart_obj in carts:
        ordergoods=OrderGoods()
        ordergoods.o_order=order
        ordergoods.o_goods_num=cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()




    data = {
        'status':200,
        'msg':'ok',
        'order_id':order.id,
    }
    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('orderid')
    order = Order.objects.get(pk=order_id)
    data = {
        'title': '订单详情',
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    print(request.user)
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)
    data = {
        'title': '订单列表',
        'orders': orders,
        # 'num': orders.count()  #自己加的功能
    }
    return render(request, 'order/order_list_not_pay.html', context=data)

def order_list_not_receive(request):
    print(request.user)
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_RECEIVE)
    data = {
        'title': '待收货列表',
        'orders': orders,
    }
    return render(request, 'order/order_list_not_receive.html', context=data)
    # return render(request, 'order/order_list_not_receive.html')

def payed(request):
    print(request.user)
    order_id = request.GET.get("orderid")
    order = Order.objects.get(pk=order_id)
    order.o_status = ORDER_STATUS_NOT_RECEIVE
    order.save()
    data = {
        'status': 200,
        'msg': 'payed success',
    }
    return JsonResponse(data)


# def alipay(request):
#     #构建支付的客户端，AlipayClIENT
#     alipay_client=AliPay(
#     appid=ALIPAY_APPID,
#     app_notify_url=None,  # 默认回调url
#     app_private_key_string=APP_PPIVATE_KEY,
#     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#     alipay_public_key_string=ALIPAY_PUBLIC_KEY,
#     sign_type="RSA", # RSA 或者 RSA2
#     debug=False,  # 默认False
#
#     )
#
#     subject='电脑'
#     # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
#     order_string = alipay.api_alipay_trade_page_pay(
#         out_trade_no="20161112",
#         total_amount=0.01,
#         subject=subject,
#         return_url="https://www.1000phone.com",
#         notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
#     )
#     #使用Alipay进行支付请求的发起
#     #客服端操作
#     return redirect("https://openapi.alipaydev.com/gateway.do?"+order_string)
