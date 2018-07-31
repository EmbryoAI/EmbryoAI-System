layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {

        // 播放暂停按钮的切换

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
		
    });
})
