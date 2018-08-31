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
            area: ['400px', '230px'],
            shadeClose: true,
            content: '/admin/user/toModifyPass',
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

    //搜索框监听回车事件
    $('#caseIdOrName').bind('keypress',function(event){
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

function openAddCase() {
	layer.open({
		title : "病历详情",
		type : 2,
		area : [ '1500px', '700px' ],
		maxmin : true,
		shadeClose : false,
        content : '/front/procedure/add',
        end:function(index,layero){
            reload();
        }
	});
}