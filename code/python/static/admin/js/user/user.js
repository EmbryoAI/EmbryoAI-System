layui.use('table', function(){
    var table = layui.table;

    //方法级渲染
    table.render({
      elem: '#user'
      ,url: '/api/v1/user'
      ,cols: [[
        {checkbox: true, fixed: true}
        ,{field:'username', title: '用户名', width:130}
        ,{field:'email', title: '电子邮箱', width:180}
        ,{field:'mobile', title: '手机号码', width:130}
        ,{field:'truename', title: '真实姓名', width:90}
        ,{field:'title', title: '职称', width:80}
        ,{field:'lastLoginTime', title: '最后登录时间', width:160}
        ,{field:'delFlag', title: '删除状态', width:90, templet: function(d){
            if(d.delFlag == 0){
              return '正常使用'
            }else{
              return '已删除'
            }
          }}
        ,{field:'right', title: '操作', width:175,toolbar:"#barDemo"}
      ]]
      ,id: 'testReload'
      ,page: true
      ,height: 'full-200',
      cellMinWidth: 80
    });
    
    //监听工具条
    table.on('tool(user)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
      var data = obj.data //获得当前行数据
      ,layEvent = obj.event; //获得 lay-event 对应的值
      
      if(layEvent === 'detail'){
        layer.open({
          type : 2,
          title : '用户详情',
          maxmin : true,
          shadeClose : false, // 点击遮罩关闭层
          area : [ '800px', '520px' ],
          content:'/admin/user/detail/' + data.id,
          end:function(index,layero){
               table.reload('testReload');//刷新当前页面.
          }
        });
      } else if(layEvent === 'del'){
        layer.confirm('真的删除行么', function(index){
          obj.del(); //删除对应行（tr）的DOM结构
          layer.close(index);
          //向服务端发送删除指令
          $.ajax({
            cache : false,
            type : "DELETE",
            url : "/api/v1/user/" + data.id,
            data : "",
            async : false,
            error : function(request) {
              parent.layer.alert(request.responseText);
            },
            success : function(data) {
              parent.layer.alert("用户删除成功!");
              var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
              parent.layer.close(index);
            }
          });
        });
      } else if(layEvent === 'edit'){
        layer.open({
          type : 2,
          title : '用户详情',
          maxmin : true,
          shadeClose : false, // 点击遮罩关闭层
          area : [ '800px', '520px' ],
          content:'/admin/user/edit/' + data.id,
          end:function(index,layero){
               table.reload('testReload');//刷新当前页面.
          }
        });
      }
    });
    

    var $ = layui.$, active = {
      reload: function(){
        var demoReload = $('#demoReload');
        //执行重载
        table.reload('testReload', {
          page: {
            curr: 1 //重新从第 1 页开始
          }
          ,where: {
             username : $("#username").val()
          }
        });
      },toAdd: function(){ //去新增用户页面
            layer.open({
                type : 2,
                title : '用户新增',
                maxmin : true,
                shadeClose : false, // 点击遮罩关闭层
                area : [ '800px', '520px' ],
                content:'/admin/user/toAdd/',
                end:function(index,layero){
                  table.reload('testReload');//刷新当前页面.
                }
            });
          }
    };
    
    $('.demoTable .layui-btn').on('click', function(){
      var type = $(this).data('type');
      active[type] ? active[type].call(this) : '';
    });
    
    

  });