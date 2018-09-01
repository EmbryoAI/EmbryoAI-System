layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

// 表格配置
    table.render({
        elem: '#cycle-table',
        page: false,
        url : '/api/v1/procedure/list',
        cols: [
            [
                {
                    field: 'boxNum',
                    title: '箱皿胚胎',
					align: 'center',
                    templet: '#boxNum',
                },{
                    field: 'grade',
                    title: '评分',
					align: 'center',
                }, {
                    field: 'end',
                    title: '结局',
					align: 'center',
                }
            ]
        ],
        data: [{
            "boxNum": "2-1-1",
            "cycle1": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle2":"<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle3": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle4": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle5": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle6": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle7": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "grade": "<span class='grade'>100</span>",
            "end": "<span class='paoq'>抛弃</span>",
			// "end": "<span class='lengd'>冷冻</span>",
            // "end": "<span class='daid'>待定</span>",
            // "end": "<span class='yiz'>移植</span>",
        },{
            "boxNum": "2-1-1",
            "cycle1": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle2":"<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle3": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle4": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle5": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle6": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "cycle7": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
            "grade": "<span class='grade'>100</span>",
            // "end": "<span class='paoq'>抛弃</span>",
			"end": "<span class='lengd'>冷冻</span>",
            // "end": "<span class='daid'>待定</span>",
            // "end": "<span class='yiz'>移植</span>",
        }
		]
    });

})
