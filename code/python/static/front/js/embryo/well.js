$(function(){
    var procedureId = $("#procedureId").val();
    var dishCode = $("#dishCode").val();
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/well/list/" + procedureId + "/" + dishCode,
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
                    "</span><img src=\"/api/v1/well/image?image_path=" + data[i+1] + "\" onclick=\"querySeriesList()\"><i></i></li>";
                }else{
                    well = well + "<li><span>well" + data[i] + 
                    "</span><img src=\"/api/v1/well/image?image_path=" + data[i+1] + "\" onclick=\"querySeriesList()\"><i></i></li>";
                }
            }
            $("#siteitem").html(well);
        }
    });
});