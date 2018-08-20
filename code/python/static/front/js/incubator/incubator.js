//默认的培养箱id
var defaultId = "";

layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
	var laydate = layui.laydate;

	var data = loadAllIncubator(1,20);
	data.done(function(result){
		var incubatorCode = $("#incubatorCode").val();
		var defaultCode = "";
		if(incubatorCode === null || incubatorCode === "" || incubatorCode === "undefined"){
			defaultCode = data[0].incubatorCode;
		} else {
			defaultCode = incubatorCode;			
		}
		defaultId = $("#incubatorDiv span[code="+ defaultCode +"]").attr("id");
		$("#incubatorDiv span[code="+ defaultCode +"]").addClass("active");
		loadDishByIncubatorId(defaultId);
	});

	// 培养皿选择
	$('#incubatorDiv').on('click','span',function(){
		if(!$(this).hasClass('active')){
			$(this).siblings('span').removeClass('active');
			$(this).addClass('active');
			var incubatorId = $(this).attr("id");
			loadDishByIncubatorId(incubatorId);
		}
	})

	// 查看病历
	$('.patient-info').hover(function(){
		const txt ="无";
		const div = "<div class='case-details'><dl><dt><strong>姓名</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>授精时间</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>首次拍照时间</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>年龄</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>授精方式</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>阶段</strong><span>"+txt+"</span></dt>"+"</dl></div>";
		$(this).append(div)
	},function(){
		$(this).children('div').remove()
	})

	$('ul').on('mouseenter', 'li', function() {//绑定鼠标进入事件
		$(this).addClass('hover');
	});
})

function loadAllIncubator(pageNo,pageSize){
    var defer = $.Deferred(); 
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/incubator/list",
        data : {"page":pageNo,"limit":pageSize},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
			defer.resolve(data.data);
			var spanDiv = "";
			if(data !== null && data.count !== null & data.count > 0){
				for (let i = 0; i < data.data.length; i++) {
					const obj = data.data[i];
					spanDiv = spanDiv + "<span id=" + obj.id + " code=" + obj.incubatorCode + ">" + obj.incubatorCode + "</span>";
				}
			}
			$("#incubatorDiv").append(spanDiv);
        }
    });
    return defer.promise();
}

function loadDishByIncubatorId(incubatorId){
	$.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/loadDishList",
        data : {"incubatorId":incubatorId},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
			console.info(data.data);
			var divHtml = "";
			if(data.code == 200 && data.data !== null & data.data.length > 0){
				for (let i = 0; i < data.data.length; i++) {
					const obj = data.data[i];
					divHtml = divHtml + '<div class="layui-col-md4">' +
						'<div class="in-dish">' + 
							'<div class="dish-num"><span>' + obj.dishCode + '</span><a>查看皿</a></div>' +
							'<ul class="dish-info">' +
								'<li>Dish # <span>' + obj.dishCode + '</span></li>' + 
								'<li>本皿胚胎数<span>' + obj.embryoCount + '</span></li>' +
								'<li>胚胎总数<span>' + data.count + '</span></li>' +
							'</ul>' +
							'<div class="patient-info">' +
								'<span>查看病历</span>' + 
							'</div>' + 
						'</div>' +
					'</div>';
				}
			} else {
				var divHtml = '<div class="layui-col-md4">此培养箱暂未存放培养皿</div>';
			}
			$("#dishDiv").html(divHtml);
        }
    });
}