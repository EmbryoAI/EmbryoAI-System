var form = null;
//最清晰的jpg对应的z轴位置
var sharpZIndex = null;
//采集时间
var acquisitionTime = null;
//目录
var path = null;
var procedureId = "";
var dishId = "";
var wellId = "";
var cellId = "";
var lastSeris = "";
var jaindex = "";
var currentSeris = "";
var seris = "";
var drwaType = "";
var clearImageUrlList="";
var current_seris_image_path = "";
var imgVideoZt = "";
var embryoId = "";
var currentSerisName = "";
var firstSeris = "";
var n = 0;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
	//增加加载层 LYZ
	jaindex = layer.msg('渲染胚胎视图中，请耐心等待', {
		  icon: 16
		  ,shade: 0.3,time:0
	});
    $(function () {
    	//初始化所有字典值 对应的radio 按钮等。
    	//动态初始化里程碑的值,字典表milestone
		//初始化PN数，字典值pn
		//初始化均匀度,字典even
		//初始化碎片率，字典fragment
		//初始化评分,字典grade
		//初始化胚胎结局字典值ID -> sys_dict.id，字典值类型为embryo_fate_type，可能取值包括：1：移植；2：冷冻；3：丢弃；4：待定
    	dict = chushihua("'milestone','pn','even','fragment','grade','embryo_fate_type'");
    	
    	//获取孔
        procedureId = $("#procedureId").val();
        dishId = $("#dishId").val();
        wellId = $('#cellCode').val();
        //页面初始化获取所有图片路径和所有时间序列
        $.ajax({
            type : "get",
            url : "/api/v1/image/pay/queryClearImageUrl",
            datatype : "json",
            cache:false,
            data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId},
            success : function(data) {
                 if(data!=null) {
                     clearImageUrlList = data;
                 }
            },
            error : function(request) {
                layer.alert(request.responseText);
            }
        });

        $.ajax({
            cache : false,
            type : "GET",
            url : "/api/v1/well/list/" + procedureId + "/" + dishId + "/" + wellId,
            data : "",
            error : function(request) {
                parent.layer.alert(request.responseText);
            },
            success : function(data) {
                var milestoneList = data.milestone_list;
                var well = "";
                var wellList = data.well_list;
                var cellCode = $('#cellCode').val();
                for(var i=0;i<wellList.length;i++){
                    if((i+1) == cellCode){
                        well = well + "<li id=\"li_" + i + "\" class=\"active\" onclick=\"querySeriesList('" + wellList[i].well_code 
                        + "','" + wellList[i].last_embryo_serie + "',0,'" +  wellList[i].well_id + "')\"><span onclick=\"clickLi('" + i + "')\">well" + 
                        wellList[i].well_code + "</span></li>";
                        cellId = wellList[i].well_id;
                        lastSeris = wellList[i].last_embryo_serie;
                    }else{
                        well = well + "<li id=\"li_" + i + "\" onclick=\"querySeriesList('" + wellList[i].well_code 
                        + "','" + wellList[i].last_embryo_serie + "',0,'" +  wellList[i].well_id + "')\"><span onclick=\"clickLi('" + i + "')\">well" + 
                        wellList[i].well_code + "</span></li>";
                    }
                   
                }

               
                $("#siteitem").html(well);
                wellId = cellCode;
                
                querySeriesList(wellId,lastSeris,0, cellId);//获取每个孔下面的时间序列
            }
        });


        // 点击切换样式
        $('.swiper-wrapper .swiper-slide').click(function () {
            $('.swiper-wrapper .swiper-slide').removeClass('active');
            $(this).addClass('active');
            $(this)
        });

        $('.siteitem li').click(function () {
            $('.siteitem li').removeClass('active');
            $(this).addClass('active');
        });

        

		// // z轴点击样式
		// $('.time-vertical li').click(function () {
		// 	$('.time-vertical li').removeClass('active');
		// 	$(this).addClass('active');
		// });
		

        // 选为最清晰的值提示
        $("#distinct").on("click", function (event) {
            var checked = $("#distinct").prop("checked");
            if(checked){
                var imageName = $(".time-vertical .active").attr("zjpg");
                var imageIndex = $(".time-vertical .active").attr("zindex");
                $.ajax({
                    cache : false,
                    type : "POST",
                    url : "/api/v1/image/markDistinct",
                    data : {"path":path,"imageName":imageName,"timeSeries":currentSeris,"wellId":wellId},
                    async : false,
                    error : function(request) {
                    	layer.alert(request.responseText);
                    },
                    success : function(data) {
                        console.info(data);
                        if(data.code == '200'){
                            sharpZIndex = imageIndex;
                            $("#distinct").prop("disabled",true);
                            layer.msg('已标注为最清晰的图片');
                            var url = $("#"+currentSeris).prop("src") + "&random=" + Math.random() ;
                            $("#"+currentSeris).prop("src",url);
                            if(imgVideoZt=="") {//如果没有播放过则更新全部图片
                            	queryClearImageUrl();
                            }else {//如果播放过则替换当前位置的图片
                            	//把当前设置为最清晰图的URL替换到 图片播放的DIV层中  首先拼接当前设置为最清晰图的URL
                            	var qximgUrl = path+currentSeris+"\\"+imageName;//拼接当前设置为最清晰图的URL
                            	//替换div中的img为 当前设置为最清晰图
                            	$("#imageVideo"+currentSeris).prop("src","/api/v1/well/image?image_path="+qximgUrl);
                            	//替换播放图片集合的值为 当前设置为最清晰图
                            	for (var int = 0; int < clearImageUrlList.length; int++) {
                            		if(currentSeris==clearImageUrlList[int].timeSeries) {//替换时间序列相等的图片URL
                            			clearImageUrlList[int].clearImageUrl = qximgUrl;
                            		}
								}
                            }
                        } else {
                            layer.msg('标注为最清晰的图片失败');
                        }
                    }
                });
                
            }
        });

        // 选中里程碑出现的内容
        form.on('checkbox(milestone)', function (data) {
            const a = data.elem.checked;

            if (a == true) {
                // layer.msg('打开');
                $('#milestone').animate({
                    height: '123px'
                });
               var value = $('[name=milestoneId]:checked').val();
               
               if(value!=undefined) {
                showHide(value);
               }
               $("#milestoneFormSubDiv").show();
            } else {
                // layer.msg('关闭');
                $('#milestone').animate({
                    height: '31px'
                });
        		$("#countDiv").hide();
        		$("#evenDiv").hide();
        		$("#fragmentDiv").hide();
        		$("#gradeDiv").hide();
        		$("#pnDiv").hide();
        		$("#embryoDiv").hide();
        		$("#embryoSjDiv").hide();
        		$("#stageDiv").hide();
        		$("#milestoneFormSubDiv").hide();
            }

        });

        // 播放暂停按钮的切换

        //上一张 下一张

        
        $(".lg-img img").hide();
        $(".lg-img img:first").show();
        // 上一张
        $(".pre-frame").click(function () {
            if (n > 0) {
                n = n - 1;
            } else {
                n < $(".lg-img img").length - 1;
            }
            $(".lg-img img").hide();
            $(".lg-img img:eq(" + n + ")").show();
        });
        // 下一张
        $(".next-frame").click(function () {
            if (n < $(".lg-img img").length - 1) {
                n = n + 1;

            } else {
                n = $(".lg-img img").length - 1;
            }
            $(".lg-img img").hide();
            $(".lg-img img:eq(" + n + ")").show();
        })

        // 滚动效果
       
        var imgTime;
        // 点击播放暂停
        $('#playBtn').click(function () {
            if ($(this).hasClass('play')) {
            
                $(this).removeClass('play');
                $(this).addClass('stop');
                $(this).children("span").text("暂停");
                $(".lg-video-img img:eq(" + n + ")").show();
                function run() {
                    if (n < $(".lg-video-img img").length) {
                        n = n;
                    } else {
                        n = 0;
                    	//播放完成 或者 暂停调用
                    	payWc();
                    }
                    n++;
                    $(".lg-video-img img").hide();
                    $(".lg-video-img img:eq(" + n + ")").show();
                }
            	$("#imgDiv").hide();
            	$("#zIndexDiv").hide();
            	$("#imgVideoDiv").show();
                imgTime = setInterval(run, 200);
                
            } else {
            	//播放完成 或者 暂停调用
            	payWc();
            }
        })
        
        function payWc() {
        	$("#imgVideoDiv").hide();
        	$("#imgDiv").show();
        	$("#zIndexDiv").show();
        	$('#playBtn').removeClass('stop');
        	$('#playBtn').addClass('play');
        	$('#playBtn').children("span").text("播放");
            //截取出图片src中的时间序列
            var imgsrc = $(".lg-video-img img:eq(" + n + ")").attr("src");
		    var image = "<img src='"+imgsrc+"' />";
            $("#imgDiv").html(image);
            var imageVideoId = $(".lg-video-img img:eq(" + n + ")").attr("id");
            var timeSeries =  imageVideoId.substring(10,imageVideoId.length);
            
            querySeriesList(wellId, timeSeries, 1, cellId);
            
//            getBigImage(procedureId, dishId, wellId, timeSeries,1,cellId, currentSerisName);//定位到对应的时间序列
            //记录一下当前暂停图片的URL
            imgVideoZt = $(".lg-video-img img:eq(" + n + ")").attr("id");
            
            clearInterval(imgTime);
        }
        
        //记录最新的标记状态值
        var embryoFateIdQj = "";
        // 标记结局
        $(".tool-end").on('click', 'li[data-end]', function () {
            var indexData = $(this).attr('data-end');
            var indexName = $(this).attr('class');
            var embryoFateId = indexData;
            var markData = $(".mark i").attr('data-mark');
            var markName = $(".mark i").attr('class');
            
            if (markData == "" || markName == "" || embryoFateIdQj!=indexData) {//添加标记
            	
            }else {//取消标记
            	embryoFateId = 0;
            }
			$.ajax({
				type : "get",
				url : "/api/v1/embryo/sign/"+$("#embryoId").val()+"/"+embryoFateId,
				datatype : "json",
				cache:false,
				success : function(data) {
			            if (markData == "" || markName == "" || embryoFateIdQj!=indexData) {
			                $(".mark i").attr('data-mark', indexData);
			                $(".mark i").attr('class', indexName);
			                layer.msg("标注成功")
			            } else {
			                $(".mark i").attr('data-mark', "");
			                $(".mark i").attr('class', "");
			                layer.msg("已取消标注")
			            }
			            embryoFateIdQj = indexData;
				},
				error : function(request) {
					layer.alert(request.responseText);
				}
			});
        })
		var canvas = document.getElementById('canvas'); // 得到画布
		var ctx = canvas.getContext('2d'); // 得到画布的上下文对象
		var flag = false;
		var x = 0; // 鼠标开始移动的位置X
		var y = 0; // 鼠标开始移动的位置Y
        var url = ''; // canvas图片的二进制格式转为dataURL格式
        var x1 ;
        var y1 ;
        
		
		// function canvasWidth(){
		// 	var embr = document.getElementById('embryo');
		// 	var canvasBox = document.getElementById('canvasBox');
		// 	canvasBox.style.width = embr.offsetWidth;
		// 	canvas.width = canvasBox.offsetWidth;
		// 	canvas.height = canvasBox.offsetHeight;
		// }
		// canvasWidth();
		
		/* 为canvas绑定mouse事件 */
		
		
		$(".tool-metrical li").click(function(){
            var self= $(this)
            var datali = $(this).attr('data-li');
			$(".tool-metrical li").removeClass("active");
            self.addClass("active"); 
            console.log(datali)
            if ( datali == 1) {
                
                $('canvas').mousedown(function(e){
                    flag = true;
                    x = e.offsetX; // 鼠标落下时的X
                    y = e.offsetY; // 鼠标落下时的Y
                    console.log("落下的坐标"+x,y)
                }).mouseup(function(e){
                    flag = false;
                    url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
                    x1 = e.offsetX; // 鼠标起时的X
                    y1 = e.offsetY; // 鼠标起下时的Y
                    console.log("放开的坐标"+x1,y1)
                    var rx = (x1-x);
                    var ry = (y1-y);
                    var r = Math.sqrt(rx*rx+ry*ry); 
                    r = Math.round(r*(1280 / 932)/3.75);
                    $('#length').text(r);

                        layer.open({
                        type: 1,
                        area: ['300px', '280px'],
                        shadeClose: false, 
                        content: $("#dbox-l"),
                        btn:["确认导入","取消"],
                        yes: function(index, layero){;
                            layer.closeAll();
                            layer.msg("导入成功！")
                            clearCanvas()

                            var zonaThickness = $('#zonaThickness').val();
                            $('#hideZonaThickness').val(zonaThickness);
                            $('#zonaThickness').val(r);
                        }
                        ,btn2: function(index, layero){
                            clearCanvas()
                        },cancel: function(){ 
                            clearCanvas()
                        },
                        btnAlign: 'c'
                    });
                    $('canvas').unbind();
		        	$(".tool-metrical li").removeClass("active");

                }).mousemove(function(e){
                        drawLine(e); // 直线绘制方法
                });
            }
            if ( datali == 2) {
                $('canvas').mousedown(function(e){
                    flag = true;
                    x = e.offsetX; // 鼠标落下时的X
                    y = e.offsetY; // 鼠标落下时的Y
                    console.log("落下的坐标"+x,y)
                }).mouseup(function(e){
                    flag = false;
                    url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
                    x1 = e.offsetX; // 鼠标起时的X
                    y1 = e.offsetY; // 鼠标起下时的Y
                    console.log("放开的坐标"+x1,y1)

                    var rx = (x1-x);
                    var ry = (y1-y);
                    var r = Math.sqrt(rx*rx+ry*ry);
                    r = Math.round(r*(1280/932)/3.75);
                    $('#diameter').text(r);
                    var area = Math.round(Math.PI * r/2 * r/2);
                    $('#area').text(area);
                    layer.open({
                        type: 1,
                        area: ['300px', '280px'],
                        shadeClose: false, 
                        content: $("#dbox-c"),
                        btn:["确认导入","取消"],
                        yes: function(index, layero){
                            layer.closeAll();
                            layer.msg("导入成功！")
                            clearCanvas()
                            var choseVal = $('#dbox-c input[name="2"]:checked ').val();
                            if(choseVal == 'choseIn'){
                                var innerArea = $('#innerArea').val();
                                $('#hideInnerArea').val(innerArea);
                                var innerDiameter = $('#innerDiameter').val();
                                $('#hideInnerDiameter').val(innerDiameter);
    
                                $('#innerArea').val(area);
                                $('#innerDiameter').val(r);
                            }
                            if(choseVal == 'choseOut'){
                                var outerArea = $('#outerArea').val();
                                $('#hideOuterArea').val(outerArea);
                                var outDiameter = $('#outDiameter').val();
                                $('#hideOutDiameter').val(outDiameter);
    
    
                                $('#outerArea').val(area);
                                $('#outDiameter').val(r);
                            }
                        }
                        ,btn2: function(index, layero){
                            clearCanvas()
                        },cancel: function(){ 
                            clearCanvas()
                        },
                        btnAlign: 'c'
                    });
                $('canvas').unbind();
                $(".tool-metrical li").removeClass("active");
                }).mousemove(function(e){
                        drawCircle(e); // 圆形绘制方法	
                });
            }
               
       })

       
	   
	   // 画圆
	   function drawCircle(e){
		   if(flag){
			   ctx.clearRect(0,0,canvas.width,canvas.height);
			   ctx.beginPath();
			   var rx = (e.offsetX-x)/2;
			   var ry = (e.offsetY-y)/2;
			   var r = Math.sqrt(rx*rx+ry*ry);
			   ctx.arc(rx+x,ry+y,r,0,Math.PI*2); // 第5个参数默认是false-顺时针
			   ctx.stroke();
			   ctx.strokeStyle ="#ffee19" ; 
			   ctx.lineWidth = 2; 
           }
           console.log(r)
	   }
	   
	   // 画直线
	   function drawLine(e){
		   if(flag){
			   ctx.clearRect(0,0,canvas.width,canvas.height);
			   ctx.beginPath();
			   ctx.moveTo(x,y);
			   ctx.lineTo(e.offsetX,e.offsetY);
			   ctx.stroke();
			   ctx.strokeStyle ="#ffee19" ; 
			   ctx.lineWidth = 2; 
		   }
	   }
	   // 清除画布
		   function clearCanvas()
			   {
				   ctx.clearRect(0,0,canvas.width,canvas.height);
			   }
            function loadImage(){
                var img = new Image();
                img.src = url;
                ctx.drawImage(img,0,0,canvas.width,canvas.height);
            }
		
		// 跟随屏幕改变的设定	
		$(window).resize(function () {
		
	
			
		});
	   
		form.on('radio(milestoneId)', function(data){
			var title = data.elem.title;
			var value = data.value;
			$("#stageId").html("("+title+")");
			showHide(value);
		});
		
		//监听提交
        form.on('submit(milestoneFormSub)', function (data) {
           
			var value = $('[name=milestoneId]:checked').val();
			if(value==undefined) {
				layer.alert("里程碑节点不能为空,请选择里程碑节点!");
				return false;
			}else if(value=="1") {//PN
				var pnId = $("input[name='pnId']:checked").val();
				if(pnId==undefined) {
					layer.alert("PN数不能为空,请选择PN数!");
					return false;
				}
			}else if(value=="2" || value=="3" || value=="4" || value=="5" || value=="6" ) {//2C
				var count = $("input[name='count']:checked").val();
				if(count==undefined) {
					layer.alert("细胞个数不能为空,请选择细胞个数!");
					return false;
				}
				
				var evenId = $("input[name='evenId']:checked").val();
				if(evenId==undefined) {
					layer.alert("均匀度不能为空,请选择均匀度!");
					return false;
				}
				
				if(value=="3" || value=="4" || value=="5" || value=="6") {
					var fragmentId = $("input[name='fragmentId']:checked").val();
					if(fragmentId==undefined) {
						layer.alert("碎片率不能为空,请选择碎片率!");
						return false;
					}
				}
				
				if(value=="6") {
					var gradeId = $("input[name='gradeId']:checked").val();
					if(gradeId==undefined) {
						layer.alert("评级不能为空,请选择评级!");
						return false;
					}
				}
			}else {
			 
			}
			

			
			var innerArea = $("#innerArea").val();
			if(innerArea=="") {
				layer.alert("胚胎内周面积不能为空,请输入胚胎内周面积!");
				return false;
			}
			
			var innerDiameter = $("#innerDiameter").val();
			if(innerDiameter=="") {
				layer.alert("胚胎内周直径不能为空,请输入胚胎内周直径!");
				return false;
			}
			
			var outerArea = $("#outerArea").val();
			if(outerArea=="") {
				layer.alert("胚胎外面积不能为空,请输入胚胎外面积!");
				return false;
			}
			
			var outDiameter = $("#outDiameter").val();
			if(outDiameter=="") {
				layer.alert("胚胎外直径不能为空,请输入胚胎外直径!");
				return false;
			}
			
			var expansionArea = $("#expansionArea").val();
			if(expansionArea=="") {
				layer.alert("扩张囊腔面积不能为空,请输入扩张囊腔面积!");
				return false;
			}
			
			var zonaThickness = $("#zonaThickness").val();
			if(zonaThickness=="") {
				layer.alert("透明带厚度不能为空,请输入透明带厚度!");
				return false;
			}
			
			
			$.ajax({
				cache : false,
				type : "post",
				url : "/api/v1/milestone/add",
				data : $(data.form).serialize(),// 你的formid
				error : function(request) {
					layer.alert(request.responseText);
				},
				success : function(data) {
					$("#embryoScoreSpanId").html(data.embryoScore)
					$("#milestoneScoreSpanId").html(data.milestoneScore);
					layer.alert("设置成功!");
				}
			});

            return false;
        });

    // 移动端点击侧滑出里程碑信息
		$('.btn-draw').click(function (){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
                $('.btn-draw i').text("←");
                $('.btn-draw span').text("查看里程碑信息");
                $(".info").animate({right:'-500px'});
                $(this).animate({right:'10px'});
                
			}else{
				$(this).addClass('active');
                $(".btn-draw i").text("→");
                $('.btn-draw span').text("关闭里程碑信息");
                $(".info").animate({right:'0px'});
                $(this).animate({right:'470px'});
                
			}
		})
    });
})

function clickLi(id){
    $('#siteitem li').removeClass('active');
    $('#li_' + id).addClass('active');
}

function resetData(){
    var hideOuterArea = $('#hideOuterArea').val();
    if(hideOuterArea != ''){
        $('#outerArea').val(hideOuterArea);
    }
    var hideOutDiameter = $('#hideOutDiameter').val();
    if(hideOutDiameter != ''){
        $('#outDiameter').val(hideOutDiameter);
    }
    var hideZonaThickness = $('#hideZonaThickness').val();
    if(hideZonaThickness != ''){
        $('#zonaThickness').val(hideZonaThickness);
    }
    var hideInnerDiameter = $('#hideInnerDiameter').val();
    if(hideInnerDiameter != ''){
        $('#innerDiameter').val(hideInnerDiameter);
    }
    var hideInnerArea = $('#hideInnerArea').val();
    if(hideInnerArea != ''){
        $('#innerArea').val(hideInnerArea);
    }
}

function loadingZIndex(procedureId,dishId,wellId,timeSeries){
    // alert("procedureId:"+procedureId+"--dishId:"+dishId+"--wellId:"+wellId+"--timeSeries:"+timeSeries);
    //加载z轴所以节点，并渲染
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/image/findAllZIndex",
        data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId,"timeSeries":timeSeries},
        error : function(request) {
        	layer.alert(request.responseText);
        },
        success : function(data) {
            var zIndexDivData = "";
            if(data.code == 200 && data.data != null){
                var length = data.data.fileEnd - data.data.fileStart;
                acquisitionTime = data.data.imagePath;
                path = data.data.path;
                var sharpJpg = data.data.sharp;
                zData = data.data.zIndexFiles;
                var zLi = "";
                for (var i = 1;i <= length; i++) {
                    if(sharpJpg === zData[i]) {
                        sharpZIndex = i;
                        zLi = "<li class='active' onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zindex=" + i + " zjpg='" + zData[i] + "'><b></b></li>" + zLi;
                    } else {
                        zLi = "<li onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zindex=" + i + " zjpg='" + zData[i] + "'><b></b></li>" + zLi;
                    }
                }
                zIndexDivData = zIndexDivData + "<a class='zarrowU' onclick=checkArrowZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','up')></a>"
                    + "<ul class='time-vertical'>" + zLi + "</ul>"
                    + "<a class='zarrowD' onclick=checkArrowZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','next')></a>"
                    + '<h6>z轴</h6>';
                $("#zIndexDiv").html(zIndexDivData);
                ini(acquisitionTime,timeSeries,path,sharpJpg);
            }
            
        }
    });
    $('#zIndexDiv').unbind("mousewheel");
    $('#zIndexDiv').bind('mousewheel', function(event, delta) {
        var zIndex = $(".time-vertical .active").attr('zindex');
        var length = $(".time-vertical li").length;
        if(delta > 0){
            zIndex = parseInt(zIndex) + 1;
            if(zIndex > length){
                zIndex = 1;
            }
        } else {
            zIndex = parseInt(zIndex) - 1;
            if(zIndex < 1){
                zIndex = length;
            }
        }
        $('.time-vertical li').removeClass('active');
        $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
        loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
        var imageName = $(".time-vertical li[zIndex="+zIndex+"]").attr("zjpg");
        ini(acquisitionTime,timeSeries,path,imageName)
        return false;    
    });
    
}

/**
 * 点击z轴上下箭头触发函数
 * @param {*} procedureId 
 * @param {*} dishId 
 * @param {*} wellId 
 * @param {*} timeSeries 
 * @param {*} arrowDirection 
 */
function checkArrowZIndex(procedureId,dishId,wellId,timeSeries,arrowDirection){
    var zIndex = $(".time-vertical .active").attr('zindex');
    var length = $(".time-vertical li").length;
    if(arrowDirection === "up"){
        zIndex = parseInt(zIndex) + 1;
        if(zIndex > length){
            zIndex = 1;
        }
    } else if (arrowDirection === "next"){
        zIndex = parseInt(zIndex) - 1;
        if(zIndex < 1){
            zIndex = length;
        }
    }
    $('.time-vertical li').removeClass('active');
    $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
    loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
    var imageName = $(".time-vertical li[zIndex="+zIndex+"]").attr("zjpg");
    ini(acquisitionTime,timeSeries,path,imageName);
}

/**
 * 选择z轴位置触发函数
 * @param {*} procedureId 
 * @param {*} dishId 
 * @param {*} wellId 
 * @param {*} timeSeries 
 * @param {*} zIndex 
 */
function checkZIndex(procedureId,dishId,wellId,timeSeries,zIndex){
    // alert("procedureId:"+procedureId+"--dishId:"+dishId+"--wellId:"+wellId+"--timeSeries:"+timeSeries+"--zIndex:"+zIndex);
    $('.time-vertical li').removeClass('active');
    $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
    loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
    var imageName = $(".time-vertical li[zIndex="+zIndex+"]").attr("zjpg");
//    ini(acquisitionTime,timeSeries,path,imageName)
}

/**
 * 加载胚胎页面大图
 * @param {*} procedureId 
 * @param {*} dishId 
 * @param {*} wellId 
 * @param {*} timeSeries 
 * @param {*} zIndex 
 */
function loadingImage(procedureId,dishId,wellId,timeSeries,zIndex){
    //alert("procedureId:"+procedureId+"--dishId:"+dishId+"--wellId:"+wellId+"--timeSeries:"+timeSeries+"--zIndex:"+zIndex);
    if(zIndex == null || zIndex == '' || sharpZIndex == zIndex){
        $("#distinctDiv").show();
        $("#distinct").prop("disabled",true);
        $("#distinct").prop("checked",true);
    } else {
        $("#distinctDiv").show();
        $("#distinct").prop("disabled",false);
        $("#distinct").prop("checked",false);
    }
    $.ajax({
        cache : true,
        type : "get",
        url : "/api/v1/image/getBigImagePath",
        data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId,"timeSeries":timeSeries,"zIndex":zIndex},
        success : function(data) {
            if (data.code == "200") {
                $("#imgDiv").html("<img src=" + data.data + ">");
            } else {
                layer.alert(data.msg);
                $("#imgDiv").html("");
            }
        },
        error : function(request) {
            layer.alert(request.responseText);
        }
    });
    current_seris_image_path = "/api/v1/image/findImage?procedureId="+ procedureId +"&dishId="+ dishId +"&wellId="+ wellId +"&timeSeries="+ timeSeries +"&zIndex=" + zIndex;
}

//羊城
function getImage(index, data){
    var result = '';
    for(var i=0;i<data.length;i=i+3){
        if(index == data[i]){
            result = data[i+1];
        }
    }
    return result;
}

function getCellId(index, data){
    var result = '';
    for(var i=0;i<data.length;i=i+3){
        if(index == data[i]){
            result = data[i+2];
        }
    }
    return result;
}

function querySeriesList(wellid, serisCode, type, cellId){
    currentSeris = serisCode;
    wellId = wellid;
    $("#wellId").val(wellId);
    $("#cellId").val(cellId);
    var dishId = $("#dishId").val();
    var index = indexOf(clearImageUrlList, serisCode)
    var startIndex = index - 5;
    var lastIndex = index + 5;
    var seris = "";

    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/list?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" 
                    + wellId + "&seris=" + serisCode,
        data : "",
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var series = data.series;
            var milestoneList = data.milestone_list;
            for(var i=0;i<=series.length-1;i++){
                var milestoneType = "<span></span>";
                for(var j=0;j<milestoneList.length;j++){
                    if(milestoneList[j].seris == series[i].series_code){
                        milestoneType = "<span>" + milestoneList[j].milestoneType + "</span>";
                    }
                }

                var imageUrl = series[i].series_image_path;
                if(imageUrl.indexOf('embryo_not_found.jpg') != -1){
                    imageUrl = "/static/front/img/loc-emb.png";
                }
                seris = seris + "<div class=\"swiper-slide\" id='" + series[i].series_code + "_div'><img src=\"" + 
                    imageUrl + "\" id='" + series[i].series_code + "' onclick=\"getBigImage('" + 
                    procedureId + "','" + dishId + "','" + wellId + "','" + series[i].series_code + "','0', '" + 
                    cellId + "','" + series[i].series_name + "')\">" + milestoneType + "<b>" + 
                    series[i].series_name + "</b></div>";

                if(serisCode == series[i].series_code){
                    currentSerisName = series[i].series_name;
                }
            }

            firstSeris = series[0].series_code;

            $("#myscrollboxul").html(seris);
            $("#xltext").html(currentSerisName);
            $("#" + serisCode + "_div").attr("class", "swiper-slide active");
            embryoId = milestoneList[0].embryoId;
            $("#embryoId").val(embryoId);

            if(data.last_embryo_serie == ''){
                parent.layer.alert('定位不到胚胎');
                return;
            }
            
            if(type==0) {
                loadingImage(procedureId,dishId,wellId,currentSeris,'');
                queryClearImageUrl();//初始化所有图片
                n = 0;
            }else if (type==1){
                n = $("#imageVideo"+currentSeris).attr("index");//根据时间序列同步播放的位置
            }else {
                loadingImage(procedureId,dishId,wellId,currentSeris,'');
                n = $("#imageVideo"+currentSeris).attr("index");//根据时间序列同步播放的位置
            }
            
            //由于切换孔了，需要根据胚胎ID加载一次患者信息
            $.ajax({
                type : "get",
                url : "/api/v1/embryo/patient/"+$("#embryoId").val(),
                datatype : "json",
                success : function(data) {
                    if (data.code == 0) {
                        $("#patientNameSpan").html(data.data.patient_name);
                        $("#patientAge").html(data.data.patient_age);
                        $("#embryoIndexSpan").html(data.data.embryo_index);
                        $("#zzjdSpan").html(data.data.zzjd);
                    } else {
                        layer.alert(data.msg);
                    }
                },
                error : function(request) {
                    layer.alert(request.responseText);
                }
            });
            
            loadingZIndex(procedureId,dishId,wellId,currentSeris);
        }
    });



    

}

/**
 * 获取当前序列的位置
 */
function indexOf(arr, item) {
    for(var i=0;i<arr.length;i++){
        if(arr[i].timeSeries == item){
            return i;
        }
    }
}

/**
 * 整体页面初始化
 * @param procedureId
 * @param dishId
 * @param wellId
 * @param seris
 * @param type 0默认方式 1播放暂停
 */
function getBigImage(procedureId, dishId, wellId, seris,type, cellId, serisName){
    currentSeris = seris;
    $("#myscrollboxul").children().each(function(){
        $(this).attr("class","swiper-slide");
        })
    $("#" + seris + "_div").attr("class", "swiper-slide active");
    $("#xltext").html(serisName);
    if(type==0) {
        loadingImage(procedureId,dishId,wellId,seris,'');
    }
    n = $("#imageVideo"+seris).attr("index");//根据时间序列同步播放的位置
    loadingZIndex(procedureId,dishId,wellId,seris);
}

function preFrame(){
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
    if(currentSeris == "0000000"){
        parent.layer.alert("已经是第一张了!");
        return;
    }
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/preframe?current_seris=" + currentSeris,
        data : "",
       
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            querySeriesList(wellId,data,2, cellId);
        }
    });
}

function nextFrame(){
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/nextframe?current_seris=" + currentSeris,
        data : "",
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            if(data == null){
                parent.layer.alert("已经是最后一张了!");
            }else{
                querySeriesList(wellId,data,2, cellId);
            }
        }
    });
}

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

function exportImg(){
    const aLink = document.createElement('a')
    aLink.download = currentSeris + '.jpg';
    aLink.href = current_seris_image_path; 
    aLink.dispatchEvent(new MouseEvent('click', {}))
}

function exportVideo(){
    var loadMsg = parent.layer.msg('视频导出中，请耐心等待', {
        icon: 16
        ,shade: 0.3,time:0
    });
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/video_path?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" + wellId,
        data : "",
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            const aLink = document.createElement('a')
            aLink.download = '孔' + wellId + '.mp4';
            aLink.href = data;
            aLink.dispatchEvent(new MouseEvent('click', {}))
            parent.layer.close(loadMsg);
        }
    });
}

function arrow(direction){
    if(direction == 'left'){
        if(firstSeris == '0000000'){
            layer.alert('前面已经没有时间序列了!');
            return;
        }
    }
    if(direction == 'right'){
        if(parseInt(currentSeris) >= parseInt(lastSeris)){
            layer.alert('后面已经没有时间序列了!');
            currentSeris = lastSeris;
            return;
        }
    }
    cellId = $("#cellId").val();
    wellId = $("#wellId").val();
    $.ajax({
		type : "get",
        url : "/api/v1/dish/scroll?procedure_id=" + procedureId + "&dish_id=" + dishId + 
                "&well_id=" + wellId + "&current_seris=" + currentSeris + "&direction=" + direction,
		datatype : "json",
		success : function(data) {
            var series = data.series;
            var serisContent = "";
            var milestoneList = data.milestone_list;
            for(var i=0;i<=series.length-1;i++){
                var milestoneType = "<span></span>";
                for(var j=0;j<milestoneList.length;j++){
                    if(milestoneList[j].seris == series[i].series_code){
                        milestoneType = "<span>" + milestoneList[j].milestoneType + "</span>";
                    }
                }

                var imageUrl = series[i].series_image_path;
                if(imageUrl.indexOf('embryo_not_found.jpg') != -1){
                    imageUrl = "/static/front/img/loc-emb.png";
                }
                serisContent = serisContent + "<div class=\"swiper-slide\" id='" + series[i].series_code + "_div'><img src=\"" + 
                    imageUrl + "\" id='" + series[i].series_code + "' onclick=\"getBigImage('" + 
                    procedureId + "','" + dishId + "','" + wellId + "','" + series[i].series_code + "','0', '" + 
                    cellId + "','" + series[i].series_name + "')\">" + milestoneType + "<b>" + 
                    series[i].series_name + "</b></div>";
            }
            $("#myscrollboxul").html(serisContent);
            embryoId = milestoneList[0].embryoId;
            $("#embryoId").val(embryoId);

            firstSeris = series[0].series_code;
            currentSeris = data.current_series;
            lastSeris = data.last_series;
            //loadingImage(procedureId,dishId,wellId,currentSeris,'');
            //loadingZIndex(procedureId,dishId,wellId,currentSeris);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//刘勇智
//初始化radio通用方法
function chushihua(dictClass) {
	$.ajax({
		type : "get",
		url : "/api/v1/dict/lists/"+dictClass,
		datatype : "json",
		success : function(data) {
			if (data.code == 0) {
				for (var i = 0; i < data.data.length; i++) {
					var obj = data.data[i];
					var radioId = obj.dictClass+"Id";
					var divId = radioId+"Div";
					var str="";
					if(obj.dictClass=="embryo_fate_type") {//如果为标记的，需要特殊处理
						str = "<li class='"+obj.dictSpare+"' data-end='"+obj.dictKey+"'><i></i><span>"+obj.dictValue+"</span></li>";
					}else {
						str="<input type='radio' name='"+radioId+"' lay-filter="+radioId+" value='" + obj.dictKey + "' title='"+obj.dictValue+"' />";
					}
					$("#"+divId).append(str);
				}
				form.render();
			} else {
				layer.alert(data.msg);
			}
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//初始化以及页面回显   采集目录 、时间序列、 图片路径、图片名称, 周期ID, 皿ID
function ini(acquisitionTime,timeSeries,path,imageName) {
	 
    //由于使用的layUI的表单提交，需要把值复制到表单中
	$("#milestoneStage").val(acquisitionTime);
	var mipath = path.substring(path.indexOf("captures")+9,path.length);
	$("#milestonePath").val(mipath+timeSeries+"\\"+imageName);
	
	$("#timeSeries").val(timeSeries);
	//根据胚胎ID查询该胚胎ID是否有里程碑，如果有则进行回显
	$.ajax({
		type : "get",
		url : "/api/v1/milestone/"+$("#embryoId").val(),
		datatype : "json",
		data:{"timeSeries":timeSeries,"procedureId":procedureId,"dishId":dishId,"wellId":wellId},
		cache:false,
		success : function(data) {
				if(data!=null) {//如果当前里程碑不为空则回显
					var milestone = data.milestone;
                    var milestoneData = data.milestoneData;
                    $("#milestoneScoreSpanId").html(milestoneData.milestoneScore);
                    if(milestone!=null) {
						$("#milestoneCheckbox").prop('checked', true);
		                $('#milestone').animate({
		                    height: '126px'
		                });
	                	$("input:radio[name=milestoneId][value="+milestone.milestoneId+"]").prop("checked",true);
	                	$("#milestoneFormSubDiv").show();
	                }
	                if(milestoneData.pnId!="") {
	                	$("input:radio[name=pnId][value="+milestoneData.pnId+"]").prop("checked",true);
	                }
	                $("input:radio[name=count][value="+milestoneData.cellCount+"]").prop("checked",true);
	                $("input:radio[name=evenId][value="+milestoneData.evenId+"]").prop("checked",true);
	                $("input:radio[name=fragmentId][value="+milestoneData.fragmentId+"]").prop("checked",true);
	                $("input:radio[name=gradeId][value="+milestoneData.gradeId+"]").prop("checked",true);
                    $("#innerDiameter").val(Math.round(milestoneData.innerDiameter));
                    $("#innerArea").val(Math.round(milestoneData.innerArea));
                    $("#outDiameter").val(Math.round(milestoneData.outerDiameter));
                    $("#outerArea").val(Math.round(milestoneData.outerArea));
                    $("#expansionArea").val(Math.round(milestoneData.expansionArea));
	                $("#zonaThickness").val(Math.round(milestoneData.zonaThickness));
	                $("#memo").val(milestoneData.memo);
	                if(milestone!=null) {
		                $("#stageId").html("("+milestone.milestoneName+")");
						showHide(milestone.milestoneId);
	                }else {
	                	showHide(null);
	                }
				}else {
					showHide(null);
				}
				form.render();
				
	        	//当前时间序列的缩略图
				var thpath = $("#"+currentSeris).attr("src").replace(/\\/g,"/");
	        	thpath = thpath.substring(thpath.indexOf("/",8),thpath.length);
	        	$("#thumbnailPath").val(thpath);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
    });
    
	
	//回显胚胎结局
	//根据胚胎ID查询该胚胎ID是否有里程碑，如果有则进行回显
	$.ajax({
		type : "get",
		url : "/api/v1/embryo/"+$("#embryoId").val(),
		datatype : "json",
		cache:false,
		success : function(data) {
			if (data.code == 0) {
				 $("#embryoScoreSpanId").html(data.data.embryoScore)
	            if (data.data.embryoFateId != 0) {
	            	embryoFateIdQj=data.data.embryoFateId;
	                $(".mark i").attr('data-mark', data.data.embryoFateId);
	                $(".mark i").attr('class', data.data.dictSpare);
	            } else {
	                $(".mark i").attr('data-mark', "");
	                $(".mark i").attr('class', "");
	            }
			} else {
				layer.alert(data.msg);
			}
			layer.close(jaindex);
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
		
	
}

function showHide(value) {
	//根据不同的value显示不同的胚胎形态
	if(value!=null) {
		$("#embryoDiv").show();
		$("#embryoSjDiv").show();
		$("#stageDiv").show();
		$("#milestoneFormSubDiv").show();
	}
	
	if(value==null) {
		$("#milestoneFormSubDiv").hide();
		$("#countDiv").hide();
		$("#evenDiv").hide();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		$("#pnDiv").hide();
		$("#embryoDiv").hide();
		$("#embryoSjDiv").hide();
		$("#stageDiv").hide();
		$("#milestoneCheckbox").prop('checked', false);
        $('#milestone').animate({
            height: '31px'
        });
        $("input:radio[name=milestoneId]").prop("checked",false);
        $("input:radio[name=pnId]").prop("checked",false);
        $("input:radio[name=count]").prop("checked",true);
        $("input:radio[name=evenId]").prop("checked",true);
        $("input:radio[name=fragmentId]").prop("checked",true);
        $("input:radio[name=gradeId]").prop("checked",true);
        $("#diameter").val("");
        $("#area").val("");
        $("#thickness").val("");
        $("#memo").val("");
        $("#stageId").html("()");
	}else if(value=="1") {//PN
		$("#countDiv").hide();
		$("#evenDiv").hide();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		$("#pnDiv").show();
		$("input:radio[name=pnId][value=2]").prop("checked",true);
	}else if(value=="2") {//2C
		$("#countDiv").show();
		$("#evenDiv").show();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		$("#pnDiv").hide();
		$("input:radio[name=count][value="+value+"]").prop("checked",true);
	}else if(value=="3" || value=="4" || value=="5" || value=="6") {
		$("#countDiv").show();
		$("#evenDiv").show();
		$("#fragmentDiv").show();
		if(value=="6") {
			value=parseInt(value)+2;
			$("#gradeDiv").show();
		}else {
			$("#gradeDiv").hide();
		}
		$("#pnDiv").hide();
		$("input:radio[name=count][value="+value+"]").prop("checked",true);
	}else {
		$("#pnDiv").hide();
		$("#countDiv").hide();
		$("#evenDiv").hide();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
//		layer.alert("待确认");
	}
	form.render();
}

//根据周期id、皿ID、孔ID、获取孔的时间序列对应最清晰的URL
function queryClearImageUrl() {
	//首先清空一次播放环境
	$("#imgVideoDiv").html("");
	$.ajax({
		type : "get",
		url : "/api/v1/image/pay/queryClearImageUrl",
		datatype : "json",
		cache:false,
		data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId},
		success : function(data) {
			 if(data!=null) {
				 clearImageUrlList = data;
		    	 for(var i=0;i<clearImageUrlList.length;i++) {
					 var image = "<img style='display:none' index="+(i)+"  id='imageVideo"+clearImageUrlList[i].timeSeries+"' src='"+clearImageUrlList[i].clearImageUrl+"' />";
					 $("#imgVideoDiv").append(image);
				 }
			 }
		},
		error : function(request) {
			layer.alert(request.responseText);
		}
	});
}

//上下里程碑   根据胚胎ID 和 当前时间序列 获取上下里程碑节点ID
function node(upOrdown) {
	if(!$('#playBtn').hasClass('play')){
		layer.msg("请先暂停播放后，再操作!")
		return;
	}
	
	$.ajax({
		type : "get",
		url : "/api/v1/milestone/node/"+$("#embryoId").val()+"/"+currentSeris+"/"+upOrdown,
		datatype : "json",
		cache:false,
		success : function(data) {
			 if(data!=null) {
				 querySeriesList(wellId, data.milestoneTime, 2, cellId);
//				 getBigImage(procedureId, dishId, wellId, data.milestoneTime,0, cellId,currentSerisName);
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
//跳转到皿视图
function toDishView() {
	window.location.href="/front/dish/?procedureId="+$("#procedureId").val()+"&dishId="+$("#dishId").val()+"&dishCode="+$("#dishCode").val();
}