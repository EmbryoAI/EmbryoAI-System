layui.use(['layer'],
				function() {
					var layer = layui.layer;
					//胚胎结局统计方法
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
									} ]
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
										series : [{
											radius : [30, 148],
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
								layer.alert("生化妊娠率、临床妊娠率、临床着床率统计异常,请联系稍后再试或联系管理员");
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
})
 


 


 






 
