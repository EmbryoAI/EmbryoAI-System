layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {

        // 上部图片滚动设置

        function scroll() {
            var scrollpic = document.getElementById('scrollpic');
            var myscroll = document.getElementById('myscroll');
            myscroll.style.width = (scrollpic.offsetWidth - 84) + "px";
            var blw = $("#myscrollbox li").width();
            var liArr = $("#myscrollbox ul").children("li");
            var mysw = $("#myscroll").width();
            var mus = parseInt(mysw / blw); //计算出需要显示的子元素的数量
            var length = liArr.length - mus; //计算子元素可移动次数（被隐藏的子元素数量）

            var i = 0;
            $("#right").click(function () {
                i++
                if (length < 0) {
                    return false
                }

                if (i < length) {

                    $("#myscrollbox").css("left", -(blw * i));

                } else {
                    i = length;
                    $("#myscrollbox").css("left", -(blw * length));
                }

            });
            $("#left").click(function () {
                i--
                if (i >= 0) {
                    $("#myscrollbox").css("left", -(blw * i));
                } else {
                    i = 0;
                    $("#myscrollbox").css("left", 0);
                }
                0
            });
        };
        scroll();

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
		// z轴点击样式
		$('.time-vertical li').click(function () {
			$('.time-vertical li').removeClass('active');
			$(this).addClass('active');
		});
		

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
                layer.msg("已经是第一张了")
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
                layer.msg("已经是最后一张了")
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
        // 标记结局
        $(".tool-end").on('click', 'li[data-end]', function () {
            var indexData = $(this).attr('data-end');
            var indexName = $(this).attr('class');
            var markData = $(".mark i").attr('data-mark');
            var markName = $(".mark i").attr('class');
            if (markData === "" || markName === "") {
                $(".mark i").attr('data-mark', indexData);
                $(".mark i").attr('class', indexName);
                layer.msg("标注成功")
            } else {
                $(".mark i").attr('data-mark', "");
                $(".mark i").attr('class', "");
                layer.msg("已取消标注")
            }
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
			   $('canvas').mousedown(function(e){
				   flag = true;
				   x = e.offsetX; // 鼠标落下时的X
				   y = e.offsetY; // 鼠标落下时的Y
				   console.log(x,y)
			   }).mouseup(function(e){
				   flag = false;
				   url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
				   x = e.offsetX; // 鼠标落下时的X
				   y = e.offsetY; // 鼠标落下时的Y
				   console.log(x,y)
			   }).mousemove(function(e){
				   
				   if(self.hasClass('straight')){
					   drawLine(e); // 绘制方法
				   }else{
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
	   
	   $(".tool").click(function(){
		   
		   clearCanvas()
		   
	   })
		
		// 跟随屏幕改变的设定	
		$(window).resize(function () {
			scroll();
			site();
			canvasWidth();
		});
		
		
        //初始化radio通用方法
		function chushihua(dictClass,radioId,divId) {
			$.ajax({
				type : "get",
				url : "/api/v1/dict/list/"+dictClass,
				datatype : "json",
				success : function(data) {
					if (data.code == 0) {
						var str = "";
						for (var i = 0; i < data.data.length; i++) {
						 
								str+="<input type='radio' name='"+radioId+"' lay-filter="+radioId+" value='" + data.data[i].dictKey + "' title='"+data.data[i].dictValue+"' />";
						 
						}
						$("#"+divId).html(str);
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
        
        //动态初始化里程碑的值,字典表milestone
        chushihua("milestone","milestoneId","milestoneIdDiv");
                
        //初始化PN数，字典值pn
        chushihua("pn","pnId","pnIdDiv");
		
		//初始化均匀度,字典even
		chushihua("even","evenId","evenIdDiv");
		
		//初始化碎片率，字典fragment
		chushihua("fragment","fragmentId","fragmentIdDiv");
		
		//初始化评分,字典grade
		chushihua("grade","gradeId","gradeIdDiv");
		
		
		//根据胚胎ID查询该胚胎ID是否有里程碑，如果有则进行回显
		$.ajax({
			type : "get",
			url : "/api/v1/milestone/"+$("#embryoId").val(),
			datatype : "json",
			success : function(data) {
				if (data.code == 0) {
					if(data.data!=null) {//如果当前里程碑不为空则回显
						var milestone = data.data.milestone;
						var milestoneData = data.data.milestoneData;
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
		                $("#diameter").val(milestoneData.diameter);
		                $("#area").val(milestoneData.area);
		                $("#thickness").val(milestoneData.thickness);
		                $("#memo").val(milestoneData.memo);
		                $("#stageId").html("("+milestone.milestoneName+")");
		                showHide(milestone.milestoneId);
					}else {//为空则全部隐藏
						  showHide(null);
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

	
		
		form.on('radio(milestoneId)', function(data){
			var title = data.elem.title;
			var value = data.value;
			$("#stageId").html("("+title+")");
			showHide(value);
		});
		
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
				async : false,
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
