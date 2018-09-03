layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
    var table = layui.table;
		
$(function () {

		$('#stage').on('click', 'span[data-tab]', function () {
				var index = $(this).attr('data-tab');
				if(index == 0){
					$('#tableSec .node').addClass('show');
				}else{
					$('#tableSec .node').addClass('hide');
					$('#tableSec .show').removeClass('show');
					$('#tableSec div[data-index=\"' + index + '\"]').addClass('show');
				}
				
		})
		$('#stage').on('click','span',function(){
				$('#stage span').removeClass('active');
				$(this).addClass('active');
		})
		//修改标题
		
	 $('#alter').on('click', function(){
		// 获取下拉框的值
		const  nameSelect = document.getElementById("nameSelect");
		const  index = nameSelect.selectedIndex ; 
		const  Oindex= nameSelect.options[index].text ;
    layer.prompt({
			title:"修改名称",
        formType: 2,
        value: Oindex,
      }, function(value, index){
        //确定按钮的回调
				layer.msg("修改成功")
        layer.close(index);//关闭窗口
      });
  });
	//设置为默认
	$('#setDefault').on('click', function(){
		const  nameSelect = document.getElementById("nameSelect");
		const  index = nameSelect.selectedIndex ; 
		const  Oindex= nameSelect.options[index].text ;
		
		layer.confirm('是否将标准 “ '+Oindex+" ” 设置为默认？", {
		btn: ['确认', '取消' ]},
		 function(index, layero){
				//确认按钮的回调
				layer.msg("设置成功")
				layer.close(index);//关闭窗口
			}, function(index){
				
			});
	});
	//新增标准
	$('#addScheme').on('click', function(){
		layer.open({
			type: 2,
			maxmin: true,
			title: '新增标准',
			area : ['900px' , '80%'],
			content: 'scheme-add.html',
			btnAlign: 'c',
			btn: ['确定', '取消'],
			yes: function(index, layero){
				//按钮【按钮一】的回调
				layer.msg("编辑成功！")
				layer.close(index);//关闭窗口
			},
			btn2: function(index, layero){
				//按钮【按钮二】的回调
			}
		});
	})
	
	//添加行
	$('.addbtn').on('click', function(){
		layer.open({
			type: 2,
			maxmin: true,
			title: '编辑',
			area : ['560px' , '360px'],
			content: 'scheme-tableadd.html',
			btnAlign: 'c',
			btn: ['确定', '取消'],
			yes: function(index, layero){
				//按钮【按钮一】的回调
				layer.msg("新增成功")
				layer.close(index);//关闭窗口
			},
			btn2: function(index, layero){
				//按钮【按钮二】的回调
			}
		});
	})
	
	// PN表格配置
	    table.render({
	        elem: '#pn',
	        cols: [
	            [
	                {
	                    field: 'option',
	                    title: '条件',
	                }, {
	                    field: 'symbol',
	                    title: '符合'
	                }, {
	                    field: 'value',
	                    title: '判断值',
	                }, {
	                    field: 'grade',
	                    title: '分值'
	                }, {
	                    field: 'operation',
	                    title: '操作',
	                    width: 240,
	                    templet: '#operation',
	                }
	            ]
	        ],
	        data: [{
	            "option": "时间",
	            "symbol": "=",
	            "value": "15h",
	            "grade": "15",
	            "operation":[ "编辑", "删除"] ,
	        }]
	    });
  //监听行工具事件
  table.on('tool(pn)', function(obj){
    var data = obj.data;
    if(obj.event === 'del'){
      layer.confirm('确定要删除此行吗？', function(index){
        obj.del();
				layer.msg("删除成功")
        layer.close(index); //关闭窗口
      });
    } else if(obj.event === 'edit'){
       layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
    }
  });
	// 2C表格配置
			table.render({
					elem: '#2C',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(2C)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});
	// 3C表格配置
			table.render({
					elem: '#3C',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(3C)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});
	// 4C表格配置
			table.render({
					elem: '#4C',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(4C)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});
	// 5C表格配置
			table.render({
					elem: '#5C',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(5C)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});
	// 8C表格配置
			table.render({
					elem: '#8C',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(8C)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});	
	// 囊胚表格配置
			table.render({
					elem: '#nangp',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(nangp)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});
	// 扩张囊胚表格配置
			table.render({
					elem: '#kuo',
					cols: [
							[
									{
											field: 'option',
											title: '条件',
									}, {
											field: 'symbol',
											title: '符合'
									}, {
											field: 'value',
											title: '判断值',
									}, {
											field: 'grade',
											title: '分值'
									}, {
											field: 'operation',
											title: '操作',
											width: 240,
											templet: '#operation',
									}
							]
					],
					data: [{
							"option": "时间",
							"symbol": "=",
							"value": "15h",
							"grade": "15",
							"operation":[ "编辑", "删除"] ,
					}]
			});
	//监听行工具事件
	table.on('tool(kuo)', function(obj){
		var data = obj.data;
		if(obj.event === 'del'){
			layer.confirm('确定要删除此行吗？', function(index){
				obj.del();
				layer.msg("删除成功")
				layer.close(index); //关闭窗口
			});
		} else if(obj.event === 'edit'){
			layer.open({
				type: 2,
				maxmin: true,
				title: '编辑',
				area : ['560px' , '360px'],
				content: 'scheme-tableedit.html',
				btnAlign: 'c',
				btn: ['确定', '取消'],
				yes: function(index, layero){
					//按钮【按钮一】的回调
					layer.msg("修改成功")
					layer.close(index);//关闭窗口
				},
				btn2: function(index, layero){
					//按钮【按钮二】的回调
				}
			});
		}
	});	
	
   })	
})
