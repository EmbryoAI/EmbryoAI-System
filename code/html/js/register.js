layui.use(['form', 'jquery', 'laydate', 'table', 'layer', 'element','address'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;
	var laydate = layui.laydate;
	var address = layui.address();
	$(function(){	
			//自定义验证规则例子
		form.verify({
		card: function(value){
			if(value.length != 18){
			return '身份证号长度应为18位';
			}
		}    
		});
		//第一页的确定按钮
		$("#btn_part1").click(function(){			
			// if(!verifyCheck._click()) return;
			$("#part1").hide();
			$("#part2").show();
			$(".step li").eq(1).addClass("on");
		});
		//第二页的确定按钮
		$("#btn_part2").click(function(){			
			$("#part2").hide();
			$("#part3").show();	
			$(".step li").eq(2).addClass("on");
		});	
		//第三页的确定按钮
		$("#btn_part3").click(function(){			
			$("#part3").hide();
			$("#part4").show();	
		});	
	});
  
  	
})
