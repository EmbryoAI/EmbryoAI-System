function editPasswd() {

	var password = $("#password").val();
	if(password == ""){
		parent.layer.alert("密码不能为空!");
		return false;
	}
	if(password.length < 6){
		parent.layer.alert("密码不能少于6个字符!");
		return false;
	}
	var passwordagain = $("#passwordagain").val();
	if(passwordagain == ""){
		parent.layer.alert("请确认密码!");
		return false;
	}
	if(password != passwordagain){
		parent.layer.alert("两次输入的密码不一致,请重新输入!");
		return false;
	}

	$.ajax({
		cache : false,
		type : "POST",
		url : "/api/v1/user/password",
		data : $('#passwordForm').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert("修改密码成功!");
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});

}


