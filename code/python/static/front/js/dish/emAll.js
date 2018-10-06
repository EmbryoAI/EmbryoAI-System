$.ajax({
	cache : false,
	type : "get",
	url : "/api/v1/dish/emAll/"+$("#dishId").val(),
	async : false,
	error : function(request) {
		parent.layer.alert(request.responseText);
	},
	success : function(data) {
		if (data!=null) {
			 
		}
	}
});