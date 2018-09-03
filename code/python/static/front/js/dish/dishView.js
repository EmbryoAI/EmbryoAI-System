var currentSeris = "";//基准的胚胎的时间序列
var n = 0;
var imgLen = 1  // 已基准孔的图片张数为标准
layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
	//增加加载层 LYZ
	jaindex = layer.msg('渲染皿视图中，请耐心等待', {
		  icon: 16
		  ,shade: 0.3,time:0
	});
    $(function () {
		// 加载胚胎标记状态
		loadEmbryoResultTool("'embryo_fate_type'");
		
		//加载12个孔的缩略图
		for(var i=1;i<=12;i++) {
			queryThumbnailImageUrl(i);
		}
		//  var bfwc = false;
		//  var thisObj = null;
		//  $('#playBtn').click(function () {
		// 	var oVideo = document.getElementsByClassName('videoSource');
		// 	var i;
		// 	thisObj = $(this);
        //     if ($(this).hasClass('play')) {
        //         $(this).removeClass('play');
        //         $(this).addClass('stop');
		// 		$(this).children("span").text("暂停");
		// 		for (i = 0; i < oVideo.length; i++) {
		// 			if(!bfwc) {
		// 		        oVideo[i].addEventListener("ended",function(){
		// 	        	  console.log(new Date().getTime());
		// 	        	  thisObj.removeClass('stop');
		// 	        	  thisObj.addClass('play');
		// 	        	  thisObj.children("span").text("播放");
		// 		        });
				      
		// 			}
		// 			oVideo[i].play();
		// 		}
		// 		bfwc = true;
        //     } else {
        //         $(this).removeClass('stop');
        //         $(this).addClass('play');
		// 		$(this).children("span").text("播放");
		// 		for (i = 0; i < oVideo.length; i++) {
		// 			oVideo[i].pause();
		// 		}
        //     }
		// })
		


	// 滚动效果
	var imgTime;
	// 点击播放暂停
	$('#playBtn').click(function () {
		if ($(this).hasClass('play')) {
			var flag = isStandard();
			if(!flag){
				layer.msg("请先选择一个孔的胚胎为基准胚胎!")
				return;
			}
			imgLen = $('.active img').length;
			
			$(this).removeClass('play');
			$(this).addClass('stop');
			$(this).children("span").text("暂停");
			function run() {
				if (n < imgLen) {
					n = n;
				} else {
					n = 0;
					payWc();//播放完成或者暂停时调用
				}
				n++;
				$(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img").hide();
				$(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();
			}
			imgTime = setInterval(run, 1000);
							
		} else {
			payWc();//播放完成或者暂停时调用
		}
	})
	
	function payWc() {
		$('#playBtn').removeClass('stop');
		$('#playBtn').addClass('play');
		$('#playBtn').children("span").text("播放");
		
		var imageVideoId = $("#dishImageUl .active img:eq(" + n + ")").attr("id");
		currentSeris = imageVideoId.substring(10,imageVideoId.length-1);;//设置基准胚胎的时间序列
		clearInterval(imgTime);
	}





		// 胚胎评分表
		 $('.em-grade').on('click', function(){
			layer.open({
			  type: 2,
			  title: '胚胎评分表',
			  maxmin: true,
			  shadeClose: true, 
			  area : ['900px' , '220px'],
			  content: 'emGrade.html'
			});
		});
		  
		// 胚胎总览表
		 $('.em-all').on('click', function(){
			layer.open({
			  type: 2,
			  title: '胚胎总览表',
			  maxmin: true,
			  shadeClose: true, 
			  area : ['900px' , '520px'],
			  content: 'emAll.html'
			});
		});

		$("#embryo_fate_type_ul").on('click', 'li', function () {
			const self = $(this),index = $(this).attr('data-end');
			if (self.hasClass('active')) {
				self.removeClass('active');
				$('.dish-box').css("cursor","auto")
			}else{
				$("#embryo_fate_type_ul li").removeClass('active');
				self.addClass('active');
				$('.dish-box').css("cursor", "url('/static/front/img/cursor"+index+".png'),auto");
			}
		});
		
		$('#dishImageUl li').click(function(){
			const self = $(this),
			calssName = self.children('i').attr('class');

			var embryoId= self.attr("embryoId");
			var type = $("#embryo_fate_type_ul .active").attr("name");
			//判断是否选中胚胎结果标记工具
			var isActive = $("#embryo_fate_type_ul").children("li").hasClass("active");
			if(isActive){
				if(type === "standard"){
					// 设置为基准胚胎
					$('#dishImageUl li').removeClass('active');
					$('#dishImageUl li span').remove('.standard');
					self.addClass('active');
					self.append("<span class='standard' ></span>")
					var wellCode = self.attr("wellCode");
					$("#time_box_div").show();
					loadTimeline(wellCode);
					
					var imageVideoId = $("#dishImageUl .active img:eq(" + n + ")").attr("id");
					currentSeris = imageVideoId.substring(10,imageVideoId.length-1);;//设置基准胚胎的时间序列
				} else {	
					//胚胎结果标记
					self.children('i').remove();
					var embryoFateId = 0;
					var appendData = "<i class='" + type + "'></i>";
					if(calssName !== type){
						embryoFateId = $('.dish-tool .tool-end .active').attr("data-end");
					}
					signEmbryoResult(self,appendData,embryoId,embryoFateId);
				}
			}
			
		})
		
		$('#cancelEnd').click(function(){
			$("#embryo_fate_type_ul li").removeClass('active');
			$('.dish-box').css("cursor","auto")

		})
		
		//初始化12个孔的缩略图
		function queryThumbnailImageUrl(wellId) {
			$.ajax({
				type : "get",
				url : "/api/v1/image/pay/queryThumbnailImageUrl",
				datatype : "json",
				cache:false,
				data : {"procedureId":$("#procedureId").val(),"dishId":$("#dishId").val(),"wellId":wellId},
				success : function(data) {
					 if(data!=null) {
						 thumbnailImageUrlList = data;
			    		 $(".dishbox"+wellId).html("");
			    		 var embryoId = "";
				    	 for(var i=0;i<thumbnailImageUrlList.length;i++) {
				    		 var image = "";
				    		 var obj = thumbnailImageUrlList[i];
				    		 embryoId = obj.embryoId;
				    		 if(i==0) {
								 var image = "<img index='"+(i+1)+"' embryoId='"+embryoId+"' id='imageVideo"+obj.timeSeries+wellId+"'  src='/api/v1/well/image?image_path="+obj.thumbnailUrl+"' />";
				    		 }else {
								 var image = "<img index='"+(i+1)+"' embryoId='"+embryoId+"' id='imageVideo"+obj.timeSeries+wellId+"'  src='/api/v1/well/image?image_path="+obj.thumbnailUrl+"' />";
								 $("imageVideo"+obj.timeSeries).hide();
				    		 }
							 $(".dishbox"+wellId).append(image);
						 }
				    	 //给孔的li增加embryoId
						 $(".dishbox"+wellId).attr("embryoId",embryoId);
						 $(".dishbox"+wellId).attr("wellCode",wellId);
					 }else {
						 
					 }
					 
					 if(wellId==12) {
						 setTimeout(function(){layer.close(jaindex);},5000);
					 }
				},
				error : function(request) {
					layer.alert(request.responseText);
				}
			});
		}

		//查询病例信息
		getProcedureInfo($("#procedureId").val());
		
		
		$(document).keydown(function(event){
		    if(event.which == "37"){
		        preFrame();
		    }
		    if(event.which == "39"){
		        nextFrame();
		    }
		    if(event.which == "38"){
		    	node("up");
		    }
		    if(event.which == "40"){
		    	node("down");
		    }
		});
    });
})

//加载胚胎标记状态
function loadEmbryoResultTool(dictClass) {
	$.ajax({
		type : "get",
		url : "/api/v1/dict/lists/"+dictClass,
		datatype : "json",
		success : function(data) {
			if (data.code == 0) {
				for (var i = 0; i < data.data.length; i++) {
					var obj = data.data[i];
					var divId = obj.dictClass;
					var str="";
					if(obj.dictClass=="embryo_fate_type") {//如果为标记的，需要特殊处理
						divId = divId + "_ul";
						str = "<li class='"+obj.dictSpare+"' name='"+obj.dictSpare+"' data-end='"+obj.dictKey+"'><i></i><span>"+obj.dictValue+"</span></li>";
					}
					$("#"+divId).append(str);
				}
			} else {
				layer.alert(data.msg);
			}
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//根据 胚胎id 保存胚胎标记结果
function signEmbryoResult(obj,appendData,embryoId,embryoFateId){
	$.ajax({
		type : "get",
		url : "/api/v1/embryo/sign/"+ embryoId +"/"+embryoFateId,
		datatype : "json",
		cache:false,
		success : function(data) {
			if(appendData != "" && embryoFateId != 0){
				obj.append(appendData);
				layer.msg("标记成功");
			} else {
				layer.msg("取消标记");
			}
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//var bfzt =0;//播放狀態  0未播放  1播放
//var oVideo = document.getElementsByClassName('videoSource');
//function playVideo(videoNum) {
//	if(oVideo[videoNum]!=null && oVideo[videoNum]!=undefined) {
//		bofang(oVideo[videoNum]);
//	}
//}
//function bofang(oVideo) {
////    if ($(this).hasClass('play')) {
////        $(this).removeClass('play');
////        $(this).addClass('stop');
////        $(this).children("span").text("暂停");
//        oVideo.addEventListener("ended",function(){
//        	  var myDate = new Date();//获取系统当前时间
//        	  console.log(myDate.getTime());
////	          $(this).removeClass('stop');
////	          $(this).addClass('play');
////	          $(this).children("span").text("播放");
//		 });
//         oVideo.play();
////    } else {
////        $(this).removeClass('stop');
////        $(this).addClass('play');
////        $(this).children("span").text("播放");
////        oVideo.pause();
////    }
//}

		// 时间轴
		$('#timelineDiv').on('click','span',function(){
			$(this).siblings('span').removeClass('active');
			$(this).addClass('active');
			var activeTime = $(this).attr("serie");
			$(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img").hide();
			for (let i = 1; i <= 12; i++) {
				if($("#imageVideo"+activeTime+i) !== undefined){
					$("#imageVideo"+activeTime+i).show();
				}
			}

		})

function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
    return currentdate;
}

//根据当前基准的胚胎ID，切换12孔的里程碑
function node(upOrdown) {
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
	var flag = isStandard();
	if(!flag){
		layer.msg("请先选择一个孔的胚胎为基准胚胎!")
		return;
	}
	var embryoId = getStandardEmbryoId();
	$.ajax({
		type : "get",
		url : "/api/v1/milestone/node/"+embryoId+"/"+currentSeris+"/"+upOrdown,
		datatype : "json",
		cache:false,
		success : function(data) {
			 if(data!=null) {
				 $(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img").hide();
				 //把12个孔的都设置为对应基准胚胎里程碑时间序列的缩略图
				 for (var i = 1; i <= 12; i++) {
					 //把这个张图显示
					 if($("#imageVideo"+data.milestoneTime+i)!=undefined) {
						 $("#imageVideo"+data.milestoneTime+i).show();
					 }
				 }
				 currentSeris = data.milestoneTime;//设置基准胚胎的时间序列
			 }else {
				 if("up"==upOrdown) {
					 layer.alert("当前已经是第一个里程碑了!");
				 }else {
					 layer.alert("当前已经是最后一个里程碑了!");
				 }
			 }
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//判断是否已选择基准胚胎
// true:表示已选中；false：表示未选中
function isStandard(){
	var isActive = $("#dishImageUl li").hasClass("active");
	if(isActive){
		return true;
	} else {
		return false;
	}
}

//获取选中的基准胚胎id
function getStandardEmbryoId(){
	var embryoId = $("#dishImageUl .active").attr("embryoId");
	return embryoId;
}

// 上一张
function preFrame() {
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
	var flag = isStandard();
	if(!flag){
		layer.msg("请先选择一个孔的胚胎为基准胚胎!")
		return;
	}
	imgLen = $('.active img').length;
	if (n > 0) {
		n = n - 1;
	} else {
		n < imgLen - 1;
		layer.msg("已经是第一张了")
	}
	$(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img").hide();
	$(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();
}

// 下一张
function nextFrame() {
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
	var flag = isStandard();
	if(!flag){
		layer.msg("请先选择一个孔的胚胎为基准胚胎!")
		return;
	}
	imgLen = $('.active img').length;
	if (n < imgLen - 1) {
		n = n + 1;

	} else {
		n = imgLen - 1;
		layer.msg("已经是最后一张了")
	}
	$(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img").hide();
	$(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();

}


//根据基准胚胎加载时间轴
function loadTimeline(wellCode){
	var dishId = $("#dishId").val();
	var procedureId = $("#procedureId").val();

	$.ajax({
		type : "get",
		url : "/api/v1/dish/loadSeriesList",
		data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellCode},
		datatype : "json",
		cache:false,
		success : function(data) {
			var divData = "";
			if(data !== null && data !== "" && data !== "[]"){
				for (let i = 0; i < data.length; i++) {
					const obj = data[i];
					divData = divData + "<span serie=" + obj["serie"] + ">" + obj["showTime"] + "</span>";
				}
			}
			$("#timelineDiv").html(divData);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
	
}

function getProcedureInfo(procedureId){
	$.ajax({
		type : "get",
		url : "/api/v1/procedure/" + procedureId,
		datatype : "json",
		cache:false,
		success : function(data) {
			var procedure = data.data;
			$('#patienName').html(procedure.patient_name);
			$('#patientAge').html(procedure.patient_age + '岁');
			$('#ecTime').html(procedure.ec_time);
			$('#ecCount').html(procedure.ec_count);
			$('#insemiTime').html(procedure.insemi_time);
			$('#insemiType').html(procedure.insemi_type);
			$('#embryoNum').html(procedure.embryo_num);
			$('#memo').html(procedure.memo);
			$('#mobile').val(procedure.mobile);
			$('#email').val(procedure.email);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

function updateMemo(){
	var procedureId = $("#procedureId").val();
	var mobile = $("#mobile").val();
	var email = $("#email").val();
	var memo = $("#memo").val();
	$.ajax({
		type : "POST",
		url : "/api/v1/procedure/info",
		data : {"id":procedureId,"mobile":mobile,"email":email,"memo":memo},
		datatype : "json",
		cache:false,
		success : function(data) {
			alert(JSON.stringify(data));
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}