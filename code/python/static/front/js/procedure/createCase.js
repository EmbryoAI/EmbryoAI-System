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
		}else{
			$(this).addClass('active');
		}
	})	
	
	//日期
	laydate.render({
			elem: '#birth',
			format: 'yyyy/MM/dd ',
			max: 0
	});
	laydate.render({
			elem: '#get',
			format: 'yyyy/MM/dd ',
			max: 0
	});
	laydate.render({
			elem: '#iui',
			format: 'yyyy/MM/dd ',
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
						for(var i=0;i<data.length;i++){
								child = child + "<span>" + data[i] + "</span>";
						}
						child = child + "<i>* 最多只能选择2个皿</i>";
						$('#dishDiv').append(child);
				},
				error : function(request) {
						layer.alert(request.responseText);
				}
		});
}



