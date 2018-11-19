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
	var checkResult = IdentityCodeValid(idCard);
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


function IdentityCodeValid(code) { 
	var city={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江 ",31:"上海",
			32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北 ",43:"湖南",44:"广东",
			45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏 ",61:"陕西",62:"甘肃",63:"青海",
			64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外 "};
	var tip = "";
	var pass= true;

	if(!code || !/^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)$/i.test(code)){
		tip = "身份证号格式错误";
		pass = false;
	}

   else if(!city[code.substr(0,2)]){
		tip = "地址编码错误";
		pass = false;
	}
	else{
		//18位身份证需要验证最后一位校验位
		if(code.length == 18){
			code = code.split('');
			//∑(ai×Wi)(mod 11)
			//加权因子
			var factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 ];
			//校验位
			var parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2 ];
			var sum = 0;
			var ai = 0;
			var wi = 0;
			for (var i = 0; i < 17; i++)
			{
				ai = code[i];
				wi = factor[i];
				sum += ai * wi;
			}
			var last = parity[sum % 11];
			if(parity[sum % 11] != code[17]){
				tip = "校验位错误";
				pass =false;
			}
		}
	}
	return pass;
}