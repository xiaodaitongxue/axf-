$(function () {
 /*   var a=document.getElementsByTagName('button')  */
    $('#order').click(function () {
  /*      a.click(function () {   */
        var $order = $(this);

        var order_id = $order.attr("orderid");

        window.open('/axf/orderdetail/?orderid=' + order_id, target="_self");

    })

})