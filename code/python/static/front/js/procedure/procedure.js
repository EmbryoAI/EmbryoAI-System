
$.ajax({
    type:"get",
    url:"/api/v1/dict/list/state",
    datatype: "json", 
    success:function(data){
    	if(data.code==0){
    		for(var i=0;i<data.data.length;i++) {
    			$("#state").append("<option value='"+data.data[i].dictValue+"'>"+data.data[i].dictValue+"</option>");
        		}
        	}else {
        		parent.layer.alert(data.msg);
        	}
        },
        error : function(request) {
            parent.layer.alert(request.responseText);
        }
});
var table = null;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    table = layui.table;
    var layer = layui.layer;

    // 日期插件配置
    laydate.render({
        elem: '#ecTime',
        range: '~',
        format: 'yyyy-MM-dd ',
        max: 0
    });
    laydate.render({
        elem: '#insemiTime',
        range: '~',
        format: 'yyyy-MM-dd ',
        max: 0
    });
// 表格配置
    table.render({
        elem: '#case-table',
        page: true,
		url: '/api/v1/procedure/list',
        cols: [
            [
                {
                    field: 'id',
                    title: '病历号',
                    templet: '#details-id'
                }, {
                    field: 'name',
                    title: '姓名'
                }, {
                    field: 'patientAge',
                    title: '年龄',
                }, {
                    field: 'embryo',
                    title: '胚胎数'
                }, {
                    field: 'insemiTime',
                    title: '授精时间', 
					sort: true
                }, {
                    field: 'way',
                    title: '授精方式',
                }, {
                    field: 'phases',
                    title: '最终阶段',
                }, {
                    field: 'state',
                    title: '状态',
                }, {
                    field: 'view',
                    title: '视图',
                    templet: '#view',
                }, {
                    field: 'operation',
                    title: '操作',
                    width: 240,
                    templet: '#operation',
                }
            ]
        ]
    });
    
    table.on('tool(case-table)', function(obj){
        var event = obj.event;
        var id = obj.data.id;
        
        if(event === 'details'){
            layer.open({
              title:"病历详情",
              type: 2,
              area: ['1020px', '560px'],
              maxmin : true,
              shadeClose: false,
              content: '/front/procedure/' + id
            });
        }
 
    });
	


})

	  function reload(){
		      //执行重载
		      table.reload('case-table', {
		        page: {
		          curr: 1 //重新从第 1 页开始
		        }
		        ,where: {
		        	userName: $("#userName").val(),
		        	medicalRecordNo: $("#medicalRecordNo").val(),
		        	ecTime: $("#ecTime").val(),
		        	insemiTime: $("#insemiTime").val(),
		        	state: $("#state").val()
		        }
		      });
		    }
    
    function reset(){
	        	$("#userName").val("");
	        	$("#medicalRecordNo").val("");
	        	$("#ecTime").val("");
	        	$("#insemiTime").val("");
	        	$("#state").val("");
			      //执行重载
			      table.reload('case-table', {
			        page: {
			          curr: 1 //重新从第 1 页开始
			        }
			      });
			}