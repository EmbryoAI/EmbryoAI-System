layui.use(['form', 'jquery', 'laydate', 'table', 'layer'],
				function() {
					var form = layui.form;
					var $ = layui.jquery;
					var laydate = layui.laydate;
					var table = layui.table;
					var layer = layui.layer;
					//胚胎结局统计方法
					
					
 // 日期插件配置
		//定义接收本月的第一天
		var startDate1=new Date(new Date().setDate(1));
		//定义今年的第一天
		var startYear=new Date(new Date().setFullYear(new Date().getFullYear(),0,1));
    laydate.render({
        elem: '#embryoOutcomeDate',
        range: '~',
        format: 'yyyy/MM/dd ',
        max: 0,
		extrabtns: [{
				id: 'thismonth',
				text: '本月',
				range: [startDate1,new Date()]
			},
				{
						id: 'thisyear',
						text: '本年',
						range: [startYear,new Date()]
				}					
		],
		ready: function(date){
		$(".laydate-main-list-0 .laydate-prev-m").click();
		}
    });
    laydate.render({
        elem: '#pregnancyRateDate',
        range: '~',
        format: 'yyyy/MM/dd ',
        max: 0,
		extrabtns: [{
				id: 'thismonth',
				text: '三个月内',
				range: [new Date(new Date().setDate(new Date().getDate()-91)),new Date()]
			},
				{
						id: 'thisyear',
						text: '本年',
						range: [startYear,new Date()]
				}					
		],
		ready: function(date){
		$(".laydate-main-list-0 .laydate-prev-m").click();
		}
    });					
					
	function embryoOutcome() {
		$.ajax({
			cache : false,
			type : "get",
			url : "/api/v1/statistics/embryo/outcome?ecTime="+$("#embryoOutcomeDate").val(),
			async : false,
			error : function(request) {
				layer.alert("胚胎结局统计异常,请联系稍后再试或联系管理员");
			},
			success : function(data) {
				var nameData = new Array();;
				var countData = new Array();;
				if(data.code=="0") {
					for (var i = 0; i < data.data.length; i++) {
						var obj = data.data[i];
						nameData.push(obj.name);
						countData.push(obj.count);
					}
				}
				// 指定图表的配置项和数据
				var option = {
					
					xAxis : {
						data : nameData
					},
					yAxis : {},
					series : [ {
						type : 'bar',
						data : countData
					} ],
					color: [
						'#d87a80','#b6a2de','#5ab1ef','#ffb980','#d87a80',
					],
				};
				endingBox1.hideLoading();
				// 使用刚指定的配置项和数据显示图表。
				endingBox1.setOption(option);
			}
		});
	}
	
	//周期中里程碑点胚胎数
	function milestoneEmbryos(){
		$.ajax({
			cache : false,
			type : "get",
			url : "/api/v1/statistics/milestone/embryos",
			async : false,
			error : function(request) {
				layer.alert("周期中里程碑点胚胎数异常,请联系稍后再试或联系管理员");
			},
			success : function(data) {
				// 指定图表的配置项和数据
				option = {
						tooltip : {
							trigger : 'item',
							formatter : "{a} <br/>{b} : {c} ({d}%)"
						},
						calculable : true,
						legend: {
							orient: 'vertical',
							x: 'left',
							data:data.data
						},
						color: [
							'#2ec7c9','#b6a2de','#5ab1ef','#ffb980','#d87a80',
							'#8d98b3','#e5cf0d','#97b552','#95706d','#dc69aa',
							'#07a2a4','#9a7fd1','#588dd5','#f5994e','#c05050',
							'#59678c','#c9ab00','#7eb00a','#6f5553','#c14089'
						],
						series : [{
							radius : [80, 130],
							roseType : 'radius',
							name : '胚胎数',
							type : 'pie',
							data : data.data
						}]
					};
				myChart.hideLoading();
				//使用刚指定的配置项和数据显示图表。
				myChart.setOption(option);
			}
		});
	}
	
	//生化妊娠率、临床妊娠率、临床着床率 
	function pregnancyRate() {
		$.ajax({
			cache : false,
			type : "get",
			url : "/api/v1/statistics/pregnancy/rate?ecTime="+$("#embryoOutcomeDate").val(),
			async : false,
			error : function(request) {
				layer.alert("生化妊娠率、临床妊娠率、临床着床率统计异常,请稍后再试或联系管理员");
			},
			success : function(data) {
				$("#shrsl").html(data.data[0].shrsl);//生化妊娠率
				$("#lcrsl").html(data.data[0].lcrsl);//临床妊娠率
				$("#lczcl").html(data.data[0].lczcl);//临床着床率
			}
		});
	}
	
	$("#embryoOutcomeButton").on("click", function (event) {
		endingBox1.showLoading();
		embryoOutcome();
	});
	
	$("#pregnancyRateButton").on("click", function (event) {
		pregnancyRate();
	});
	
	//胚胎结局统计初始化
	embryoOutcome();
	
	//周期中里程碑点胚胎数初始化
	milestoneEmbryos();
	
	//生化妊娠率、临床妊娠率、临床着床率初始化 
	pregnancyRate();


	$(function() {
		$('.circle').each(function(index, el) {
			var num = $(this).find('span').text() * 3.6;
			if (num<=180) {
				$(this).find('.right').css('transform', "rotate(" + num + "deg)");
			} else {
				$(this).find('.right').css('transform', "rotate(180deg)");
				$(this).find('.left').css('transform', "rotate(" + (num - 180) + "deg)");
			};
		});

	});


})
 


 


 






 
