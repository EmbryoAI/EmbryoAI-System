layui.use('form', function(){

});

function edit() {
	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/incubator/update",
		data : $('#incubatorForm').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert("编辑培养箱成功!");
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});
}
$("#incubatorBrand").val($("#incubatorBrandHide").val());
$("#incubatorType").val($("#incubatorTypeHide").val());