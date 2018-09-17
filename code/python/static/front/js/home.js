layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    var element = layui.element;

    $(function () {
        loadNewestCase(1,4);
        loadNewestDish(1,3);

    });
    
})

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
			if(data !== null && data.count !== null & data.count > 0){
				for (let i = 0; i < data.data.length; i++) {
                    const obj = data.data[i];
                    var dishData = obj.dishCode;
                    var dishCode = null;
                    if(dishData !== null && dishData !== ''){
                        dishCode = dishData.split(",");
                    }
					divData = divData + '<div class="layui-col-md3">'
                        + '<div class="case-list">';
                    if(dishCode !== null && dishCode.length > 0 && obj.pts > 0) {
                        divData = divData + '<div class="embryo-img">'
                        + '<img src="/api/v1/image/findImageFouce?procedureId=' + obj.id + '&dishCode=' + dishCode[0] + '" ></div>';
                    } else {
                        divData = divData + '<div class="embryo-img"><img src="/static/front/img/icon-noembryo.jpg" ></div>';
                    }
                    divData = divData + '<div class="case-info">'
                    + '<h1><span>培养箱 ' + obj.incubatorCode + ' </span>：<span>Dish #  ' + obj.dishCode + '</span></h1>'
                    + '<ul>'
                        + '<li><span style="margin-right: 20px;">'+ obj.patient_name +'</span><span>'+obj.patient_age+'岁</span></li>'
                        + '<li><span>胚胎数：</span><span>' + obj.pts + '枚</span></li>'
                        + '<li><span>阶&nbsp;&nbsp;&nbsp; 段：</span><span>'+obj.zzjd+'</span></li>'
                    + '</ul>'
                    + '</div></div></div>';
				}
			}
			$("#caseListDiv").append(divData);
        }
    });
}

function loadNewestDish(pageNo,pageSize){
    $.ajax({
        cache : false,
        type : "GET",
        url : "/api/v1/image/findNewestImageUrl",
        data : {"pageNo":pageNo,"pageSize":pageSize},
        async : false,
        error : function(request) {
            alert(request.responseText);
        },
        success : function(res) {
            var divData = "";
			if(res.code === 200 && res.data !== null && res.count !== null && res.count > 0){
                $("#incubatorSpan").html(res.data.incubatorCode);
                data = res.data.dishInfo;
				for (let i = 0; i < data.length; i++) {
                    divData = divData + '<div class="layui-col-md4" dishId=' + data[i].dishId + '><h6>Dish #' + data[i].dishCode + '</h6>'
                        + '<div class="img-list"><p>拍照时间: <span>' + data[i].imagePath + '</span>';
                    const wellUrls = data[i].wellUrls;
                    if(wellUrls !== null && wellUrls !== ""){
                        divData = divData + '总时间: <span>' + data[i].times + '</span></p>';
                        for (let j = 0; j < wellUrls.length; j++) {
                            divData = divData + '<a><img src="/api/v1/well/image?image_path=' + wellUrls[j].url + '"></a>';
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
			$("#homeImageRow").append(divData);
        }
    });
    
}