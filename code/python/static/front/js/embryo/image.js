var form = null;
//最清晰的jpg
var sharpJpg = null;
//最清晰的jpg对应的z轴位置
var sharpZIndex = null;
//z轴总数
var zIndexLength = 0;
//采集时间
var acquisitionTime = null;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

//    $(function () {
//        var procedureId = $("#procedureId").val();
//        var dishId = $("#dishId").val();
//        var wellId = 1;
//        var timeSeries = '0000000';
//        var zIndex = '';
//        loadingImage(procedureId,dishId,wellId,timeSeries,zIndex)
//        loadingZIndex(procedureId,dishId,wellId,timeSeries)
//
//    });
});

function loadingZIndex(procedureId,dishId,wellId,timeSeries){

    //加载z轴所以节点，并渲染
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/image/findAllZIndex",
        data : {"procedureId":procedureId,"dishId":dishId,"wellId":wellId,"timeSeries":timeSeries},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
            var zLi = "";
            if(data.code == 200 && data.data != null){
                var i = data.data.fileStart;
                var length = data.data.fileEnd;
                acquisitionTime = data.data.imagePath;
                sharpJpg = data.data.sharp;
                zData = data.data.zIndexFiles;
                zIndexLength = zData.length;
                for (;i < length; i++) {
                    if(sharpJpg == zData[i]) {
                        sharpZIndex = i;
                        zLi = "<li class='active' onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zIndex=" + i + " zJpg='" + zData[i] + "'><b></b></li>" + zLi;
                    } else {
                        zLi = "<li onclick=checkZIndex('"+ procedureId +"','"+ dishId +"','"+ wellId +"','"+ timeSeries +"','" + i + "') zIndex=" + i + " zJpg='" + zData[i] + "'><b></b></li>" + zLi;
                    }
                }
                $("#zIndex").html(zLi);
                ini(acquisitionTime,data.data.path,sharpJpg)
            }
        }
    });
    
    $('#zIndexDiv').bind('mousewheel', function(event, delta) {
        var zIndex = $(".time-vertical .active").attr('zIndex');
        var length = $(".time-vertical li").length;
        if(delta > 0){
            zIndex = parseInt(zIndex) + 1;
            if(zIndex > length){
                zIndex = 1;
            }
        } else {
            zIndex = parseInt(zIndex) - 1;
            if(zIndex < 1){
                zIndex = length;
            }
        }
        $('.time-vertical li').removeClass('active');
        $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
        loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
        return false;    
    });
    
}

function checkZIndex(procedureId,dishId,wellId,timeSeries,zIndex){
    $('.time-vertical li').removeClass('active');
    $('.time-vertical li[zIndex='+zIndex+']').addClass('active');
    loadingImage(procedureId,dishId,wellId,timeSeries,zIndex);
}

function loadingImage(procedureId,dishId,wellId,timeSeries,zIndex){
    var imgUrl = "/api/v1/image/findImage?procedureId="+ procedureId +"&dishId="+ dishId +"&wellId="+ wellId +"&timeSeries="+ timeSeries +"&zIndex=" + zIndex; 
    var img = "<img src=" + imgUrl + ">";
    $("#imgDiv").html(img);
    if(zIndex == null || zIndex == '' || sharpZIndex == zIndex){
        // alert(111111111111);
        $("#distinct").attr("checked",true);
//        form.render("checkbox");
    } else {
        // alert(222222222222);
        // $("#distinct").attr("checked",false);
        $("#distinct").removeAttr('checked')
//        form.render("checkbox");
    }
    
}