$.ajax({
	cache : false,
	type : "get",
	url : "/api/v1/dish/emGrade/"+$("#dishId").val(),
	async : false,
	error : function(request) {
		parent.layer.alert(request.responseText);
	},
	success : function(data) {
		if (data!=null) {
			for (var i = 0; i < data.length; i++) {
				$("#td"+data[i].cellCode).html(data[i].embryoScore==null?0:data[i].embryoScore);
			}
		}
	}
});