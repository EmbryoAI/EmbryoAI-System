// 加载数据
function loadLogin(username,password){
    var defer = $.Deferred(); 
    $.ajax({
        cache : false,
        type : "POST",
        url : "/api/v1/login/nameAndPwd",
        data : {"username":username,"password":password},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
            defer.resolve(data);
        }
    });
    return defer.promise();
}

//登录到前台页面
function loginToFront(){
    $("#uAccount,#uPasswd").blur();
    var uAccount = $('#uAccount').val().toString();
    var uPasswd = $('#uPasswd').val().toString();
		
    if (checkAccountPasswd(uAccount,uPasswd)) {
        var data = loadLogin(uAccount,uPasswd);
        data.done(function(result){
            $(".verify").html(result.msg);
            $(".verify").animate({right:'20px'});
            if(result.code == 200){
                location = "/front/home";
            }
        });
    }
}

//检测账号密码是否输入
function checkAccountPasswd(uAccount,uPasswd){
    var falg = true;
    if (uAccount == "" || uPasswd == ""  ) {
        falg = false;
        $(".verify").html("*账号或密码不能为空");
		$(".verify").animate({right:'20px'});
    }
    return falg;
}


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
        loginToFront();
    });

    //用户密码登录后台
    $("#adminLogin").on("click", function (event) {
        event.preventDefault();
        $("#uAccount,#uPasswd").blur();
        var uAccount = $('#uAccount').val().toString();
        var uPasswd = $('#uPasswd').val().toString();
        if (checkAccountPasswd(uAccount,uPasswd)) {
            var data = loadLogin(uAccount,uPasswd);
            data.done(function(result){
                var msg = result.msg;
                if(result.code == 200){
                    if(result.data.isAdmin != 0 ){
                        location = "/login/main";
                    } else {
                        msg = "您不是管理员用户！";
                    }
                }
                $(".verify").html(msg);
                $(".verify").animate({right:'20px'})
            });
        }
    });

    $("#uAccount,#uPasswd").focus(function () {
		$(".verify").animate({right:'-200px'});
        // $(".verify").html(" ");
    });

    //密码框监听回车事件
    $('#uPasswd').bind('keypress',function(event){
        if(event.keyCode == "13"){  
            loginToFront();
        }
    });
})

