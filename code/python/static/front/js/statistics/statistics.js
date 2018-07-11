

//function iniEchars(divId,url,param) {
//	var myChart = echarts.init(document.getElementById('endingBox'));
//	$.ajax({
//		cache : false,
//		type : "get",
//		url : "/api/v1/statistics/embryo/outcome",
//		async : false,
//		error : function(request) {
//			parent.layer.alert(request.responseText);
//		},
//		success : function(data) {
//			var nameData = new Array();;
//			var countData = new Array();;
//			if(data.code=="0") {
//				for (var i = 0; i < data.data.length; i++) {
//					var obj = data.data[i];
//					nameData.push(obj.name);
//					countData.push(obj.count);
//				}
//			}
//			// 指定图表的配置项和数据
//			var option = {
//				xAxis : {
//					data : nameData
//				},
//				yAxis : {},
//				series : [ {
//					type : 'bar',
//					data : countData
//				} ]
//			};
//			myChart.hideLoading();
//			// 使用刚指定的配置项和数据显示图表。
//			myChart.setOption(option);
//		}
//	});
//	myChart.setOption(option);
//}
//
//$(function() {
//	//iniEchars(divId,option);
//	
//	
//	
//	
//});


 


// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('endingBox'));
myChart.showLoading();


$.ajax({
	cache : false,
	type : "get",
	url : "/api/v1/statistics/embryo/outcome",
	async : false,
	error : function(request) {
		parent.layer.alert(request.responseText);
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
			} ]
		};
		myChart.hideLoading();
		// 使用刚指定的配置项和数据显示图表。
		myChart.setOption(option);
	}
});

var myChart = echarts.init(document.getElementById('milestone'));
myChart.showLoading();
$.ajax({
	cache : false,
	type : "get",
	url : "/api/v1/statistics/milestone/embryos",
	async : false,
	error : function(request) {
		parent.layer.alert(request.responseText);
	},
	success : function(data) {
		// 指定图表的配置项和数据
		option = {
				tooltip : {
					trigger : 'item',
					formatter : "{a} <br/>{b} : {c} ({d}%)"
				},
				calculable : true,
				series : [ {
					radius : [30, 148],
					roseType : 'radius',
					name : '胚胎数',
					type : 'pie',
					roseType : 'area',
					data : data.data
				} ]
			};
		myChart.hideLoading();
		// 使用刚指定的配置项和数据显示图表。
		myChart.setOption(option);
	}
});




var myChart = echarts.init(document.getElementById('pregnancyRate'));
option = {
	tooltip : {
		trigger : 'item',
		formatter : "{a} <br/>{b}: {c} ({d}%)"
	},
	series : [ {
		name : '访问来源',
		type : 'pie',
		labelLine : {
			normal : {
				show : false
			}
		},
		data : [ {
			value : 335,
			name : '直接访问'
		}, {
			value : 310,
			name : '邮件营销'
		}, {
			value : 234,
			name : '联盟广告'
		}, {
			value : 135,
			name : '视频广告'
		}, {
			value : 1548,
			name : '搜索引擎'
		} ]
	} ]
};
myChart.setOption(option);

