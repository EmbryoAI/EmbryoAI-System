layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {
        //上一张 下一张
        var n = 0;
        $(".dishimg li img").hide();
        $(".dishimg li img:first").show();
        // 上一张
        $(".pre-frame").click(function () {
            if (n > 0) {
                n = n - 1;
            } else {
                n < $(".dishimg li img").length - 1;
                layer.msg("已经是第一张了")
            }
            $(".dishimg li img").hide();
            $(".dishimg li img:eq(" + n + ")").show();
        });
        // 下一张
        $(".next-frame").click(function () {
            if (n < $(".dishimg li img").length - 1) {
                n = n + 1;

            } else {
                n = $(".dishimg li img").length - 1;
                layer.msg("已经是最后一张了")
            }
            $(".dishimg li img").hide();
            $(".dishimg li img:eq(" + n + ")").show();
        })

        // 滚动效果
        var textTime;
        var imgTime;
        // 点击播放暂停
        $('#playBtn').click(function () {
            if ($(this).hasClass('play')) {
                $(this).removeClass('play');
                $(this).addClass('stop');
                $(this).children("span").text("暂停");

                function showText() {
                    n = n + 1;
                }
                textTime = setInterval(showText, 200);

                function run() {
                    if (n < $(".dishimg li img").length) {
                        n = n;
                    } else {
                        n = 0
                    }
                    $(".dishimg li img").hide();
                    $(".dishimg li img:eq(" + n + ")").show();
                }
                imgTime = setInterval(run, 200);

            } else {
                $(this).removeClass('stop');
                $(this).addClass('play');
                $(this).children("span").text("播放");
                clearInterval(textTime);
                clearInterval(imgTime);
            }
        })
		
		// 胚胎评分表
		 $('.em-grade').on('click', function(){
			layer.open({
			  type: 2,
			  title: '胚胎评分表',
			  maxmin: true,
			  shadeClose: true, 
			  area : ['900px' , '220px'],
			  content: 'emGrade.html'
			});
		  });
		  
		// 胚胎总览表
		 $('.em-all').on('click', function(){
			layer.open({
			  type: 2,
			  title: '胚胎总览表',
			  maxmin: true,
			  shadeClose: true, 
			  area : ['900px' , '520px'],
			  content: 'emAll.html'
			});
		  });
		// 选择基准胚胎
		$('.tool-end li').click(function () {
			const self = $(this);
			const index = $(this).attr('data-end');
			if (self.hasClass('active')) {
				self.removeClass('active');
				$('.dish-box').css("cursor","auto")
			}else{
				$(".tool-end li").removeClass('active');
				self.addClass('active');
				$('.dish-box').css("cursor", "url('img/cursor"+index+".png'),auto");
			}
		})
		
		$('.dishimg li').click(function(){
			const  self = $(this),
				calssName = self.children('i').attr('class'),
			standard = $('.standard').hasClass('active'),	
			    appendStan = "<span class='standard'></span>" ,
				
				transplant = $('.transplant').hasClass('active'),
			    appendTran = "<i class='transplant'></i>",
				
				  freeze = $('.freeze').hasClass('active'),	
			    appendFreeze = "<i class='freeze'></i>" ,
				
				abandon = $('.abandon').hasClass('active'),
				appendAband = "<i class='abandon'></i>",
				
			  hold = $('.hold').hasClass('active'),
			  appendHold = "<i class='hold'></i>";
			if(standard){
				$('.dishimg li').removeClass('active');
				$('.dishimg li span').remove('.standard');
				self.addClass('active');
				self.append(appendStan)
			}else if(transplant){
				if(calssName=="transplant"){
					self.children('i').remove();
				}else{
					self.children('i').remove();
					self.append(appendTran)
				}
			}else if(freeze){
				if(calssName=="freeze"){
					self.children('i').remove();
				}else{
				self.children('i').remove();
				self.append(appendFreeze)
				}
			}else if(abandon){
				if(calssName=="abandon"){
					self.children('i').remove();
				}else{
				self.children('i').remove();
				self.append(appendAband)
				}
			}else if(hold){
				if(calssName=="hold"){
					self.children('i').remove();
				}else{
				self.children('i').remove();
				self.append(appendHold)
				}
			}else{
				return false
			}
		})
		
		$('#cancelEnd').click(function(){
			$(".tool-end li").removeClass('active');
			$('.dish-box').css("cursor","auto")

		})
    });
})
