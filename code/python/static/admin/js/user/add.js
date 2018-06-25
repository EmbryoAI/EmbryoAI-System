layui.use('form', function(){
	
});

function add() {
	var username = $("#username").val();
	if(username == ""){
		alert("用户名不能为空!");
		return false;
	}
	if(username.length < 5){
		alert("用户名不能少于5个字符!");
		return false;
	}
	var password = $("#password").val();
	if(password == ""){
		alert("密码不能为空!");
		return false;
	}
	if(password.length < 6){
		alert("用户名不能少于6个字符!");
		return false;
	}
	var passwordagain = $("#passwordagain").val();
	if(passwordagain == ""){
		alert("请确认密码!");
		return false;
	}
	if(password != passwordagain){
		alert("两次输入的密码不一致,请重新输入!");
		return false;
	}
	var mobile = $("#mobile").val();
	if(mobile == ""){
		alert("手机号码不能为空!");
		return false;
	}
	//手机号正则  
	var phoneReg = /(^1[3|4|5|7|8]\d{9}$)|(^09\d{8}$)/;  
	//电话  
	var phone = $.trim(mobile);  
	if (!phoneReg.test(phone)) {  
		alert('请输入有效的手机号码！');  
		return false;  
	}  
	var email = $("#email").val();
	if(email == ""){
		alert("电子邮箱不能为空!");
		return false;
	}
	var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); 
	var emailStr = $.trim(email);  
	if (!reg.test(emailStr)) {  
		alert('请输入有效的电子邮箱！');  
		return false;  
	}  
	var truename = $("#truename").val();
	if(truename == ""){
		alert("真实姓名不能为空!");
		return false;
	}
	var title = $("#title").val();
	if(title == ""){
		alert("职称不能为空!");
		return false;
	}
	var isAdmin = $('input:radio[name="isAdmin"]:checked').val();
	if(isAdmin == undefined){
		alert("是否管理员不能为空!");
		return false;
	}
	var isPrivate = $('input:radio[name="isPrivate"]:checked').val();
	if(isPrivate == undefined){
		alert("病历权限不能为空!");
		return false;
	}

	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/user",
		data : $('#userAdd').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert("新增用户成功!");
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});

}