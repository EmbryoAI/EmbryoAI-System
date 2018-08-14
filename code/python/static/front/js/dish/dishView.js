layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {
		// 加载胚胎标记状态
		loadEmbryoResultTool("'embryo_fate_type'");

        //上一张 下一张
        var n = 0;
        $(".dishimg li img").hide();
        $(".dishimg li img:first").show();
        // 上一张
        $(".pre-frame").click(function () {
            if (n > 0) {
                n = n - 1;
            } else {
                n < $(".dishimg li img").length - 1;
                layer.msg("已经是第一张了")
            }
            $(".dishimg li img").hide();
            $(".dishimg li img:eq(" + n + ")").show();
        });
        // 下一张
        $(".next-frame").click(function () {
            if (n < $(".dishimg li img").length - 1) {
                n = n + 1;

            } else {
                n = $(".dishimg li img").length - 1;
                layer.msg("已经是最后一张了")
            }
            $(".dishimg li img").hide();
            $(".dishimg li img:eq(" + n + ")").show();
        })

        // 滚动效果
        var textTime;
        var imgTime;
        // 点击播放暂停
        $('#playBtn').click(function () {
            if ($(this).hasClass('play')) {
                $(this).removeClass('play');
                $(this).addClass('stop');
                $(this).children("span").text("暂停");

                function showText() {
                    n = n + 1;
                }
                textTime = setInterval(showText, 200);

                function run() {
                    if (n < $(".dishimg li img").length) {
                        n = n;
                    } else {
                        n = 0
                    }
                    $(".dishimg li img").hide();
                    $(".dishimg li img:eq(" + n + ")").show();
                }
                imgTime = setInterval(run, 200);

            } else {
                $(this).removeClass('stop');
                $(this).addClass('play');
                $(this).children("span").text("播放");
                clearInterval(textTime);
                clearInterval(imgTime);
            }
        })
		
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
					$('.dishimg li').removeClass('active');
					$('.dishimg li span').remove('.standard');
					self.addClass('active');
					self.append("<span class='standard'></span>")
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