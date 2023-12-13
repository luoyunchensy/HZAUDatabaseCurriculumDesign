// main.js
$(document).ready(function() {
    $(".add-to-cart").click(function(e) {
        e.preventDefault();

        var uid = $(this).data('uid');
        var cid = $(this).data('cid');
        var number  = $(this).data('number');

        // 发送 AJAX 请求
        $.ajax({
            type: 'POST',
            url: '/add_to_cart',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                uid: uid,
                cid: cid,
                number: number
            }),
            success: function(response) {
                alert('商品已成功添加到购物车！');
                // 或者更新页面其他元素
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
