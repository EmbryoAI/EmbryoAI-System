layer = layui.layer;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    layer = layui.layer;

// 表格配置
//    table.render({
//        elem: '#cycle-table',
//        page: false,
//        url : '/api/v1/procedure/list',
//        cols: [
//            [
//                {
//                    field: 'boxNum',
//                    title: '箱皿胚胎',
//					align: 'center',
//                    templet: '#boxNum',
//                },{
//                    field: 'grade',
//                    title: '评分',
//					align: 'center',
//                }, {
//                    field: 'end',
//                    title: '结局',
//					align: 'center',
//                }
//            ]
//        ],
//        data: [{
//            "boxNum": "2-1-1",
//            "cycle1": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle2":"<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle3": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle4": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle5": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle6": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle7": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "grade": "<span class='grade'>100</span>",
//            "end": "<span class='paoq'>抛弃</span>",
//			// "end": "<span class='lengd'>冷冻</span>",
//            // "end": "<span class='daid'>待定</span>",
//            // "end": "<span class='yiz'>移植</span>",
//        },{
//            "boxNum": "2-1-1",
//            "cycle1": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle2":"<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle3": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle4": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle5": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle6": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "cycle7": "<img src='img/icon-noembryo.jpg' class='cycle-img'><span class='cycle-t'>2h2min</span>",
//            "grade": "<span class='grade'>100</span>",
//            // "end": "<span class='paoq'>抛弃</span>",
//			"end": "<span class='lengd'>冷冻</span>",
//            // "end": "<span class='daid'>待定</span>",
//            // "end": "<span class='yiz'>移植</span>",
//        }
//		]
//    });
    
    $('#medicalRecordNo').autocompleter({
    	highlightMatches : true,
    	minLength : 3,
    	source : '/api/v1/procedure/no/list',
    		cache : false

    	});
  //如果 初始化页面时，病历号不为空，则直接查询
    if($('#medicalRecordNo').val()!="") {
    	listView();
    }
})

    //由于动态表头，需要使用静态转换成动态，首先初始化静态表格
    function listView() {
		if($("#medicalRecordNo").val()=="") {
			layer.alert("病历号不能为空!");
			return;
		}
		jaindex = layer.msg('查询中，请耐心等待', {
			  icon: 16
			  ,shade: 0.3,time:0
		});
		$("#qts").html("");
		$("#theadView").html("");
		$("#tbodyView").html("");
		$("#patientView").hide();
		$.ajax({
			type : "get",
			url : "/api/v1/procedure/list/view",
			datatype : "json",
			cache:false,
			data : {"medicalRecordNo":$("#medicalRecordNo").val()},
			success : function(data) {
				 if(data!=null && data!="null") {
					 //首先渲染患者信息
					 var obj = JSON.parse(data);
					 var patient = obj.patient;
					 var num = 0;
					 for(var key in patient){
						 $("#"+key).html(patient[key]);
						 num++;
						 if(num>4) {
							 var str = '<li class="emb"><strong>'+key+'个数：</strong><span>'+patient[key]+'</span></li>';
							 $("#qts").append(str);
						 }
					 }
					 $("#defDiv").hide();
					 $("#patientView").show();
					 
					 //渲染列表
					 var procedureViewList = obj.procedureViewList;
					 var size = procedureViewList.length;
					 var coSize = 0;//获取有多少列;
					 for(var i=0;i<size;i++) {
						 var procedure = procedureViewList[i];
						 if(i==0) {//i为0时 则为表头
							 var str = "<tr>";
							 for(var key in procedure){
								 str += "<th>"+procedure[key]+"</th>";
							 }
							 str += "</tr>";
							 $("#theadView").html(str);
						 }else {
							 var str = "<tr>";
							 for(var key in procedure){
								 //如果不为空，并且有,号则表示 是里程碑节点，需要显示图片和时间序列
								 var value = procedure[key]+"";
								 if(value!="" && value.indexOf(",")!=-1) {
									 var proArr = value.split(",");
									 str += "<td>";
									 if(proArr[0].indexOf("loc-emb.png")!=-1) {
										 str +="<img src='/static/front/img/loc-emb.png' class='cycle-img' /><br/>";
									 }else {
									 	str +="<img src='/api/v1/well/image?image_path="+obj.imageRoot+proArr[0]+"' class='cycle-img' /><br/>";
								 	 }
									 str +="<span class='cycle-t'>"+proArr[1]+"</span>";
									 str +="</td>";
								 }else {
									 if(value=="") {
										 value = "无";
									 }
									 str += "<td>"+value+"</td>";
								 }
							 }
							 str += "</tr>";
							 $("#tbodyView").append(str);
						 }
					 }
 
				 }else {
					 //该胚胎无数据
					 $("#defDiv").show();
					 layer.alert("该病历号无对应数据!");
				 }
				 layer.close(jaindex);
			},
			error : function(request) {
				layer.alert(request.responseText);
				layer.close(jaindex);
			}
		});
    }



