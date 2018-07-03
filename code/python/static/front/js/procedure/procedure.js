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
