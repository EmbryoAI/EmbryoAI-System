var table = null;
layui
		.use(
				[ 'form', 'jquery', 'laydate', 'table', 'layer' ],
				function() {
					var form = layui.form;
					var $ = layui.jquery;
					var laydate = layui.laydate;
					table = layui.table;
					var layer = layui.layer;

					// 日期插件配置
					laydate.render({
						elem : '#ecTime',
						range : '~',
						format : 'yyyy-MM-dd ',
						max : 0
					});
					laydate.render({
						elem : '#insemiTime',
						range : '~',
						format : 'yyyy-MM-dd ',
						max : 0
					});
					// 表格配置
					table
							.render({
								elem : '#case-table',
								page : true,
								url : '/api/v1/procedure/list',
								cols : [ [
										{
											field : 'medical_record_no',
											title : '病历号',
											templet : function(d) {

												if (d.medical_record_no != null
														&& d.medical_record_no != '') {
													return "<a href='javascript:void()' onclick='showDetail(\""
															+ d.id
															+ "\")' class='layui-table-link view' >"
															+ d.medical_record_no
															+ "</a> ";
												} else {
													return "无";
												}
											}
										},
										{
											field : 'patient_name',
											title : '姓名'
										},
										{
											field : 'patient_age',
											title : '年龄',
										},
										{
											field : 'pts',
											title : '胚胎数'
										},
										{
											field : 'insemi_time',
											title : '授精时间',
											width : 180,
											sort : true
										},
										{
											field : 'sjfs',
											title : '授精方式',
										},
										{
											field : 'zzjd',
											title : '最终阶段',
										},
										{
											width : 180,
											field : 'state',
											title : '状态',
										},
										{

											width : 120,
											field : 'xst',
											title : '视图',
											templet : function(d) {

												if (d.xst != null
														&& d.xst != '') {
													var arr = d.xst.split(",");
													var url = "";
													for (var i = 0; i < arr.length; i++) {
														url += "<a href='javascript:void()' class='layui-table-link view' >皿"
																+ (i + 1)
																+ "</a> ";
													}
													return url;
												} else {
													return "无";
												}
											}
										}, {
											field : 'operation',
											title : '操作',
											width : 240,
											templet : function(d) {
												var a="<a style='cursor: pointer;' class='layui-table-link report'>报告</a>";
												var b="<a style='cursor: pointer;' onclick='toReturnVisit(\""+d.id+"\")' class='layui-table-link return'>回访</a>";
												var c="<a style='cursor: pointer;' onclick='deleteProcedure(\""+d.id+"\");' class='layui-table-link del'>删除</a>";
												return a+b+c;
											}
										} ] ]
							});

					table.on('tool(case-table)', function(obj) {
						var event = obj.event;
						var id = obj.data.id;
						if (event === 'details') {
							layer.open({

								title : "病历详情",
								type : 2,
								area : [ '1020px', '610px' ],
								maxmin : true,

								shadeClose : false,
								content : '/front/procedure/' + id
							});
						}

					});
					
					// 获取状态字典值
					$.ajax({
						type : "get",
						url : "/api/v1/dict/list/state",
						datatype : "json",
						success : function(data) {
							if (data.code == 0) {
								for (var i = 0; i < data.data.length; i++) {
									$("#state").append(
											"<option value='" + data.data[i].dictValue + "'>"
													+ data.data[i].dictValue + "</option>");

								}
							} else {
								layer.alert(data.msg);
							}
						},
						error : function(request) {
							layer.alert(request.responseText);
						}
					});

					$('#medicalRecordNo').autocompleter({
						highlightMatches : true,
						minLength : 3,
						source : '/api/v1/procedure/no/list',
						cache : false

					});

					$('#userName').autocompleter({
						highlightMatches : true,
						source : '/api/v1/patient/name/list',
						cache : false
					});
				})

function toReturnVisit(id){
	layer.open({
		title : "病历回访",
		type : 2,
		area : [ '300px', '300px' ],
		maxmin : true,
		shadeClose : false,
		content : '/front/feedback/return_visit/' + id
	});
}

function showDetail(id) {
	layer.open({
		title : "病历详情",
		type : 2,
		area : [ '1020px', '610px' ],
		maxmin : true,
		shadeClose : false,
		content : '/front/procedure/' + id
	});
}

//刪除病例
function deleteProcedure(id) {
    layer.confirm('真的删除该病历么？', function(index){
//        obj.del(); //删除对应行（tr）的DOM结构
//        layer.close(index);
        //向服务端发送删除指令
    	$.ajax({
    		cache : false,
    		type : "get",
    		url : "/api/v1/procedure/delete/" + id,
    		async : false,
    		error : function(request) {
    			layer.alert(request.responseText);
    		},
    		success : function(data) {
    			layer.alert("删除病例成功!");
    			reload();//刷新当前页面.
    		}
    	});
    	
   });
} 

// 查询
function reload() {
	// 执行重载
	table.reload('case-table', {
		page : {
			curr : 1
		// 重新从第 1 页开始
		},
		where : {
			userName : $("#userName").val(),
			medicalRecordNo : $("#medicalRecordNo").val(),
			ecTime : $("#ecTime").val(),
			insemiTime : $("#insemiTime").val(),
			state : $("#state").val()
		}
	});
}

// 重置
function reset() {
	$("#userName").val("");
	$("#medicalRecordNo").val("");
	$("#ecTime").val("");
	$("#insemiTime").val("");
	$("#state").val("");
	reload();
}