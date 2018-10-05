var embryoNumber = 0;
var embryoCount = 0;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element','address'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
		var laydate = layui.laydate;
		var address = layui.address();

	// 培养箱选择
	$('.incubator').on('click','span',function(){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		}else{
			$(this).siblings('span').removeClass('active');
			$(this).addClass('active');
		}
		$('#incubator').val($(this).html());
	})
	// 培养皿选择
	$('.dish').on('click','span',function(){
		const length = $('.dish').children('.active').length;
		const text = $(this).text();
		if(length>=2){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
			}
			return
		}
		if($(this).hasClass('active')){
			$(this).removeClass('active');
			embryoCount = embryoCount - embryoNumber;
		}else{
			$(this).addClass('active');
			embryoCount = embryoNumber + embryoCount;
		}
		$('#embryo_number').val(embryoCount);
		var dishName = "";
		var dishCatalog = $('#dish_' + this.id).val();
		if(dishName == ''){
			dishName = $(this).html() + "," + dishCatalog;
		}else{
			dishName = dishName + "|" + $(this).html() + "," + dishCatalog;
		}
		$('#dish').empty();
		$('#dish').val(dishName);

		quertEmbryoNumber(dishName);
	})	
	
	//日期
	laydate.render({
			elem: '#birth',
			format: 'yyyy-MM-dd ',
			max: 0,
			done: function(){
				var birthdate = $('#birth').val();
				var year = birthdate.substring(0,4);
				var today = new Date();
				var now = today.getFullYear();
				var result = parseInt(now) - parseInt(year);
				$('#patientAge').val(result);
			}
	});
	laydate.render({
			elem: '#get',
			format: 'yyyy-MM-dd ',
			max: 0
	});
	laydate.render({
			elem: '#iui',
			format: 'yyyy-MM-dd ',
			max: 0
	});

	
	  //自定义验证规则例子
  form.verify({
    card: function(value){
      if(value.length != 18){
        return '身份证号长度应为18位';
      }
    }    
	});
	
		$(function(){
				$.ajax({
						type : "get",
						url : "/api/v1/well/incubator",
						datatype : "json",
						success : function(data) {
								var child = "";
								for(var i=0;i<data.length;i++){
										child = child + "<span onclick=\"queryDish('" + data[i] + "')\">" +
										data[i] + "</span>";
								}
								$('#incubatorNameDiv').append(child);
						},
						error : function(request) {
								layer.alert(request.responseText);
						}
				});
		});
})

function queryDish(incubatorName){
	$.ajax({
		type : "get",
		url : "/api/v1/well/dish?incubatorName=" + incubatorName,
		datatype : "json",
		success : function(data) {
				$('#dishDiv').empty();
				var child = "<strong>培养箱选择：</strong>";
				for(var i=0;i<data.length;i=i+2){
					child = child + "<span id=\"" + i + "\">" + data[i] + "</span>" + 
									"<input type=\"hidden\" id=\"dish_" + i + "\" value=\"" + data[i+1] + "\"/>";
				}
				child = child + "<i>* 最多只能选择2个皿</i>";
				$('#dishDiv').append(child);
		},
		error : function(request) {
				layer.alert(request.responseText);
		}
	});

	form.on('input(birthdate)', function(data){
		alert(1);
     });  
}

function addCase(){
	var cubActive = $('#incubatorNameDiv').children("span").hasClass("active");
	if(cubActive == false){
		layer.alert('请选择培养箱!');
		return;
	}
	var dishActive = $('#dishDiv').children("span").hasClass("active");
	if(dishActive == false){
		layer.alert('请选择培养皿!');
		return;
	}

	$.ajax({
		cache : false,
		type : "post",
		url : "/api/v1/procedure/add",
		data : $('#procedureForm').serialize(),// 你的formid
		error : function(request) {
			layer.alert(request.responseText);
		},
		success : function(data) {
			parent.layer.alert(data);
			var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			parent.layer.close(index);
		}
	});
}

function quertEmbryoNumber(dishCode){
	$.ajax({
		type : "get",
		url : "/api/v1/embryo/number?dishCode=" + dishCode,
		datatype : "json",
		success : function(data) {
			//$('#embryo_number').val(data.length);
			embryoNumber = data.length;
			$('#well_id').val(data);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}




