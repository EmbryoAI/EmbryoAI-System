layui.use('form', function(){
	laydate.render({
		elem: '#birthday'
	  });
});

$(function(){
    var sex = $("#sex").val();
    if(sex == "1"){
        $("#man").attr("checked","checked");
    }else{
        $("#women").attr("checked","checked");
    }
    var isAdmin = $("#isAdmin").val();
    if(isAdmin == "0"){
        $("#adminno").attr("checked","checked");
    }else{
        $("#adminyes").attr("checked","checked");
    }
    var isPrivate = $("#isPrivate").val();
    if(isPrivate == "0"){
        $("#privateno").attr("checked","checked");
    }else{
        $("#privateyes").attr("checked","checked");
	}
	var title = $("#title").val();
	$("#titleSelect").val(title);
})


function edit() {

	var username = $("#username").val();
	if(username == ""){
		alert("用户名不能为空!");
		return false;
	}
	if(username.length < 5){
		alert("用户名不能少于5个字符!");
		return false;
	}
	var mobile = $("#mobile").val();
	var email = $("#email").val();
	if(mobile == "" && email == ""){
		alert("手机号码和电子邮箱必须填写一项!");
		return false;
	}
	if(mobile != ""){
		//手机号正则  
		var phoneReg = /(^1[3|4|5|7|8]\d{9}$)|(^09\d{8}$)/;  
		//电话  
		var phone = $.trim(mobile);  
		if (!phoneReg.test(phone)) {  
			alert('请输入有效的手机号码！');  
			return false;  
		}  
	}

	if(email != ""){
		var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); 
		var emailStr = $.trim(email);  
		if (!reg.test(emailStr)) {  
			alert('请输入有效的电子邮箱！');  
			return false;  
		}  
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

	$.ajax({
		cache : false,
		type : "POST",
		url : "/api/v1/user/userInfo",
		data : $('#userEdit').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert("修改用户成功!");
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});

}


