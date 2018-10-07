$.ajax({
	cache : false,
	type : "get",
	url : "/api/v1/dish/emAll/"+$("#dishId").val(),
	async : false,
	error : function(request) {
		parent.layer.alert(request.responseText);
	},
	success : function(data) {
		 if(data!=null && data!="null") {
			 //首先渲染患者信息
			 var procedureViewList = JSON.parse(data);
			 var size = procedureViewList.length;
			 for(var i=0;i<size;i++) {
				 var procedure = procedureViewList[i];
				 if(i==0) {//i为0时 则为表头
					 var str = "<tr>";
					 for(var key in procedure){
						 str += "<th>"+procedure[key]+"</th>";
					 }
					 str += "</tr>";
					 $("#theadView").html(str);
				 }else {
					 var str = "<tr>";
					 for(var key in procedure){
						 //如果不为空，并且有,号则表示 是里程碑节点，需要显示图片和时间序列
						 var value = procedure[key]+"";
						 if(value!="" && value.indexOf(",")!=-1) {
							 var proArr = value.split(",");
							 str += "<td>";
							 str +="<img src='/api/v1/well/image?image_path="+proArr[0]+"' class='cycle-img' /><br/>";
							 str +="<span class='cycle-t'>"+proArr[1]+"</span>";
							 str +="</td>";
						 }else {
							 if(value=="") {
								 value = "无";
							 }
							 str += "<td>"+value+"</td>";
						 }
					 }
					 str += "</tr>";
					 $("#tbodyView").append(str);
				 }
			 }

		 }
	}
});