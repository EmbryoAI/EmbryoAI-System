layui.use('table', function(){
	  var table = layui.table;
 
	  //方法级渲染
	  table.render({
	    elem: '#test'
	    ,url: '/admin/demo/list/'
	    ,cols: [[
	      {checkbox: true, fixed: true}
	      ,{field:'id', title: 'ID', width:80, sort: true, fixed: true}
	      ,{field:'username', title: '用户名', width:80}
	      ,{field:'sex', title: '性别', width:80, sort: true}
	      ,{field:'city', title: '城市', width:80}
	      ,{field:'sign', title: '签名'}
	      ,{field:'experience', title: '积分', sort: true, width:80}
	      ,{field:'score', title: '评分', sort: true, width:80}
	      ,{field:'classify', title: '职业', width:80}
	      ,{field:'wealth', title: '财富', sort: true, width:135}
	      ,{field:'right', title: '操作', width:188,toolbar:"#barDemo"}
	    ]]
	    ,id: 'testReload'
	    ,page: true
	    ,height: 'full-200',
	    cellMinWidth: 80
	  });
	  
	  //监听工具条
	  table.on('tool(test)', function(obj){ //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
	    var data = obj.data //获得当前行数据
	    ,layEvent = obj.event; //获得 lay-event 对应的值
	    
	    if(layEvent === 'detail'){
	      layer.msg('查看操作');
	    } else if(layEvent === 'del'){
	      layer.confirm('真的删除行么', function(index){
	        obj.del(); //删除对应行（tr）的DOM结构
	        layer.close(index);
	        //向服务端发送删除指令
	      });
	    } else if(layEvent === 'edit'){
	    	layer.open({
	    		type : 2,
	    		title : '增加',
	    		maxmin : true,
	    		shadeClose : false, // 点击遮罩关闭层
	    		area : [ '800px', '520px' ],
	    		content:'/add' // iframe的url
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
	          key: {
	            id: demoReload.val()
	          }
	        }
	      });
	    }
	  };
	  
	  $('.demoTable .layui-btn').on('click', function(){
	    var type = $(this).data('type');
	    active[type] ? active[type].call(this) : '';
	  });
	  
	  

	});