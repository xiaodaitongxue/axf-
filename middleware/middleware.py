from typing import List

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/subtocart/',
    '/axf/changecartstate/',
    '/axf/makeorder/',

]

REQUIRE_LOGIN = [
    '/axf/cart/',
    '/axf/orderdetail/',
    '/axf/orderlistnotpay/',
    '/axf/orderlistnotreceive/',
]


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in REQUIRE_LOGIN_JSON:
            user_id = request.session.get('user_id')
            print(user_id)
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    print(user.u_username, user.u_password)
                    request.user=user
                except:
                    data ={
                        'status': 302,
                        'msg': 'user not avaliable'
                    }
                   # return redirect(reverse('axf:login'))
                    return JsonResponse(data=data)
            else:
                data = {
                    'status': 302,
                    'msg': 'user not login'
                }
                # return redirect(reverse('axf:login'))
                return JsonResponse(data=data)

        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            print(user_id)
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    print(user.u_username, user.u_password)
                    request.user = user
                except:

                    return redirect(reverse('axf:login'))

            else:
                return redirect(reverse('axf:login'))
