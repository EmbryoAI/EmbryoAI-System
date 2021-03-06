layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
    var table = layui.table;
	var dataIndex = 0;
$(function () {
	$('#search').on('click', function () {//查询
		if($("#ruleId").val()=="") {
			layer.msg("请选择标准名称!")
			return;
		}
		$("#tableSec").html("");
		$.ajax({
			type : "get",
			url : "/api/v1/rule/get/"+$("#ruleId").val(),
			datatype : "json",
			cache:false,
			success : function(data) {
				 var dictList = JSON.parse($("#dictStr").val());
				 var tableThead = '<thead id="theadView">'
					 +"<tr>"
						 +"<th>条件</th>"
						 +"<th>符号</th>"
						 +"<th>判断值</th>"
						 +"<th>分值</th>"
						 +"<th>权重</th>"
						 +"<th>操作</th>"
					 +"</tr>"
					 +"</thead>";
				 //首选循环dict
				 for (var i = 0; i < dictList.length; i++) {
					//获取对应里程碑节点值的
					var tableTbody = "<tbody id='"+dictList[i].dictValue+"'  >";
					if(data!=null && data.dataJson!=null && data.dataJson!="") {
						var dataJson = JSON.parse(data.dataJson);
						var obj = dataJson[dictList[i].dictValue];
						for (var j = 0; j < obj.length; j++) {
							tableTbody+="<tr>";
								tableTbody+="<td>"+obj[j].condition+"</td>";
								tableTbody+="<td>"+obj[j].symbol+"</td>";
								tableTbody+="<td>"+obj[j].value+"</td>";
								tableTbody+="<td>"+obj[j].score+"</td>";
								tableTbody+="<td>"+obj[j].weight+"</td>";
								tableTbody+="<td>";
								tableTbody+="<a class='layui-table-link edit-btn'" +
										" onclick='toRuleJsonSave(\""+dictList[i].dictValue+"\",\""+obj[j].index+"\",\"update\")'" +
												" lay-event='edit'>编辑</a>";
								tableTbody+="<a class='layui-table-link del-btn' " +
										"onclick='deleteRuleJson(\""+dictList[i].dictValue+"\",\""+obj[j].index+"\")'" +
												" lay-event='del'>删除</a>";
								tableTbody+="<a class='layui-table-link edit-btn' " +
								"onclick='toRuleJsonSave(\""+dictList[i].dictValue+"\",\""+obj[j].index+"\",\"copy\")'" +
										" lay-event='del'>复制</a>";
								tableTbody+="</td>";
							tableTbody+="</tr>";
						}
					}
					tableTbody += "</tbody>";
					var str = '<div class="node" data-index="'+dictList[i].dictKey+'">'
						+'<h2>'+dictList[i].dictValue+'</h2>'
						+'<table class="layui-table"  >'
						+tableThead
						+tableTbody
						+'</table>'
						+'<p class="addbtn">'
							+"<button onclick='toRuleJsonSave(\""+dictList[i].dictValue+"\",null,\"add\");'; type='button'>新增条件行</button>"
						+'</p>'
					+'</div>'
					$("#tableSec").append(str);
				 }
				 
					 
				if(dataIndex == 0){
					$('#tableSec .node').addClass('show');
				}else{
					$('#tableSec .node').addClass('hide');
					$('#tableSec .show').removeClass('show');
					$('#tableSec div[data-index=\"' + dataIndex + '\"]').addClass('show');
				}
			},
			error : function(request) {
				layer.alert(request.responseText);
				layer.close(jaindex);
			}
		});
	})

		$('#stage').on('click', 'span[data-tab]', function () {
				var index = $(this).attr('data-tab');
				if(index == 0){
					$('#tableSec .node').addClass('show');
				}else{
					$('#tableSec .node').addClass('hide');
					$('#tableSec .show').removeClass('show');
					$('#tableSec div[data-index=\"' + index + '\"]').addClass('show');
				}
				dataIndex = index;
		})
		$('#stage').on('click','span',function(){
				$('#stage span').removeClass('active');
				$(this).addClass('active');
		})
		//修改标题
		
	 $('#alter').on('click', function(){
		// 获取下拉框的值
		const  ruleId = document.getElementById("ruleId");
		const  index = ruleId.selectedIndex ; 
		const  Oindex= ruleId.options[index].text ;
    layer.prompt({
			title:"修改名称",
        formType: 2,
        value: Oindex,
      }, function(value, index){
        //确定按钮的回调
				layer.msg("修改成功")
        layer.close(index);//关闭窗口
      });
  });
 
 
 
 
	 
	
   })
})

/**
 * 添加规则页面
 * @param type 1.新增  2.修改
 */
function toRuleSave(type) {
	var title = '新增标准';
	var ruleId = null;
	if(type==1) {
		title = '新增标准';
	}else {
		title = '修改标准';
		ruleId = $("#ruleId").val();
		if(ruleId=="" || ruleId==null) {
			layer.msg("请选择标准名称!")
			return;
		}
	}
	layer.open({
		type: 2,
		maxmin: true,
		title: title,
		area : ['560px' , '400px'],
		content: "/front/rule/toRuleSave?ruleId="+ruleId,
	    end:function(index,layero){
	    	window.location.reload();
	    }
	});
}

/**
 * 添加规则JSON串页面
 * @param jsonKey  添加的里程碑节点类型
 * @param type add.新增  update.编辑  copy.复制
 */
function toRuleJsonSave(jsonKey,index,type) {
	var title = "";
	if(type=="add") {
		title = "添加"+jsonKey+"规则";
	}else if(type=="update"){
		title = "编辑"+jsonKey+"规则";
	}else {
		title = "复制"+jsonKey+"规则";
	}
	
	layer.open({
		type: 2,
		maxmin: true,
		title: title,
		area : ['560px' , '400px'],
		content: '/front/rule/toRuleJsonSave/'+$("#ruleId").val()+'/'+jsonKey+'/'+index+'/'+type,
	    end:function(index,layero){
	    	$('#search').trigger("click");
	    }
	});
}

function deleteRuleJson(jsonKey,index) {
    layer.confirm('确定删除该规则吗?', function(idx){
    	$.ajax({
    		cache : false,
    		type : "get",
    		url : "/api/v1/rule/delete/" + $("#ruleId").val()+"/"+jsonKey+"/"+index,
    		async : false,
    		error : function(request) {
    			parent.layer.alert(request.responseText);
    		},
    		success : function(data) {
    			layer.alert("删除成功!");
    			$('#search').trigger("click");
    		}
    	});
    });
}

function setDefault() {
	if ($("#ruleId").val() == "") {
		layer.msg("请选择标准名称!")
		return;
	}
	var ruleId = document.getElementById("ruleId");
	var index = ruleId.selectedIndex;
	var Oindex = ruleId.options[index].text;
	layer.confirm('是否将标准 “ ' + Oindex + " ” 设置为默认？", function(idx) {
		$.ajax({
			cache : false,
			type : "get",
			url : "/api/v1/rule/setDefault/" + $("#ruleId").val(),
			async : false,
			error : function(request) {
				parent.layer.alert(request.responseText);
			},
			success : function(data) {
				layer.alert("设置成功!");
			}
		});
	});

}
