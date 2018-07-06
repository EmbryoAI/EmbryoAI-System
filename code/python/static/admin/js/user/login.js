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

  	//用户密码登录前台	
    $("#loginButton").on("click", function (event) {
        event.preventDefault();
		console.log('sss')
        $("#uAccount,#uPasswd").blur();
        var uAccount = $('#uAccount').val().toString();
        var uPasswd = $('#uPasswd').val().toString();
		
        if (uAccount == "" || uPasswd == ""  ) {
            $(".verify").html("*账号或密码不能为空");
			$(".verify").animate({right:'20px'});
        }  else {
            $.ajax({
                cache : false,
                type : "POST",
                url : "/api/v1/login/nameAndPwd",
                data : {"username":uAccount,"password":uPasswd},
                async : false,
                error : function(request) {
                    parent.layer.alert(request.responseText);
                },
                success : function(data) {
                    $(".verify").html(data.msg);
			        $(".verify").animate({right:'20px'});
                    if(data.code == 200){
                        location = "/front/procedure";
                    }
                }
            });

        }

    });

    //用户密码登录后台
    $("#adminLogin").on("click", function (event) {
        event.preventDefault();
		console.log('sss')
        $("#uAccount,#uPasswd").blur();
        var uAccount = $('#uAccount').val().toString();
        var uPasswd = $('#uPasswd').val().toString();
		
        if (uAccount == "" || uPasswd == ""  ) {
            $(".verify").html("*账号或密码不能为空");
			$(".verify").animate({right:'20px'})
        }  else {
            $.ajax({
                cache : false,
                type : "POST",
                url : "/api/v1/login/nameAndPwd",
                data : {"username":uAccount,"password":uPasswd},// 你的formid
                async : false,
                error : function(request) {
                    parent.layer.alert(request.responseText);
                },
                success : function(data) {
                    var msg = data.msg;
                    if(data.code == 200){
                        if(data.data.isAdmin != 0 ){
                            location = "/login/main";
                        } else {
                            msg = "您不是管理员用户！";
                        }
                    }
                    $(".verify").html(msg);
			        $(".verify").animate({right:'20px'})

                }
            });
        }

    });

    $("#uAccount,#uPasswd").focus(function () {
		$(".verify").animate({right:'-200px'});
        // $(".verify").html(" ");
    });
	
})
