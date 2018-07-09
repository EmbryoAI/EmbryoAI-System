layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    var element = layui.element;



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

    // //密码修改验证		
    // $(".layui-btn").on("click", function (event) {
    //     event.preventDefault();
    //     $(".layui-word-aux").addClass("show");
    //     $(".layui-word-aux").html(" ");

    //     $("#oldpasswd,#newpasswd1,#newpasswd2").blur();
    //     var oldpasswd = $('#oldpasswd').val().toString();
    //     var newpasswd1 = $('#newpasswd1').val().toString();
    //     var newpasswd2 = $('#newpasswd2').val().toString();
		
		
    //     if (oldpasswd == "" || newpasswd1 == "" || newpasswd2 == "") {
    //         $(".layui-word-aux").html("密码不能为空！");
    //     } else if (newpasswd1 != newpasswd2) {
    //         $(".layui-word-aux").html("新密码不一致！");
    //     } else {

    //     }

    // });

    // $("#oldpasswd,#newpasswd1,#newpasswd2").focus(function () {
    //     $(".layui-word-aux").html(" ");
    // });

    $('#caseSearch').on('click', function () {
        var caseIdOrName = $("#caseIdOrName").val();
        // $("#userName").val(caseIdOrName);
        //执行重载
        table.reload('case-table', {
            page: {
            curr: 1  //重新从第 1 页开始
            }
            ,where: {
                userName: caseIdOrName
            }
        });
    });

    $('#caseIdOrName').bind('keypress',function(event){//监听sim卡回车事件
        if(event.keyCode == "13"){  
            var caseIdOrName = $("#caseIdOrName").val();
            // $("#userName").val(caseIdOrName);
            //执行重载
            table.reload('case-table', {
                page: {
                curr: 1  //重新从第 1 页开始
                }
                ,where: {
                    userName: caseIdOrName
                }
            });
        }
    });
})