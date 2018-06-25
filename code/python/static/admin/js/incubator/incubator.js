layui.use('table', function(){
	  var table = layui.table;
 
	  //方法级渲染
	  table.render({
	    elem: '#incubator'
	    ,url: '/api/v1/incubator/list'
	    ,cols: [[
	      {checkbox: true, fixed: true}
	      ,{field:'incubatorCode', title: '培养箱编码', width:140, sort: true}
	      ,{field:'incubatorBrand', title: '培养箱品牌', sort: true, width:120}
	      ,{field:'incubatorType', title: '培养箱型号', sort: true, width:120}
	      ,{field:'delFlag', title: '状态', width:80, templet: function(d){
	            if(d.delFlag == 0){
	                return '正常'
	              }else{
	                return '无效'
	              }
	            }}
	      ,{field:'incubatorDescription', title: '培养箱描述备注'}
	      ,{field:'createTime', title: '创建时间', width:150}
	      ,{field:'updateTime', title: '修改时间', width:150}
	      ,{field:'right', title: '操作', width:118,toolbar:"#barDemo"}
	    ]]
	    ,id: 'testReload'
	    ,page: true
	    ,height: 'full-200',
	    cellMinWidth: 80
	  });
	  
	  //监听工具条
	  table.on('tool(incubator)', function(obj){ //注：tool是工具条事件名，incubator是table原始容器的属性 lay-filter="对应的值"
	    var data = obj.data //获得当前行数据
	    ,layEvent = obj.event; //获得 lay-event 对应的值
	    
	    if(layEvent === 'detail'){
	      layer.msg('查看操作');
	    } else if(layEvent === 'del'){
	      layer.confirm('真的删除行么', function(index){
//	        obj.del(); //删除对应行（tr）的DOM结构
//	        layer.close(index);
	        //向服务端发送删除指令
	    	$.ajax({
	    		cache : false,
	    		type : "get",
	    		url : "/api/v1/incubator/delete/" + data.id,
	    		async : false,
	    		error : function(request) {
	    			parent.layer.alert(request.responseText);
	    		},
	    		success : function(data) {
	    			parent.layer.alert("删除培养箱成功，状态设置为无效!");
	    			table.reload('testReload');//刷新当前页面.
	    		}
	    	});
	    	
	      });
	    } else if(layEvent === 'edit'){
	    	layer.open({
	    		type : 2,
	    		title : '编辑',
	    		maxmin : true,
	    		shadeClose : false, // 点击遮罩关闭层
	    		area : [ '800px', '520px' ],
	    		content:'/admin/incubator/toEdit/' + data.id,
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
	        	incubatorCode: demoReload.val()
	        }
	      });
	    },getCheckData: function(){ //获取选中数据
		      var checkStatus = table.checkStatus('testReload')
		      ,data = checkStatus.data;
		      layer.alert(JSON.stringify(data));
		    }
		    ,getCheckLength: function(){ //获取选中数目
		      var checkStatus = table.checkStatus('testReload')
		      ,data = checkStatus.data;
		      layer.msg('选中了：'+ data.length + ' 个');
		    }
		    ,isAll: function(){ //验证是否全选
		      var checkStatus = table.checkStatus('testReload');
		      layer.msg(checkStatus.isAll ? '全选': '未全选')
		    },toAdd: function(){ //去新增培养箱页面
	            layer.open({
	                type : 2,
	                title : '培养箱新增',
	                maxmin : true,
	                shadeClose : false, // 点击遮罩关闭层
	                area : [ '800px', '520px' ],
	                content:'/admin/incubator/toAdd/',
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