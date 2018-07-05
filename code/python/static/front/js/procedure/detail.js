$(function(){
    var procedureId = $("#id").val();
    $.ajax({
		cache : false,
		type : "GET",
		url : "/api/v1/procedure/" + procedureId,
		data : "",
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
            var procedure = data.data;
            $("#patient_name").html(procedure.patient_name);
            $("#idcard_no").html(procedure.idcard_no);
            $("#new_mobile").val(procedure.mobile);
            $("#new_email").val(procedure.email);
            $("#birthdate").html(procedure.birthdate);
            $("#new_address").val(procedure.address);
            $("#is_smoking").html(procedure.is_smoking);
            $("#is_drinking").html(procedure.is_drinking);
            $("#patient_age").html(procedure.patient_age);
            $("#patient_height").html(procedure.patient_height);
            $("#patient_weight").html(procedure.patient_weight);
            $("#ec_time").html(procedure.ec_time);
            $("#insemi_type").html(procedure.insemi_type);
            $("#insemi_time").html(procedure.insemi_time);
            $("#embryo_num").html(procedure.embryo_num);
            $("#new_memo").val(procedure.memo);
            
            queryEmbryo(procedureId);
		}
	});
});

function queryEmbryo(procedureId){
    $.ajax({
		cache : false,
		type : "GET",
		url : "/api/v1/embryo/list/" + procedureId,
		data : "",
		async : false,
		error : function(request) {
			parent.layer.alert(request.responseText);
		},
		success : function(data) {
            var table = $("#embryo_table");
			for(var i=0;i<data.data.length;i++){
                table.append("<tr><td>"
                 + data.data[i].embryo_index + 
                 "</td><td><a href=\"#\" onclick=\"showIncubator()\" class=\"layui-table-link report\">"
                  + data.data[i].incubator_code +
                 "</a></td><td><a href=\"#\" onclick=\"showDish()\" class=\"layui-table-link report\">"
                  + data.data[i].dish_code 
                  + "</a></td><td><a href=\"#\" onclick=\"showEmbryo()\" class=\"layui-table-link report\">"
                   + data.data[i].cell_code + "</a></td></tr>")
            }
		}
	});
}

function showEmbryo(){
    alert("跳到胚胎视图");
}
function showDish(){
    alert("跳到皿视图");
}
function showIncubator(){
    alert("跳到培养箱视图");
}

function update(){
    var cf = confirm("是否确定修改已变更的内容?");
    if(cf){
        var mobile = $("#new_mobile").val();
        var email = $("#new_email").val();
        if(mobile == "" && email == ""){
            alert("手机号码跟邮箱不能同时为空!");
            return;
        }
        $.ajax({
            cache : false,
            type : "POST",
            url : "/api/v1/procedure/info",
            data : $('#procedureEdit').serialize(),
            async : false,
            error : function(request) {
                parent.layer.alert(request.responseText);
            },
            success : function(data) {
                alert(data);
            }
        });
    }
}