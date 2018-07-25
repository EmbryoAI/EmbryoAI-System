var procedureId = "";
var dishId = "";
var wellId = "";

$(function(){
    procedureId = $("#procedureId").val();
    dishId = $("#dishId").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/list/" + procedureId + "/" + dishId,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var well = "";
            for(var i=0;i<data.length;i=i+2){
                if(i == 0){
                    well = well + "<li class=\"active\"><span>well" + data[i] + 
                    "</span><img src=\"/api/v1/well/image?image_path=" + data[i+1] +
                     "\" onclick=\"querySeriesList('" + data[i] + "')\"><i></i></li>";
                }else{
                    well = well + "<li><span>well" + data[i] + 
                    "</span><img src=\"/api/v1/well/image?image_path=" + data[i+1] +
                     "\" onclick=\"querySeriesList('" + data[i] + "')\"><i></i></li>";
                }
            }
            $("#siteitem").html(well);
            wellId = data[0];
            querySeriesList(wellId);
        }
    });
});

function querySeriesList(wellId){
    var procedureId = $("#procedureId").val();
    var dishId = $("#dishId").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/list?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" + wellId,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var seris = "";
            for(var i=0;i<data.length;i=i+3){
                if(i == data.length-3){
                    seris = seris + "<li class=\"active\"><a href=\"#\">" + 
                                    "<img src=\"/api/v1/well/image?image_path=" + data[i+1] + 
                                    "\" onclick=\"getBigImage('" + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\">" +
                                    "<span>" + data[i+2] + "</span></a></li>";
                }else{
                    seris = seris + "<li><a href=\"#\">" + 
                                    "<img src=\"/api/v1/well/image?image_path=" + data[i+1] + 
                                    "\" onclick=\"getBigImage('" + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\">" +
                                    "<span>" + data[i+2] + "</span></a></li>";
                }
            }
            $("#myscrollboxul").html(seris);
        }
    });
}

function getBigImage(procedureId, dishId, wellId, seris){
    alert("传入周期ID:" + procedureId + ",皿ID:" + dishId + 
            ",孔ID:" + wellId + ",时间序列:" + seris + ",调用小妹妹的方法获取大图");
}

function preFrame(){
    var currentSeris = "5171500";
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/preframe?current_seris=" + currentSeris,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            getBigImage(procedureId, dishId, wellId, data);
        }
    });
}

function nextFrame(){
    var currentSeris = "5171500";
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/nextframe?current_seris=" + currentSeris,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            getBigImage(procedureId, dishId, wellId, data);
        }
    });
}