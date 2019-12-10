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
		var catalog = data.value.split(" ")[0];
		$.ajax({
			type : "get",
			url : "/api/v1/well/catalog/info?catalogName=" + catalog,
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
				$("#rule").append("<option value=\"" + data.data[i].id + "\">" + data.data[i].ruleName + "</option>");
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
	var checkIdResult = $("#checkIdResult").val();
	if(checkIdResult == "" || checkIdResult == 'false'){
		layer.alert('请输入正确的身份证号!');
		return;
	}
	var selected = $("#catalogSelect  option:selected").text();
	if(selected == 0){
		layer.alert('采集目录不能为空!');
		return;
	}

	//获取采集时间
	var collectionTime = $('#catalog_collection_time').text();
	var ecTime = $("#get").val();
	var insemiTime = $("#iui").val();
	if(ecTime != ""){
		var collectionCompareEcTime = compareDate(collectionTime, ecTime);
		if(!collectionCompareEcTime){
			layer.alert("取卵时间大于采集时间,请重新选择取卵时间!");
			return;
		}
	}	
	if(insemiTime != ""){
		var collectionCompareInsemiTime = compareDate(collectionTime, insemiTime);
		if(!collectionCompareInsemiTime){
			layer.alert("受精时间大于采集时间,请重新选择受精时间!");
			return;
		}
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

function compareDate(d1,d2){
  return ((new Date(d1.replace(/-/g,"\/"))) > (new Date(d2.replace(/-/g,"\/"))));
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
//根据出生日期计算年龄
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

//根据身份证号计算年龄
function countAgeByIdCard(){
	var idCard = $('#nope').val(); 
	var checkResult = isCardNo(idCard);
	$("#checkIdResult").val(checkResult);
	if(checkResult == false){
		layer.alert("请输入正确的身份证!");  
		return  false;  
	}
	
	var birthDate = idCard.substring(6, 14);
	var year = birthDate.substring(0,4);
	var month =  birthDate.substring(4,6);
	var day =  birthDate.substring(6,8);
	$('#birth').val(year + "-" + month + "-" + day);
	var today = new Date();
	var now = today.getFullYear();
	var result = parseInt(now) - parseInt(year);
	if(birthDate == ''){
		$('#patientAge').val(0);
	}else{
		$('#patientAge').val(result);
	}
}


function isCardNo(id) {
	var format = /^(([1][1-5])|([2][1-3])|([3][1-7])|([4][1-6])|([5][0-4])|([6][1-5])|([7][1])|([8][1-2]))\d{4}(([1][9]\d{2})|([2]\d{3}))(([0][1-9])|([1][0-2]))(([0][1-9])|([1-2][0-9])|([3][0-1]))\d{3}[0-9xX]$/;
	//号码规则校验
	if (!format.test(id)) {
		return false;
	}
	//区位码校验
	//出生年月日校验   前正则限制起始年份为1900;
	var year = id.substr(6, 4),//身份证年
		month = id.substr(10, 2),//身份证月
		date = id.substr(12, 2),//身份证日
		time = Date.parse(month + '-' + date + '-' + year),//身份证日期时间戳date
		now_time = Date.parse(new Date()),//当前时间戳
		dates = (new Date(year, month, 0)).getDate();//身份证当月天数
	if (time > now_time || date > dates) {
		return false;
	}
	return true;
}