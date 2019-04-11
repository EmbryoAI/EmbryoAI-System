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
			defaultCode = result[0].incubatorCode;
		} else {
			defaultCode = incubatorCode;			
		}
		defaultId = $("#incubatorDiv span[code="+ defaultCode +"]").attr("id");
		$("#incubatorDiv span[code="+ defaultCode +"]").addClass("active");
		var procedureId = $("#procedureId").val();
		//加载培养箱下的皿信息
		loadDishData(defaultId,procedureId);
	});

	// 培养皿选择
	$('#incubatorDiv').on('click','span',function(){
		if(!$(this).hasClass('active')){
			$(this).siblings('span').removeClass('active');
			$(this).addClass('active');
			var incubatorId = $(this).attr("id");
			var procedureId = $("#procedureId").val();
			loadDishData(incubatorId,procedureId);
		}
	})

	// $('#dishDiv .patient-info').on('mouseenter', '', function() {//绑定鼠标进入事件
	// 	const dishId = $(this).attr('dishId');
	// 	$('#caseDiv_'+dishId).show();
	// });

	// $("#dishDiv .patient-info").on('mouseout','', function() {
	// 	const dishId = $(this).attr('dishId');
	// 	$('#caseDiv_'+dishId).hide();
	// });
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
					if(obj.delFlag === 0){
						spanDiv = spanDiv + "<span id=" + obj.id + " code=" + obj.incubatorCode + ">" + obj.incubatorCode + "</span>";
					}
					
				}
			}
			$("#incubatorDiv").append(spanDiv);
        }
    });
    return defer.promise();
}

function loadDishData(incubatorId,procedureId){
	$.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/loadDishList",
        data : {"incubatorId":incubatorId,"procedureId":procedureId},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
			var divHtml = "";
			if(data.code == 200){
				if(data.count > 0 && data.data !== null){
					for (let i = 0; i < data.data.length; i++) {
						const obj = data.data[i];
						divHtml = divHtml + '<div class="layui-col-md4">' +
							'<div class="in-dish">';
						if(obj.embryoCount > 0 && obj.procedureId !== null && obj.procedureId !== ""){
							divHtml = divHtml + '<div class="dish-num"><span>' + obj.dishCode + '</span><a href="/front/dish?procedureId=' + obj.procedureId + '&dishId=' + obj.dishId + '&dishCode=' + obj.dishCode + '" target="_blank">查看皿</a></div>';
						} else {
							divHtml = divHtml + '<div class="dish-num"><span>' + obj.dishCode + '</span><a>查看皿</a></div>';
						}
						divHtml = divHtml + '<ul class="dish-info">' +
							'<li>Dish # <span>' + obj.dishCode + '</span></li>' + 
							'<li>本皿胚胎数<span>' + obj.embryoCount + '</span></li>' +
							'<li>胚胎总数<span>' + obj.embryoSum + '</span></li>' +
						'</ul>' ;
						if(obj.embryoCount > 0){
							// divHtml = divHtml + '<div class="patient-info" index=' + i + ' onclick="lookCase('+ obj.procedureId +')">' + 
							divHtml = divHtml + '<div class="patient-info" index=' + i + ' >' + 
							'<span>查看病历</span>' +
							'<div class="case-details" id="caseDiv_' + i + '" style="display:none;">' +  
								'<dl>' + 
									'<dt><strong>姓名</strong><span>' + obj.name + '</span></dt>' +
									'<dt><strong>授精时间</strong><span>' + obj.insemiTime + '</span></dt>' +
									'<dt><strong>开始采集时间</strong><span>' + obj.imagePath + '</span></dt>' +
									'<dt><strong>年龄</strong><span>' + obj.age + '</span></dt>' + 
									'<dt><strong>授精方式</strong><span>' + obj.insemiType + '</span></dt>' + 
									'<dt><strong>阶段</strong><span>' + obj.stage + '</span></dt>' +
								'</dl>' +
							'</div></div>';
						} else {
							divHtml = divHtml + '<div class="patient-info" index=' + i + ' ><span>查看病历</span><div class="case-details" id="caseDiv_' + i + '" style="display:none;"> <dl><dt><span>暂无病历信息</span></dt></dl> </div></div>';
						}
						divHtml = divHtml + '</div></div>';
					}
				}
				if(data.count < 9){
					for (let i = data.count; i < 9; i++) {
						divHtml = divHtml + '<div class="layui-col-md4">' +
							'<div class="in-dish">' + 
								'<div class="dish-num"><span> 空 </span><a>查看皿</a></div>' +
								'<ul class="dish-info">' +
									'<li>Dish # <span> 空 </span></li>' + 
									'<li>本皿胚胎数<span> 0 </span></li>' +
									'<li>胚胎总数<span> 0 </span></li>' +
								'</ul>' + 
								'<div class="patient-info" index=' + i + ' >' + 
									'<span>查看病历</span>' + 
									'<div class="case-details" id="caseDiv_' + i + '" style="display:none;"> ' + 
										'<dl><dt><span>暂无病历信息</span></dt></dl>' + 
									'</div>' +
								'</div>' + 
							'</div>' +
						'</div>';
					}
				}
			}
			
			$("#dishDiv").html(divHtml);

			// 查看病历
			$('#dishDiv .patient-info').hover(function(){
				const index = $(this).attr('index');
				$('#caseDiv_'+index).show();
			},function(){
				const index = $(this).attr('index');
				$('#caseDiv_'+index).hide();
			});
        }
    });
}

function lookCase(procedureId){
	layer.open({
		title : "病历详情",
		type : 2,
		area : [ '1020px', '610px' ],
		maxmin : true,

		shadeClose : false,
		content : '/front/procedure/' + procedureId
	});
}