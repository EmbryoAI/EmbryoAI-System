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
                layer.msg('打开');
                $('#milestone').animate({
                    height: '153px'
                });
            } else {
                layer.msg('关闭');
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
			$('.tool-metrical li').removeClass('active');
			$(this).addClass('active');
			if($(this).hasClass('straight')){
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
					drawLine(e); // 绘制方法
				});
			}else{
				
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
					drawCircle(e); // 绘制方法
				});
				
			}
			
			
			
			
		})
		
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
			drawLine(e); // 绘制方法
		});
		
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
		
		
    });
})
