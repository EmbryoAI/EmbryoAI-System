layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {

        // 上部图片滚动设置
//         var scrollpic = document.getElementById('scrollpic');
//             var myscroll = document.getElementById('myscroll');
//             myscroll.style.width = (scrollpic.offsetWidth - 84) + "px";
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


        
        // function scroll() {
        //     var scrollpic = document.getElementById('scrollpic');
        //     var myscroll = document.getElementById('myscroll');
        //     myscroll.style.width = (scrollpic.offsetWidth - 84) + "px";
        //     var blw = $("#myscrollbox li").width();
        //     var liArr = $("#myscrollbox ul").children("li");
        //     var mysw = $("#myscroll").width();
        //     var mus = parseInt(mysw / blw); //计算出需要显示的子元素的数量
        //     var length = liArr.length - mus; //计算子元素可移动次数（被隐藏的子元素数量）

        //     var i = 0;
        //     $("#right").click(function () {
        //         i++
        //         if (length < 0) {
        //             return false
        //         }

        //         if (i < length) {

        //             $("#myscrollbox").css("left", -(blw * i));

        //         } else {
        //             i = length;
        //             $("#myscrollbox").css("left", -(blw * length));
        //         }

        //     });
        //     $("#left").click(function () {
        //         i--
        //         if (i >= 0) {
        //             $("#myscrollbox").css("left", -(blw * i));
        //         } else {
        //             i = 0;
        //             $("#myscrollbox").css("left", 0);
        //         }
        //         0
        //     });
        // };
        // scroll();

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
                    height: '120px'
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
		var drwaType ='';
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
            var datali = $(this).attr('data-li');
			$(".tool-metrical li").removeClass("active");
            self.addClass("active"); 
            console.log(datali)
            if ( datali == 1) {
                $('canvas').unbind();
                $('canvas').mousedown(function(e){
                    flag = true;
                    x1,x = e.offsetX; // 鼠标落下时的X
                    y1,y = e.offsetY; // 鼠标落下时的Y
                }).mouseup(function(e){
                    flag = false;
                    url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
                    x = e.offsetX; // 鼠标起时的X
                    y = e.offsetY; // 鼠标起下时的Y
                        var length = Math.round(Math.sqrt(Math.abs((x1 - x)* (x1 - x)+(y1 - y)* (y1 - y))));
                        $('#length').text(length);
    
                        layer.open({
                        type: 1,
                        area: ['300px', '280px'],
                        shadeClose: true, 
                        content: $("#dbox-l"),
                        btn:["确认导入","取消"],
                        yes: function(index, layero){
                            layer.closeAll();
                            layer.msg("导入成功！")
                            clearCanvas()
                        }
                        ,btn2: function(index, layero){
                            clearCanvas()
                        },
                        btnAlign: 'c'
                    });
                }).mousemove(function(e){
                        drawLine(e); // 直线绘制方法
                });
            }
            if ( datali == 2) {
                $('canvas').unbind();
                $('canvas').mousedown(function(e){
                    flag = true;
                    x1,x = e.offsetX; // 鼠标落下时的X
                    y1,y = e.offsetY; // 鼠标落下时的Y
                }).mouseup(function(e){
                    flag = false;
                    url = $('canvas')[0].toDataURL(); // 每次 mouseup 都保存一次画布状态
                    x = e.offsetX; // 鼠标起时的X
                    y = e.offsetY; // 鼠标起下时的Y
                    var rx = (e.offsetX-x1);
                    var ry = (e.offsetY-y1);
                    var r = Math.round(Math.sqrt(rx*rx+ry*ry));
                    $('#diameter').text(r);
                    var area = Math.round(Math.PI * r/2 * r/2);
                    $('#area').text(area);
                    layer.open({
                        type: 1,
                        area: ['300px', '280px'],
                        shadeClose: true, 
                        content: $("#dbox-c"),
                        btn:["确认导入","取消"],
                        yes: function(index, layero){
                            layer.closeAll();
                            layer.msg("导入成功！")
                            clearCanvas()
                        }
                        ,btn2: function(index, layero){
                            clearCanvas()
                        },
                        btnAlign: 'c'
                    });
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
