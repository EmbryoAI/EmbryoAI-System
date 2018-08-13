layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
	var laydate = layui.laydate;
	// 培养皿选择
	$('.incubator').on('click','span',function(){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		}else{
			$(this).siblings('span').removeClass('active');
			$(this).addClass('active');
		}
	})
	
	// 查看病历
	$('.patient-info').hover(function(){
		const txt ="无";
		const div = "<div class='case-details'><dl><dt><strong>姓名</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>授精时间</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>首次拍照时间</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>年龄</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>授精方式</strong><span>"+txt+"</span></dt>"+
		"<dt><strong>阶段</strong><span>"+txt+"</span></dt>"+"</dl></div>";
		$(this).append(div)
	},function(){
		$(this).children('div').remove()
	})
})
