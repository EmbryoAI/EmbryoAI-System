//function iniEchars(divId,option) {
//	var myChart = echarts.init(document.getElementById('endingBox'));
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
option = {
	tooltip : {
		trigger : 'item',
		formatter : "{a} <br/>{b} : {c} ({d}%)"
	},
	calculable : true,
	series : [ {
		name : '面积模式',
		type : 'pie',
		roseType : 'area',
		data : [ {
			value : 10,
			name : 'rose1'
		}, {
			value : 5,
			name : 'rose2'
		}, {
			value : 15,
			name : 'rose3'
		}, {
			value : 25,
			name : 'rose4'
		}, {
			value : 20,
			name : 'rose5'
		}, {
			value : 35,
			name : 'rose6'
		}, {
			value : 30,
			name : 'rose7'
		}, {
			value : 40,
			name : 'rose8'
		} ]
	} ]
};
myChart.setOption(option);




var myChart = echarts.init(document.getElementById('pregnancyRate'));

option = {
	tooltip : {
		trigger : 'item',
		formatter : "{a} <br/>{b}: {c} ({d}%)"
	},
	legend : {
		orient : 'vertical',
		x : 'left',
		data : [ '直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎' ]
	},
	series : [ {
		name : '访问来源',
		type : 'pie',
		avoidLabelOverlap : false,
		label : {
			normal : {
				show : false,
				position : 'center'
			},
			emphasis : {
				show : true,
				textStyle : {
					fontSize : '30',
					fontWeight : 'bold'
				}
			}
		},
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

