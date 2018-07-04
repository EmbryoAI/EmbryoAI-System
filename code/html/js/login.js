layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;

// 登录类型切换
    $(function () {
        $('#choice').on('click', 'span[data-tab]', function () {
            $('#choice span').removeClass('active');
            $(this).addClass('active');
            var index = $(this).attr('data-tab');
            $('#choice-tab .show').removeClass('show');
            $('#choice-tab div[data-index=\"' + index + '\"]').addClass('show');
        })
    })

  //密码修改验证		
    $(".u-login-front,.admin-login").on("click", function (event) {
        event.preventDefault();
		console.log('sss')
        $("#uAccount,#uPasswd").blur();
        var uAccount = $('#uAccount').val().toString();
        var uPasswd = $('#uPasswd').val().toString();
		
        if (uAccount == "" || uPasswd == ""  ) {
            $(".verify").html("*账号或密码不能为空");
			$(".verify").animate({right:'20px'})
        }  else {

        }

    });

    $("#uAccount,#uPasswd").focus(function () {
		$(".verify").animate({right:'-200px'});
        // $(".verify").html(" ");
    });
	
})
