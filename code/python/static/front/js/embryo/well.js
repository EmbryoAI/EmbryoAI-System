$(function(){
    var procedureId = $("#procedureId").val();
    var dishId = $("#dishId").val();
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
            querySeriesList(data[0]);
        }
    });
});

function querySeriesList(well_id){
    var procedureId = $("#procedureId").val();
    var dishId = $("#dishId").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/dish/list?procedure_id=" + procedureId + "&dish_id=" + dishId + "&well_id=" + well_id,
        data : "",
        async : false,
        error : function(request) {
            parent.layer.alert(request.responseText);
        },
        success : function(data) {
            var seris = "";
            for(var i=0;i<data.length;i=i+3){
                seris = seris + "<li class=\"active\"><a href=\"#\">" + 
                                "<img src=\"/api/v1/well/image?image_path=" + data[i+1] + 
                                "\"><span>" + data[i+2] + "</span></a></li>";
            }
            $("#myscrollboxul").html(seris);
        }
    });
}