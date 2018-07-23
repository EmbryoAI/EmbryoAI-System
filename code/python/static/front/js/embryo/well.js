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
            for(var i=0;i<data.length;i++){
                if(i == 0){
                    well = well + "<li class=\"active\"><span>well" + data[i] + 
                    "</span><img src=\"d:/EmbryoAI-System/code/captures/20180422152100/DISH8/focus/01_0000000_focus.jpg\" onclick=\"querySeriesList()\"><i></i></li>";
                }else{
                    well = well + "<li><span>well" + data[i] + 
                    "</span><img src=\"/focus\01_0000000_focus.jpg\" onclick=\"querySeriesList()\"><i></i></li>";
                }
            }
            $("#siteitem").html(well);
        }
    });
});