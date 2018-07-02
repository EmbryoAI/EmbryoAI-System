layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    // 日期插件配置
    laydate.render({
        elem: '#pull',
        range: '~',
        format: 'yyyy/MM/dd ',
        max: 0
    });
    laydate.render({
        elem: '#insmt',
        range: '~',
        format: 'yyyy/MM/dd ',
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
                    field: 'medical_record_no',
                    title: '病历号',
                    templet: '#details-id'
                }, {
                    field: 'patient_name',
                    title: '姓名'
                }, {
                    field: 'patient_age',
                    title: '年龄',
                }, {
                    field: 'pts',
                    title: '胚胎数'
                }, {
                    field: 'insemi_time',
                    title: '授精时间', 
					sort: true
                }, {
                    field: 'sjfs',
                    title: '授精方式',
                }, {
                    field: 'zzjd',
                    title: '最终阶段',
                }, {
                    field: 'state',
                    title: '状态',
                }, {
                    field: 'xst',
                    title: '视图'
                    , templet: function(d){
                    	if(d.xst!=null && d.xst!='') {
                    		var arr = d.xst.split(",");
                    		var url = "";
                    		for(var i=0;i<arr.length;i++) {
                    			url += "<a href='' class='layui-table-link view' >皿"+(i+1)+"</a> ";
                    		}
                    		return url;
                    	}else {
                    		return "无";
                    	}
        	        }
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
        if(event === 'details'){
            layer.open({
              title:"病历详情",
              type: 2,
              area: ['1020px', '560px'],
              maxmin : true,
              shadeClose: false,
              content: '/front/procedure/123'
            });
        }
    });
	

})
