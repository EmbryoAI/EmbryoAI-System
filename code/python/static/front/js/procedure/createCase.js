var embryoNumber = 0;
var embryoCount = 0;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element','address'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
	var laydate = layui.laydate;
	var address = layui.address();

	//查询未关联的采集目录
	$.ajax({
		type : "get",
		url : "/api/v1/well/catalog/list",
		datatype : "json",
		success : function(data) {
			for(var i=0;i<data.length;i++){
				$('#catalogSelect').append(new Option(data[i], data[i]));
			}
			form.render();
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});

	//监听采集目录下拉框选中事件
	form.on('select(catalogSelect)', function(data){

		$.ajax({
			type : "get",
			url : "/api/v1/well/catalog/info?catalogName=" + data.value,
			datatype : "json",
			success : function(catalogData) {
				if(catalogData.code == 200){
					var catalogInfo = catalogData.data;
					$('#catalog_incubator').text(catalogInfo.incubator);
					$('#catalog_dish').text(catalogInfo.dish_list);
					$('#catalog_patient').text(catalogInfo.patient_name);
					$('#catalog_collection_time').text(catalogInfo.collectionDate);
					$('#embryo_number').val(catalogInfo.embryo_number);
					$('#dish').val(catalogInfo.dish_list);
					$('#incubator').val(catalogInfo.incubator);
				}else{
					layer.alert(catalogData.msg)
				}
			},
			error : function(request) {
				layer.alert(request.responseText);
			}
		});

		$('#catalogInfoDiv').show();
	});

	//查询评分规则
	$.ajax({
		type : "get",
		url : "/api/v1/rule/list",
		datatype : "json",
		success : function(data) {
			$("#rule").append("<option value=\"\">请选择</option>");
			for(var i=0;i<data.data.length;i++){
				$("#rule").append("<option value=\"" + i + "\">" + data.data[i].ruleName + "</option>");
			}
			form.render('select');
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});

	
	
	//日期
	laydate.render({
			elem: '#birth',
			format: 'yyyy-MM-dd',
			max: 0,
			done: function(){
				var birthdate = $('#birth').val();
				var year = birthdate.substring(0,4);
				var today = new Date();
				var now = today.getFullYear();
				var result = parseInt(now) - parseInt(year);
				if(birthdate == ''){
					$('#patientAge').val(0);
				}else{
					$('#patientAge').val(result);
				}
			}
	});
	laydate.render({
			elem: '#get',
			format: 'yyyy-MM-dd',
			max: 0
	});
	laydate.render({
			elem: '#iui',
			format: 'yyyy-MM-dd HH:mm',
			max: 0,
			type: 'datetime',
	});

	
	  //自定义验证规则例子
  form.verify({
    card: function(value){
      if(value.length != 18){
        return '身份证号长度应为18位';
      }
    }    
	});
})


function addCase(){
	var selected = $("#catalogSelect  option:selected").text();
	if(selected == 0){
		layer.alert('采集目录不能为空!');
		return;
	}
	$("#addCaseButton").attr("disabled", true).attr("value","创建中..."); 
	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/procedure/add",
		data : $('#procedureForm').serialize(),// 你的formid
		error : function(request) {
			$("#addCaseButton").attr("disabled", false).attr("value","创建病历"); 
			layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert(data);
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});
}

function queryRules(){
	$("#rule").empty();
	$.ajax({
		type : "get",
		url : "/api/v1/rule/list",
		datatype : "json",
		success : function(data) {
			for(var i=0;i<data.data.length;i++){
				$("#rule").append("<option value=\"" + i + "\">" + data.data[i].ruleName + "</option>");
			}
			form.render('select');
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

function countAge(){
	var birthdate = $('#birth').val();
	var year = birthdate.substring(0,4);
	var today = new Date();
	var now = today.getFullYear();
	var result = parseInt(now) - parseInt(year);
	if(birthdate == ''){
		$('#patientAge').val(0);
	}else{
		$('#patientAge').val(result);
	}
}




