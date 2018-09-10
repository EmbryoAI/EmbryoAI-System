layui.use('form', function(){
	
});

function save() {
	if($("#condition").val()=="") {
		parent.layer.alert("请选择条件!");
		return false;
	}
	
	if($("#symbol").val()=="") {
		parent.layer.alert("请选择符号!");
		return false;
	}
	
	if($("#value").val()=="") {
		parent.layer.alert("请填写值!");
		return false;
	}
	
	if($("#score").val()=="") {
		parent.layer.alert("请填写得分!");
		return false;
	}
	
	if($("#weight").val()=="") {
		parent.layer.alert("请填写权重!");
		return false;
	}
	
	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/rule/saveRuleJson",
		data : $('#ruleForm').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert("保存成功!");
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});
}

$("#condition").val($("#conditionHide").val());
$("#symbol").val($("#symbolHide").val());