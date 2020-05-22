$(function(){
    $("#not_login").click(function(){
        window.open('/axf/login/', target='_self');
    })
     $("#regis").click(function(){
        window.open('/axf/register/', target='_self');
    })


    $("#not_pay").click(function(){

//     var $notpay = $("#not_pay");
//
//    $.getJSON("/axf/payed/", {"orderid": orderid}, function (data) {
//        console.log(data);
//
//        if(data['status'] === 200){
//            window.open('/axf/mine/', target='_self');
//        }

//    if (order_not_pay >0){
        window.open('/axf/orderlistnotpay/', target='_self');
//    }
//    else{
//        alert('没有未付款订单')
//    }


    })



    $("#not_receive").click(function(){
        window.open('/axf/orderlistnotreceive/', target='_self');
    })

})