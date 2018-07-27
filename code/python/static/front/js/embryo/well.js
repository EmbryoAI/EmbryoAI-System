var procedureId = "";
var dishId = "";
var wellId = "";
var lastSeris = "";

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
            for(var i=1;i<=12;i++){
                var result = check(i, data);
                if(result != ''){
                    if(i == data[0]){
                        well = well + "<li class=\"active\"><span>well" + i + 
                        "</span><img src=\"/api/v1/well/image?image_path=" + result +
                        "\" onclick=\"querySeriesList('" + i + "')\"><i></i></li>";
                    }else{
                        well = well + "<li><span>well" + i + 
                        "</span><img src=\"/api/v1/well/image?image_path=" + result +
                        "\" onclick=\"querySeriesList('" + i + "')\"><i></i></li>";
                    }
                }else{
                    well = well + "<li><span>well" + i + 
                    "</span><img src=\"/static/front/img/icon-wellnone.jpg\"><i></i></li>";
                }
            }
            $("#siteitem").html(well);
            wellId = data[0];
            querySeriesList(wellId);
        }
    });
});

function check(index, data){
    var result = '';
    for(var i=0;i<data.length;i=i+2){
        if(index == data[i]){
            result = data[i+1];
        }
    }
    return result;
}

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
                var imagePath = "/api/v1/well/image?image_path=" + data[i+1];
                if(imagePath.indexOf("embryo_not_found") != -1){
                    imagePath = "/static/front/img/icon-noembryo.jpg";
                }
                if(i == data.length-3){
                    seris = seris + "<li class=\"active\"><a href=\"#\">" + 
                                    "<img src=\"" + imagePath +"\" onclick=\"getBigImage('" 
                                    + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\">" +
                                    "<span>" + data[i+2] + "</span></a></li>";
                }else{
                    seris = seris + "<li><a href=\"#\">" + 
                                    "<img src=\"" + imagePath + "\" onclick=\"getBigImage('" 
                                    + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\">" +
                                    "<span>" + data[i+2] + "</span></a></li>";
                }
            }
            $("#myscrollboxul").html(seris);
            lastSeris = data[data.length-3];
        }
    });
}

function getBigImage(procedureId, dishId, wellId, seris){
    alert("传入周期ID:" + procedureId + ",皿ID:" + dishId + 
            ",孔ID:" + wellId + ",时间序列:" + seris + ",调用小妹妹的方法获取大图");
}

function preFrame(){
    var currentSeris = "5171500";
    if(currentSeris == "0000000"){
        parent.layer.alert("已经是第一张了!");
        return;
    }
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
    if(parseInt(currentSeris) >= parseInt(lastSeris)){
        parent.layer.alert("已经是最后一张了!");
        return;
    }
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

$(document).keydown(function(event){
    if(event.which == "37"){
        preFrame();
    }
    if(event.which == "39"){
        nextFrame();
    }
});