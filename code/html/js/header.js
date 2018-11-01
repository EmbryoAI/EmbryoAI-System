layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    var element = layui.element;

		function IsPC() {
        var userAgentInfo = navigator.userAgent;
        var Agents = ["Android", "iPhone",
                    "SymbianOS", "Windows Phone",
                    "iPad", "iPod"];
        var flag = true;
        for (var v = 0; v < Agents.length; v++) {
            if (userAgentInfo.indexOf(Agents[v]) > 0) {
                flag = false;
                break;
            }
        }
        return flag;
    };
    $(document).ready(function(){
        var isPC=IsPC();
        if(isPC){
           //这里执行的是PC端的代码；
		   console.log("11pc")
      }
        else{
           //这里执行的是移动端的代码；
		   alert("m22")
        }
    });

    // 弹窗系统设置
    $('#settings').on('click', function () {
        layer.open({
            title: "系统设置",
            type: 2,
            area: ['350px', '250px'],
            shadeClose: true,
            content: 'setting.html',
        });
    });
    // 弹窗密码修改
    $('#passwd').on('click', function () {
        layer.open({
            title: "密码修改",
            type: 2,
            area: ['500px', '300px'],
            shadeClose: true,
            content: 'changePasswd.html',
        });
    });

    //密码修改验证		
    $(".layui-btn").on("click", function (event) {
        event.preventDefault();
        $(".layui-word-aux").addClass("show");
        $(".layui-word-aux").html(" ");

        $("#oldpasswd,#newpasswd1,#newpasswd2").blur();
        var oldpasswd = $('#oldpasswd').val().toString();
        var newpasswd1 = $('#newpasswd1').val().toString();
        var newpasswd2 = $('#newpasswd2').val().toString();
		
		
        if (oldpasswd == "" || newpasswd1 == "" || newpasswd2 == "") {
            $(".layui-word-aux").html("密码不能为空！");
        } else if (newpasswd1 != newpasswd2) {
            $(".layui-word-aux").html("新密码不一致！");
        } else {

        }

    });

    $("#oldpasswd,#newpasswd1,#newpasswd2").focus(function () {
        $(".layui-word-aux").html(" ");
    });


	function nolist(){
		var marginT = $(".layui-col-md4 h6").height()+8;
		var listH = $(".img-list").height();
		console.log(marginT,listH);
		$(".no-list").css("margin-top",marginT+'px');
		$(".no-list").css("height",listH-marginT);
		$(".no-list").css("line-height",listH-marginT+'px');
	}
	nolist();
	$(window).resize(function () {
		nolist();
	});
})
