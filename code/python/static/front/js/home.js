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

