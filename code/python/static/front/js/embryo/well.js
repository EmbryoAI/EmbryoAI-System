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
                        "\" onclick=\"querySeriesList('" + i + "','lastEmbryoSerie')\"><i></i></li>";
                    }else{
                        well = well + "<li><span>well" + i + 
                        "</span><img src=\"/api/v1/well/image?image_path=" + result +
                        "\" onclick=\"querySeriesList('" + i + "','lastEmbryoSerie')\"><i></i></li>";
                    }
                }else{
                    well = well + "<li><span>well" + i + 
                    "</span><img src=\"/static/front/img/icon-wellnone.jpg\"><i></i></li>";
                }
            }
            $("#siteitem").html(well);
            wellId = data[0];
            querySeriesList(wellId,'lastEmbryoSerie');
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

function querySeriesList(wellId, seris){
    var procedureId = $("#procedureId").val();
    var dishId = $("#dishId").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/list?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" + wellId + "&seris=" + seris,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var seris = "";
            for(var i=0;i<data.length;i=i+4){
                var imagePath = "/api/v1/well/image?image_path=" + data[i+1];
                if(data[i+1].indexOf("embryo_not_found") != -1){
                    imagePath = "/static/front/img/icon-noembryo.jpg";
                }
                var active = "<div class=\"swiper-slide\">";
                if(i == 16){
                    active = "<div class=\"swiper-slide active\">";
                }
                seris = seris + active + "<span><img src=\"" + 
                                    imagePath +"\" onclick=\"getBigImage('" 
                                    + procedureId + "','" + dishId + 
                                    "','" + wellId + "','" + data[i] + "')\"><b>" + 
                                    data[i+2] + "</b></div>";
            }
            $("#myscrollboxul").html(seris);
            lastSeris = data[data.length-1];
        }
    });
}

function getBigImage(procedureId, dishId, wellId, seris){
    querySeriesList(wellId, seris);
    
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