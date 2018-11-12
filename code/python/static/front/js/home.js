// var layer = null;
layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    var element = layui.element;

    $(function () {
        loadNewestCase(1,4);
        loadNewestDish();

        $(window).resize(function () {
            nolist();
        });

        });
})

    //培养箱空白填充自适应
    function nolist(){
        var marginT = $(".layui-col-md4 h6").height()+8;
        var listH = $(".img-list").height()-20;
        console.log(marginT,listH);
        // $(".no-list").css("margin-top",marginT+'px');
        $(".no-list").css("height",listH);
        $(".no-list").css("line-height",listH-marginT+'px');
    }

function loadNewestCase(pageNo,pageSize){
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/procedure/list",
        data : {"page":pageNo,"limit":pageSize},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(data) {
            var divData = "";
            var dataCount = 0;
			if(data !== null && data.count !== null & data.count > 0){
                dataCount = data.data.length;
				for (let i = 0; i < data.data.length; i++) {
                    const obj = data.data[i];
                    var dishDiv = "";
                    var dishCodeArr = null;
                    var dishIdArr = null;
                    if(obj.dishCode !== null && obj.dishCode !== ''){
                        dishIdArr = obj.xst.split(",");
                        dishCodeArr = obj.dishCode.split(",");
                        for (let j = 0; j < dishIdArr.length; j++) {
                            if(j > 0){
                                dishDiv = dishDiv + ',';
                            }
                            dishDiv = dishDiv + '<a href="/front/dish?procedureId='+ obj.id +'&dishId=' + dishIdArr[j] + '&dishCode=' +dishCodeArr[j]+'" target="_blank"><span>Dish #  ' + dishCodeArr[j] + '</span></a>';
                        }
                    }
					divData = divData + '<div class="layui-col-md3">'
                        + '<div class="case-list">';
                    if(dishCodeArr !== null && dishCodeArr.length > 0 && obj.pts > 0) {
                        divData = divData + '<div class="embryo-img" onclick=lookCase("'+ obj.id +'") title="查看病历详情">'
                        + '<img src="/api/v1/image/findImageFouce?procedureId=' + obj.id + '&dishCode=' + dishCodeArr[0] + '" ></div>';
                    } else {
                        divData = divData + '<div class="embryo-img" onclick=lookCase("'+ obj.id +'")><img src="/static/front/img/icon-noembryo.jpg" ></div>';
                    }
                    divData = divData + '<div class="case-info">'
                    + '<h1><a href="/front/incubator?procedureId=' + obj.id + '&incubatorId=' + obj.incubatorCode + '" target="_blank"><span>培养箱 ' + obj.incubatorCode + '</span></a>：' + dishDiv 
                    + '</h1><ul>'
                        + '<li><span style="margin-right: 20px;">'+ obj.patient_name +'</span><span>'+obj.patient_age+'岁</span></li>'
                        + '<li><span>胚胎数：</span><span>' + obj.pts + '枚</span></li>'
                        + '<li><span>阶&nbsp;&nbsp;&nbsp; 段：</span><span>'+obj.zzjd+'</span></li>'
                    + '</ul>'
                    + '</div></div></div>';
                    //
                }
            }
            if(dataCount < 4){
                for (let i = dataCount; i < 4; i++) {
                    divData = divData + '<div class="layui-col-md3"><div class="no-case"><h1>无病历</h1></div></div>';
                }
            }
			$("#caseListDiv").append(divData);
        }
    });
}

function lookCase(procedureId){
	layer.open({
		title : "病历详情",
		type : 2,
		area : [ '760px', '650px' ],
		maxmin : true,

		shadeClose : false,
		content : '/front/procedure/' + procedureId
	});
}

function loadNewestDish(){
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/image/findNewestImageUrl",
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(res) {
            var divData = "";
            var dataCount = 0;
			if(res.code === 200 && res.data !== null && res.count !== null && res.count > 0){
               // $("#incubatorSpan").html(res.data.incubatorCode);
                data = res.data.dishInfo;
                dataCount = data.length;
				for (let i = 0; i < data.length; i++) {
                    // divData = divData + '<h1 class="incbt-title">@培养箱 <span>'+ data[i].incubatorCode +'</span></h1>';
                    divData = divData + '<div class="layui-col-md4" dishId=' + data[i].dishId + '><h1 class="incbt-title">@培养箱 <span>'+ data[i].incubatorCode +'</span></h1><h6>Dish #' + data[i].dishCode + '</h6>'
                        + '<div class="img-list"><p>拍照时间: <span>' + data[i].imagePathShow + '</span>';
                    const wellUrls = data[i].wellUrls;
                    if(wellUrls !== null && wellUrls !== ""){
                        divData = divData + '总时间: <span>' + data[i].times + '</span></p>';
                        for (let j = 0; j < wellUrls.length; j++) {
                            divData = divData + '<a href="/front/embryo/toEmbryo?imagePath=' + data[i].imagePath + '&dishId=' + data[i].dishId + '&wellCode=' + wellUrls[j].wellId + '&dishCode=' + data[i].dishCode + '" target="_blank"><img src="' + wellUrls[j].url + '"></a>';
                        }
                        if(wellUrls.length < 12){
                            for (let j = wellUrls.length; j < 12; j++) {
                                divData = divData + '<a><img src="/static/front/img/icon-noembryo.jpg" ></a>';
                            }
                        }
                    } else {
                        divData = divData + '总时间: <span></span></p>';
                        for (let j = 0; j < 12; j++) {
                            divData = divData + '<a><img src="/static/front/img/icon-noembryo.jpg" ></a>';
                        }
                    }
                    divData = divData + '<div class="clear"></div></div></div>';
                }
            }
            if(dataCount < 3){
                for (let i = dataCount; i < 3; i++) {
                    divData = divData + '<div class="layui-col-md4"><h1 class="incbt-title">@培养箱 <span></span></h1><h6>Dish # </h6><div class="no-list"><img src="/static/front/img/hnoimg.png" alt=""></div></div>';
                }
            }
            $("#homeImageRow").append(divData);
            nolist();
        }
    });
    
}
