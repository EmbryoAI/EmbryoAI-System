layui.use('form', function(){
	var form = layui.form;
	form.on('select(conditionLay)', function(obj){
		valueIni(obj.value);
	});
	$("#condition").val($("#conditionHide").val());
	$("#symbol").val($("#symbolHide").val());
	if($("#conditionHide").val()!="") {
		valueIni($("#conditionHide").val());
	}
	
	//显示 和 回显
	function valueIni(value) {
		$("#value").html('<option value="">请选择</option>');
		$.ajax({
			cache : false,
			type : "get",
			url : "/api/v1/dict/list/"+value,
			async : false,
			error : function(request) {
				parent.layer.alert(request.responseText);
			},
			success : function(data) {
				if (data.code == 0) {
					for (var i = 0; i < data.data.length; i++) {
						var obj = data.data[i];
						$("#value").append("<option value='"+obj.dictKey+"'>"+obj.dictValue+"</option>");
					}
				} else {
					parent.layer.alert(data.msg);
				}
			}
		});
		form.render();
	}
	$("#value").val($("#valueKeyHide").val());
	form.render();
});

function save() {
	if($("#condition").val()=="") {
		parent.layer.alert("请选择条件!");
		return false;
	}
	
	if($("#value").val()=="") {
		parent.layer.alert("请填写值!");
		return false;
	}
	
	if($("#symbol").val()=="") {
		parent.layer.alert("请选择符号!");
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

 

