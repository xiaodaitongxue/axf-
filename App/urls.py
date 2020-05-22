from django.urls import path, re_path

from App import views

urlpatterns = [
    path(r'home/', views.home, name='home'),
    path(r'market/', views.market, name='market'),
    re_path(r'marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params, name='market_with_params'),
    path(r'cart/', views.cart, name='cart'),
    path(r'mine/', views.mine, name='mine'),

    path(r'register/', views.register, name='register'),
    path(r'login/', views.login, name='login'),
    path(r'checkuser/', views.check_user, name='check_user'),
    path(r'logout/', views.logout, name='logout'),
    path(r'activate/', views.activate, name='activate'),
    path(r'addtocart/', views.add_to_cart, name='add_to_cart'),
    path(r'subtocart/', views.sub_to_cart, name='sub_to_cart'),
    path(r'changecartstate/', views.change_cart_state, name='change_cart_state'),
    path(r'subshopping/', views.sub_shopping, name='sub_shopping'),
    path(r'addshopping/', views.add_shopping, name='add_shopping'),
    path(r'allselect/', views.all_select, name='all_select'),
    path(r'makeorder/', views.make_order, name='make_order'),
    path(r'orderdetail/', views.order_detail, name='order_detail'),


    path(r'orderlistnotpay/', views.order_list_not_pay, name='order_list_not_pay'),
    path(r'orderlistnotreceive/', views.order_list_not_receive, name='order_list_not_receive'),

    path(r'payed/', views.payed, name='payed'),
    # path(r'alipay/', views.alipay, name='alipay'),
    # path(r'sendemail/', views.send_email, name='send_email'),
]