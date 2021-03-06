layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    // 日期插件配置
		//定义接收本月的第一天和最后一天
		var startDate1=new Date(new Date().setDate(1));
		var endDate1=new Date(new Date(new Date().setMonth(new Date().getMonth()+1)).setDate(0));
		//定义接收上个月的第一天和最后一天
		var startDate2=new Date(new Date(new Date().setMonth(new Date().getMonth()-1)).setDate(1));
		var endDate2=new Date(new Date().setDate(0));		
    laydate.render({
        elem: '#pull',
        range: '~',
        format: 'yyyy/MM/dd ',
        max: 0,
				extrabtns: [{
				        id: 'today',
				        text: '今天',
				        range: [new Date(), new Date()]
				    },
				    {
				        id: 'yesterday',
				        text: '昨天',
				        range: [new Date(new Date().setDate(new Date().getDate() - 1)),
				            new Date()
				        ]
				    },
						{
								id: 'lastday-2',
								text: '前天',
								range: [new Date(new Date().setDate(new Date().getDate() - 2)),
										new Date()
								]
						},
						{
								id: 'lastday-3',
								text: '三天内',
								range: [new Date(new Date().setDate(new Date().getDate() - 3)),
										new Date()
								]
						},
						{
								id: 'lastday-5',
								text: '五天内',
								range: [new Date(new Date().setDate(new Date().getDate() - 4)),
										new Date()
								]
						}
				],
    });
    laydate.render({
        elem: '#insmt',
        range: '~',
        format: 'yyyy/MM/dd ',
        max: 0,
				extrabtns: [{
								id: 'today',
								text: '今天',
								range: [new Date(), new Date()]
						},
						{
								id: 'yesterday',
								text: '昨天',
								range: [new Date(new Date().setDate(new Date().getDate() - 1)),
										new Date()
								]
						},
						{
								id: 'lastday-2',
								text: '前天',
								range: [new Date(new Date().setDate(new Date().getDate() - 2)),
										new Date()
								]
						},
						{
								id: 'lastday-3',
								text: '三天内',
								range: [new Date(new Date().setDate(new Date().getDate() - 3)),
										new Date()
								]
						},
						{
								id: 'lastday-5',
								text: '五天内',
								range: [new Date(new Date().setDate(new Date().getDate() - 4)),
										new Date()
								]
						}
				],
    });
// 表格配置
    table.render({
        elem: '#case-table',
        page: true,
        cols: [
            [
                {
                    field: 'number',
                    title: '病历号',
                    templet: '#number',
                }, {
                    field: 'name',
                    title: '姓名'
                }, {
                    field: 'age',
                    title: '年龄',
                }, {
                    field: 'embryo',
                    title: '胚胎数'
                }, {
                    field: 'time',
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
        ],
        data: [{
            "number": "A565232",
            "name": "赵莎莎",
            "age": "15",
            "embryo": 2,
            "time": "2208/08/05 10:10",
            "way": "ifv",
            "phases": "day3",
            "state": "抛弃",
            "view": ["皿1", "皿2"],
            "operation": ["报告", "回访", "删除"],
        }]
    });
	
	// 弹窗详情
	 $('.details').on('click', function(){
    layer.open({
		title:"病历详情",
      type: 1,
      area: ['1020px', '560px'],
      shadeClose: true,
      content:$('.details-box')
    });
  });
  // 删除确认
  $('.del').on('click', function(){
	 layer.confirm('确认要删除此条病历吗？', {
	  btn: ['确认','取消'] 
	}, function(){
	  layer.msg('删除成功', {
		  time:1500,
		  icon: 1});
	}, function(){
	  // layer.msg('取消');
	});
  });
  
  // 弹窗回访
  $('.return').on('click', function(){
  layer.open({
  	title:"回访",
  	type: 1,
  	area: ['320px', '290px'],
  	shadeClose: true,
  	content:$('.return-box')
	});
  });
  

})
