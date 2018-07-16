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
        $(window).resize(function () {
            scroll();
            site();
        });

        // 点击切换样式
        $('#myscrollboxul li').click(function () {
            $('#myscrollboxul li').removeClass('active');
            $(this).addClass('active');
        });

        $('#siteitem li').click(function () {
            $('#siteitem li').removeClass('active');
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
        function showText() {
            n = n + 1;
        }
        setInterval(showText, 200);		
		
		function run() {
			if (n < $(".lg-img img").length) {
				n = n;
			} else {
				n = 0
			}
			$(".lg-img img").hide();
			$(".lg-img img:eq(" + n + ")").show();
		}
		var timer = setInterval(run, 200);
		
		
                $('#playBtn').click(function () {
                    if ($(this).hasClass('play')) {
                        $(this).removeClass('play');
                        $(this).addClass('stop');
						console.log("播放");
						timer
						
						
                    } else {
                        $(this).removeClass('stop');
                        $(this).addClass('play');
						console.log("暂停");
						clearInterval(timer);
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
    });
})
