var form = null;
//最清晰的jpg
var sharpJpg = null;
//最清晰的jpg对应的z轴位置
var sharpZIndex = null;
//z轴总数
var zIndexLength = 0;
//采集时间
var acquisitionTime = null;
//目录
var path = null;
var procedureId = "";
var dishId = "";
var wellId = "";
var lastSeris = "";
var jaindex = "";
var currentSeris = "";
var seris = "";
var drwaType = "";
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
        $.ajax({
            cache : false,
            type : "GET",
            url : "/api/v1/well/list/" + procedureId + "/" + dishId,
            data : "",
            error : function(request) {
                parent.layer.alert(request.responseText);
            },
            success : function(data) {
                var well = "";
                for(var i=1;i<=12;i++){
                    var result = check(i, data);
                    if(result != ''){
                        if(i == data[0]){
                            well = well + "<li class=\"active\"><span>well" + i + 
                            "</span><img src=\"/api/v1/well/image?image_path=" + result +
                            "\" onclick=\"querySeriesList('" + i + "','lastEmbryoSerie')\"><i></i></li>";
                        }else{
                            well = well + "<li><span>well" + i + 
                            "</span><img src=\"/api/v1/well/image?image_path=" + result +
                            "\" onclick=\"querySeriesList('" + i + "','lastEmbryoSerie')\"><i></i></li>";
                        }
                    }else{
                        well = well + "<li><span>well" + i + 
                        "</span><img src=\"/static/front/img/icon-wellnone.jpg\"><i></i></li>";
                    }
                }
                $("#siteitem").html(well);
                wellId = data[0];
                querySeriesList(wellId,'lastEmbryoSerie');//获取每个孔下面的时间序列
            }
        });

        // 上部图片滚动设置
		var mySwiper = new Swiper('#topNav', {
            freeMode: true,
            freeModeMomentumRatio: 0.5,
            slidesPerView: 'auto',
			prevButton:'.swiper-button-prev',
			nextButton:'.swiper-button-next',
        });
        
        swiperWidth = mySwiper.container[0].clientWidth
        maxTranslate = mySwiper.maxTranslate();
        maxWidth = -maxTranslate + swiperWidth / 2
        
        $(".swiper-container").on('touchstart', function(e) {
            e.preventDefault()
        })
        
        mySwiper.on('tap', function(swiper, e) {
        
            e.preventDefault()
        
            slide = swiper.slides[swiper.clickedIndex]
            slideLeft = slide.offsetLeft
            slideWidth = slide.clientWidth
            slideCenter = slideLeft + slideWidth / 2
            // 被点击slide的中心点
        
            mySwiper.setWrapperTransition(300)
        
            if (slideCenter < swiperWidth / 2) {
                
                mySwiper.setWrapperTranslate(0)
        
            } else if (slideCenter > maxWidth) {
                
                mySwiper.setWrapperTranslate(maxTranslate)
        
            } else {
        
                nowTlanslate = slideCenter - swiperWidth / 2
        
                mySwiper.setWrapperTranslate(-nowTlanslate)
        
            }
        
            $("#topNav  .active").removeClass('active')
        
            $("#topNav .swiper-slide").eq(swiper.clickedIndex).addClass('active')
        
        })



        function site() {
            var site = document.getElementById('site');
            var siteItem = document.getElementById('siteitem');
            siteItem.style.width = (site.offsetWidth - 44) + "px";
        }
        site();

        // 点击切换样式
        $('#myscrollboxul li').click(function () {
            $('#myscrollboxul li').removeClass('active');
            $(this).addClass('active');
        });

        $('#siteitem li').click(function () {
            $('#siteitem li').removeClass('active');
            $(this).addClass('active');
        });
		// // z轴点击样式
		// $('.time-vertical li').click(function () {
		// 	$('.time-vertical li').removeClass('active');
		// 	$(this).addClass('active');
		// });
		

        // 选为最清晰的值提示
        form.on('checkbox(clear)', function (data) {
            const a = data.elem.checked;
            if (a == true) {
                layer.msg('已标注为最清晰的图片');
            } else {
                layer.msg('已取消标注');
            }

        });
        // 选中里程碑出现的内容
        form.on('checkbox(milestone)', function (data) {
            const a = data.elem.checked;

            if (a == true) {
                // layer.msg('打开');
                $('#milestone').animate({
                    height: '120px'
                });
            } else {
                // layer.msg('关闭');
                $('#milestone').animate({
                    height: '31px'
                });

            }

        });

        // 播放暂停按钮的切换

        //上一张 下一张

        var n = 0;
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
        var textTime;
        var imgTime;
        // 点击播放暂停
        $('#playBtn').click(function () {
            if ($(this).hasClass('play')) {
                $(this).removeClass('play');
                $(this).addClass('stop');
                console.log("播放");

                function showText() {
                    n = n + 1;
                }
                textTime = setInterval(showText, 200);

                function run() {
                    if (n < $(".lg-img img").length) {
                        n = n;
                    } else {
                        n = 0
                    }
                    $(".lg-img img").hide();
                    $(".lg-img img:eq(" + n + ")").show();
                }
                imgTime = setInterval(run, 200);

            } else {
                $(this).removeClass('stop');
                $(this).addClass('play');
                console.log("暂停");
                clearInterval(textTime);
                clearInterval(imgTime);
            }
        })
        
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
		
		function canvasWidth(){
			var embr = document.getElementById('embryo');
			var canvasBox = document.getElementById('canvasBox');
			canvasBox.style.width = embr.offsetWidth;
			canvas.width = canvasBox.offsetWidth;
			canvas.height = canvasBox.offsetHeight;
		}
		canvasWidth();
		
		/* 为canvas绑定mouse事件 */
		
		
		$(".tool-metrical li").click(function(){
            var self= $(this)
            var x1 = 0;
            var y1 = 0;
			   $('canvas').mousedown(function(e){
				   flag = true;
				   x1,x = e.offsetX; // 鼠标落下时的X
				   y1,y = e.offsetY; // 鼠标落下时的Y
				   console.log(x,y)
			   }).mouseup(function(e){
				    flag = false;
				    url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
				    x = e.offsetX; // 鼠标落下时的X
                    y = e.offsetY; // 鼠标落下时的Y
                    console.log(x,y)
                    if(drwaType == 'straight'){
                       alert(1);
                    }else{
                        alert(2);
                        var rx = (e.offsetX-x1);
                        var ry = (e.offsetY-y1);
                        var r = Math.round(Math.sqrt(rx*rx+ry*ry));
                        $('#diameter').text('直径:' + r + "um");
                        var area = Math.round(Math.PI * r/2 * r/2);
                        $('#area').text('面积:' + area + "um²");
                    }
			   }).mousemove(function(e){
				    if(self.hasClass('straight')){
                        drwaType = 'straight';
					    drawLine(e); // 绘制方法
				    }else{
                        drwaType = 'circle';
					    drawCircle(e); // 绘制方法	
				    }
               });
               
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
                alert(1);
                var img = new Image();
                img.src = url;
                ctx.drawImage(img,0,0,canvas.width,canvas.height);
            }
		
		// 跟随屏幕改变的设定	
		$(window).resize(function () {
			scroll();
			site();
			canvasWidth();
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
			

			
			var diameter = $("#diameter").val();
			if(diameter=="") {
				layer.alert("直径不能为空,请输入直径!");
				return false;
			}
			
			var area = $("#area").val();
			if(area=="") {
				layer.alert("面积不能为空,请选择评级!");
				  return false;
			}
			
			var thickness = $("#thickness").val();
			if(thickness=="") {
				layer.alert("透明带厚度不能为空,请选择评级!");
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
					layer.alert("设置成功!");
				}
			});

            return false;
        });

    });
})

function loadingZIndex(procedureId,dishId,wellId,timeSeries){

    //加载z轴所以节点，并渲染
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/image/findAllZIndex",
        data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId,"timeSeries":timeSeries},
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
            var zLi = "";
            if(data.code == 200 && data.data != null){
                var i = data.data.fileStart;
                var length = data.data.fileEnd;
                acquisitionTime = data.data.imagePath;
                path = data.data.path;
                sharpJpg = data.data.sharp;
                zData = data.data.zIndexFiles;
                zIndexLength = zData.length;
                for (;i < length; i++) {
                    if(sharpJpg == zData[i]) {
                        sharpZIndex = i;
                        zLi = "<li class='active' onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zIndex=" + i + " zJpg='" + zData[i] + "'><b></b></li>" + zLi;
                    } else {
                        zLi = "<li onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zIndex=" + i + " zJpg='" + zData[i] + "'><b></b></li>" + zLi;
                    }
                }
                $("#zIndex").html(zLi);
                var imageName = $(".time-vertical .active").attr("zJpg");
                ini(acquisitionTime,timeSeries,path,imageName)
            }
        }
    });
    
    $('#zIndexDiv').bind('mousewheel', function(event, delta) {
        var zIndex = $(".time-vertical .active").attr('zIndex');
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
        var imageName = $(".time-vertical li[zIndex="+zIndex+"]").attr("zJpg");
        ini(acquisitionTime,timeSeries,path,imageName)
        return false;    
    });
    
}

function checkZIndex(procedureId,dishId,wellId,timeSeries,zIndex){
    $('.time-vertical li').removeClass('active');
    $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
    loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
    var imageName = $(".time-vertical li[zIndex="+zIndex+"]").attr("zJpg");
    ini(acquisitionTime,timeSeries,path,imageName)
}

function loadingImage(procedureId,dishId,wellId,timeSeries,zIndex){
    if(zIndex == null || zIndex == '' || sharpZIndex == zIndex){
        $("#distinct").prop("checked",true);
    } else {
        $("#distinct").prop("checked",false);
    }
    var imgUrl = "/api/v1/image/findImage?procedureId="+ procedureId +"&dishId="+ dishId +"&wellId="+ wellId +"&timeSeries="+ timeSeries +"&zIndex=" + zIndex; 
    var img = "<img src=" + imgUrl + ">";
    $("#imgDiv").html(img);
}

//羊城
function check(index, data){
    var result = '';
    for(var i=0;i<data.length;i=i+2){
        if(index == data[i]){
            result = data[i+1];
        }
    }
    return result;
}

function querySeriesList(wellId, seris){
    var procedureId = $("#procedureId").val();
    var dishId = $("#dishId").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/list?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" + wellId + "&seris=" + seris,
        data : "",
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var seris = "";
            for(var i=0;i<data.length;i=i+4){
                var imagePath = "/api/v1/well/image?image_path=" + data[i+1];
                if(data[i+1].indexOf("embryo_not_found") != -1){
                    imagePath = "/static/front/img/icon-noembryo.jpg";
                }
                var active = "<div class=\"swiper-slide\">";
                if(i == 16){
                    active = "<div class=\"swiper-slide active\">";
                }
                seris = seris + active + "<span><img src=\"" + 
                                    imagePath +"\" onclick=\"getBigImage('" 
                                    + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\"><b>" + 
                                    data[i+2] + "</b></div>";
            }
            $("#myscrollboxul").html(seris);
            currentSeris = data[data.length-1];
            loadingImage(procedureId,dishId,wellId,currentSeris,'');
            loadingZIndex(procedureId,dishId,wellId,currentSeris);
        }
    });
}

function getBigImage(procedureId, dishId, wellId, seris){
    querySeriesList(wellId, seris);
    loadingImage(procedureId,dishId,wellId,seris,'');
    loadingZIndex(procedureId,dishId,wellId,seris);
}

function preFrame(){
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
            getBigImage(procedureId, dishId, wellId, data);
        }
    });
}

function nextFrame(){
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
                getBigImage(procedureId, dishId, wellId, data);
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
});



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
	$("#milestonePath").val(path+imageName);
	$("#timeSeries").val(timeSeries);
	//根据胚胎ID查询该胚胎ID是否有里程碑，如果有则进行回显
	$.ajax({
		type : "get",
		url : "/api/v1/milestone/"+$("#embryoId").val(),
		datatype : "json",
		data:{"milestonePath":path+imageName, "timeSeries":timeSeries, "wellId":wellId, "procedureId":procedureId, "dishId":dishId},
		cache:false,
		success : function(data) {
				if(data!=null) {//如果当前里程碑不为空则回显
					var milestone = data.milestone;
					var milestoneData = data.milestoneData;
					$("#milestoneCheckbox").attr('checked', true);
	                $('#milestone').animate({
	                    height: '120px'
	                });
	                $("input:radio[name=milestoneId][value="+milestone.milestoneId+"]").attr("checked",true);
	                if(milestoneData.pnId!="") {
	                	$("input:radio[name=pnId][value="+milestoneData.pnId+"]").attr("checked",true);
	                }
	                $("input:radio[name=count][value="+milestoneData.cellCount+"]").attr("checked",true);
	                $("input:radio[name=evenId][value="+milestoneData.evenId+"]").attr("checked",true);
	                $("input:radio[name=fragmentId][value="+milestoneData.fragmentId+"]").attr("checked",true);
	                $("input:radio[name=gradeId][value="+milestoneData.gradeId+"]").attr("checked",true);
                    $("#innerDiameter").val(Math.round(milestoneData.innerDiameter));
                    $("#innerArea").val(Math.round(milestoneData.innerArea));
                    $("#outDiameter").val(Math.round(milestoneData.outerDiameter));
                    $("#outArea").val(Math.round(milestoneData.outerArea));
                    $("#expansionArea").val(Math.round(milestoneData.expansionArea));
	                $("#zonaThickness").val(Math.round(milestoneData.zonaThickness));
	                $("#memo").val(milestoneData.memo);
	                $("#stageId").html("("+milestone.milestoneName+")");
	                showHide(milestone.milestoneId);
				}else {
					showHide(null);
				}
				form.render();
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
		
	}
	
	if(value==null) {
		$("#countDiv").hide();
		$("#evenDiv").hide();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		$("#pnDiv").hide();
		$("#embryoDiv").hide();
		$("#embryoSjDiv").hide();
		$("#stageDiv").hide();
		$("#milestoneCheckbox").attr('checked', false);
        $('#milestone').animate({
            height: '31px'
        });
        $("input:radio[name=milestoneId]").attr("checked",false);
        $("input:radio[name=pnId]").attr("checked",false);
        $("input:radio[name=count]").attr("checked",true);
        $("input:radio[name=evenId]").attr("checked",true);
        $("input:radio[name=fragmentId]").attr("checked",true);
        $("input:radio[name=gradeId]").attr("checked",true);
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
	}else if(value=="2") {//2C
		$("#countDiv").show();
		$("#evenDiv").show();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		$("#pnDiv").hide();
	}else if(value=="3" || value=="4" || value=="5" || value=="6") {
		$("#countDiv").show();
		$("#evenDiv").show();
		$("#fragmentDiv").show();
		if(value=="6") {
			$("#gradeDiv").show();
		}else {
			$("#gradeDiv").hide();
		}
		$("#pnDiv").hide();
	}else {
		$("#pnDiv").hide();
		$("#countDiv").hide();
		$("#evenDiv").hide();
		$("#fragmentDiv").hide();
		$("#gradeDiv").hide();
		layer.alert("待确认");
	}
}