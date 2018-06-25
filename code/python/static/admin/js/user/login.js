layui.use(['form', 'layer'], function () {
	var $ = layui.jquery,form =layui.form,layer = layui.layer;
	// 验证
	form.verify({
			username: function (value) {
					if (value == "") {
							return "请输入用户账号！";
					}
			},
			password: function (value) {
					if (value == "") {
							return "请输入密码！";
					}
			}
	});

})

$("#loginSubmit").click(function(){  
	var username = $("#username").val();
	var password = $("#password").val();
	if (username != "" && password != "") {
		$("#loginForm").submit();
	}
	
});
