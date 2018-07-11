var form;
layui.use('form', function(){
	form = layui.form;
	var biochem_pregnancy = $('#biochemPregnancy').val();
	if(biochem_pregnancy != '' && biochem_pregnancy != 'None' && biochem_pregnancy != 0){
		$("#biochem_pregnancy").attr("checked", "checked");
		form.render("checkbox");
		$('#second_div').show();
	}
	var clinical_pregnancy = $('#clinicalPregnancy').val();
	if(clinical_pregnancy != '' && clinical_pregnancy != 'None' && clinical_pregnancy != 0){
		$("#clinical_pregnancy").attr("checked", "checked");
		form.render("checkbox");
		$('#third_div').show();
	}
	var fetus_count = $('#fetusCount').val();
	if(fetus_count != '' && fetus_count != 'None'){
		$('#fetus_count_' + fetus_count).attr("checked", "checked");
		form.render('radio');
	}
});


function showNext(index){
	if(index == 1){
		
		$("#biochem_pregnancy :checkbox").prop("checked", "checked");
		
		form.render('checkbox');
		var node=$('#second_div');
		if(node.is(':hidden')){
			node.show();
		}else{
			$('#clinical_pregnancy').removeAttr('checked');
			form.render('checkbox');
			node.hide();
			$('input:radio[name="fetus_count"]').removeAttr('checked');
			form.render('radio');
			$('#third_div').hide();
		}
	}
	if(index == 2){
		$('#clinical_pregnancy').attr('checked', "checked");
		form.render('checkbox');
		var node=$('#third_div');
		if(node.is(':hidden')){
			node.show();
		}else{
			$('input:radio[name="fetus_count"]').removeAttr('checked');
			form.render('radio');
			node.hide();
			
		}
	}
}

function choseRadio(index){
	$('#fetus_count_' + index).attr('checked', "checked");
	form.render('radio');
}

function save() {
	var biochem_pregnancy = $("#biochem_pregnancy").is(":checked");
	if(biochem_pregnancy == true){
		biochem_pregnancy = 1;
	}else{
		biochem_pregnancy = 0;
	}
	var clinical_pregnancy = $("#clinical_pregnancy").is(":checked");
	if(clinical_pregnancy == true){
		clinical_pregnancy = 1;
	}else{
		clinical_pregnancy = 0;
	}
	var fetus_count = $('input:radio:checked').val();
	if(fetus_count == undefined){
		fetus_count = 0;
	}
	var user_id = $('#userId').val();
	var procedureId = $('#procedureId').val();

	layer.confirm('是否确定提交？', function(index){
		$.ajax({
			cache : false,
			type : "POST",
			url : "/api/v1/feedback/",
			data: JSON.stringify({                  
                biochem_pregnancy: biochem_pregnancy,
				clinical_pregnancy: clinical_pregnancy,
				fetus_count: fetus_count,
				user_id: user_id,
				procedure_id: procedureId
            }),
            contentType: "application/json; charset=utf-8",
			error : function(request) {
				parent.layer.alert(request.responseText);
			},
			success : function(data) {
				parent.layer.alert("病历回访数据保存成功!");
				var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
				parent.layer.close(index);
			}
		});
	});
}


