/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-9-11
 * Time: 上午11:18
 * To change this template use File | Settings | File Templates.
 */
/* 共用 js 模块 *

/* 时间插件 使用 */

          
      
(function($){
    $.setStartTime = function(){
        $('.startDate').datepicker({
            dateFormat: "yy-mm-dd",
            maxDate: "+d",
            onClose : function(dateText, inst) {
                $( "#endDate" ).datepicker( "show" );
            },
			onSelect:function(dateText, inst) {
                $( "#endDate" ).datepicker( "option","minDate",dateText );
            },
			
        });
    };
    $.setEndTime = function(){
        $(".endDate").datepicker({
            dateFormat: "yy-mm-dd",
            maxDate: "+d",
			defaultDate : new Date(),
            onClose : function(dateText, inst) {
                if (dateText < $("input[name=startDate]").val()){
                  $( "#endDate" ).datepicker( "show" );
				    alert("结束日期不能小于开始日期！");
					//$("#endDate").val(newdate)
                }
            }
        });
    };
    $.date = function(){
        $('.date').datepicker(
            $.extend({showMonthAfterYear:true}, $.datepicker.regional['zh-CN'],
                {'showAnim':'','dateFormat':'yy-mm-dd','changeMonth':'true','changeYear':'true',
                    'showButtonPanel':'true'}
            ));
    };
    $.datepickerjQ = function(){
       $(".ui-datepicker-time").on("click",function(){
           $(".ui-datepicker-css").show(300)
        });
        $(".ui-kydtype li").on("click",function(){
            $(".ui-kydtype li").removeClass("on").filter($(this)).addClass("on");
//            getAppCondtion();
        });
        $(".ui-datepicker-quick input").on("click",function(){
            var thisAlt = $(this).attr("alt");
            var dateList = timeConfig(thisAlt);
            $(".ui-datepicker-time").val(dateList);
            $(".ui-datepicker-css").hide(300);
			 $("#ui-datepicker-div").hide(300)
//            getAppCondtion()
        });
//      $(".ui-close-date").on("click",function(){
//          $(".ui-datepicker-css").css("display","none")
//			 $("#ui-datepicker-div").css("display","none")
//			//inst.dpDiv.css({"display":"none"})
//      });
		 $(".startDate").on("click",function(){
            $(".endDate").attr("disabled",false);
        });
        
        $('.ui-datepicker-css').parent().parent().siblings().on("click", function() {
		$('.ui-datepicker-css').hide(300);
	});
	
    }
	
})(jQuery);


//设置当前显示时间
$(function(){
        $.setStartTime();
        $.setEndTime();
        $.datepickerjQ();
		
        var nowDate = new Date();
        var month = nowDate.getMonth()+1;
        var day = nowDate.getDate();
        month=month<10?('0'+month):month;
        day  =day<10?('0'+day):day;
        
        timeStr = nowDate.getFullYear() + '-'+ month + '-' + day;
        nowDate.setDate(nowDate.getDate()+parseInt(0));
        
        var month = nowDate.getMonth();
        var day = nowDate.getDate();
        month=month<10?('0'+month):month;
        day  =day<10?('0'+day):day;
        
        var endDateStr = nowDate.getFullYear() + '-'+ month + '-' + day;
		$(".ui-datepicker-time").attr("value",endDateStr +"~"+ timeStr)
		$("#startDate").attr("value",endDateStr)
		$("#endDate").attr("value",timeStr)
    });


    function timeConfig(time){
		//快捷菜单的控制
        var nowDate = new Date();
        var month = nowDate.getMonth()+1;
        var day = nowDate.getDate();
        month=month<10?('0'+month):month;
        day  =day<10?('0'+day):day;
       
//      timeStr = '一' + nowDate.getFullYear() + '-' + (month<10?month01:month) + '-' + (date<10?date01:date);
        timeStr = '~' + nowDate.getFullYear() + '-'+ month + '-' + day;
        nowDate.setDate(nowDate.getDate()+parseInt(time));
        var month = nowDate.getMonth()+1;
        var day = nowDate.getDate();
        month=month<10?('0'+month):month;
        day  =day<10?('0'+day):day;
        var endDateStr = nowDate.getFullYear() + '-'+ month + '-' + day;
//      var endDateStr = nowDate.getFullYear() + '-'+  (nowDate.getMonth()+1) + '-' + nowDate.getDate();
        if(time == -1){
            endDateStr += '~' + endDateStr;
        }else{
            endDateStr += timeStr;
        }
        return endDateStr;
    }

    function datePickers(){
		//自定义菜单
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();
        var dateList = startDate +'~'+ endDate;
        $(".ui-datepicker-time").val(dateList);
        $(".ui-datepicker-css").hide(300);
//        getAppCondtion()
    }