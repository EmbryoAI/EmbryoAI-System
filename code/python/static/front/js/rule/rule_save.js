layui.use('form', function(){
	
});

function save() {
	if($("#ruleName").val()=="") {
		parent.layer.alert("请输入标准名称!");
		return false;
	}
	
	if($("#description").val()=="") {
		parent.layer.alert("请输入描述!");
		return false;
	}
	
	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/rule/save",
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