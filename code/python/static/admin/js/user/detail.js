layui.use('form', function(){
	
});

$(function(){
    var sex = $("#sex").val();
    if(sex == "1"){
        $("#man").attr("checked","checked");
    }else{
        $("#women").attr("checked","checked");
    }
    var isAdmin = $("#isAdmin").val();
    if(isAdmin == "0"){
        $("#adminno").attr("checked","checked");
    }else{
        $("#adminyes").attr("checked","checked");
    }
    var isPrivate = $("#isPrivate").val();
    if(isPrivate == "0"){
        $("#privateno").attr("checked","checked");
    }else{
        $("#privateyes").attr("checked","checked");
    }
})


