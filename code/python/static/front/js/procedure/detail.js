layui.use('form', function(){
	var layer = layui.layer;
});

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
                 "</td><td><a href=\"#\" onclick=\"showIncubator()\" class=\"layui-table-link\">"
                  + data.data[i].incubator_code +
                 "</a></td><td><a href=\"#\" onclick=\"showDish()\" class=\"layui-table-link\">"
                  + data.data[i].dish_code 
                  + "</a></td><td><a href=\"/front/embryo?procedureId=" + procedureId + "&dishId=" + 
                  data.data[i].dish_id + "&embryoId=" + data.data[i].id + 
                  "\" target=\"_blank\" class=\"layui-table-link\">"
                  + data.data[i].cell_code + "</a></td></tr>")
            }
		}
	});
}

function showDish(){
    alert("跳到皿视图");
}
function showIncubator(){
    alert("跳到培养箱视图");
}

function update(){
    var mobile = $("#new_mobile").val();
    var email = $("#new_email").val();
    if(mobile == "" && email == ""){
        parent.layer.alert("手机号码跟邮箱不能同时为空!");
        return;
    }

    if(mobile != ""){
        //手机号正则  
        var phoneReg = /(^1[3|4|5|7|8]\d{9}$)|(^09\d{8}$)/;  
        //电话  
        var phone = $.trim(mobile);  
        if (!phoneReg.test(phone)) {  
            parent.layer.alert('请输入有效的手机号码！'); 
            return false;  
        }  
    }

    if(email != ""){
        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); 
        var emailStr = $.trim(email);  
        if (!reg.test(emailStr)) {  
            parent.layer.alert('请输入有效的电子邮箱！');  
            return false;  
        }  
    }
    layer.confirm('是否确定修改已变更的内容？', function(index){
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
                parent.layer.alert(data);
                var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
			    parent.layer.close(index);
            }
        });
    });
}