layui.use(['form', 'jquery', 'laydate', 'table', 'layer'], function () {
    var form = layui.form;
    var $ = layui.jquery;
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;

    $(function () {
        // 点击播放暂停
//         $('#playBtn').click(function () {
// 					var oVideo = document.getElementsByClassName('videoSource');
// 					var i;
//             if ($(this).hasClass('play')) {
//                 $(this).removeClass('play');
//                 $(this).addClass('stop');
//                 $(this).children("span").text("暂停");
// 								for (i = 0; i < oVideo.length; i++) {
// 									oVideo[i].play();
// 								}
//             } else {
//                 $(this).removeClass('stop');
//                 $(this).addClass('play');
//                 $(this).children("span").text("播放");
// 								for (i = 0; i < oVideo.length; i++) {
// 									oVideo[i].pause();
// 								}
//             }
//         })
		
			var n = 0;
			var imgLen = $('.active img').length  // 已基准孔的图片张数为标准
			var all = $(".dishbox1 img,.dishbox2 img,.dishbox3 img,.dishbox4 img,.dishbox5 img,.dishbox6 img,.dishbox7 img,.dishbox8 img,.dishbox9 img,.dishbox10 img,.dishbox11 img,.dishbox12 img")
				// 上一张
        $(".pre-frame").click(function () {
            if (n > 0) {
                n = n - 1;
            } else {
                n < imgLen - 1;
                layer.msg("已经是第一张了")
            }
            all.hide();
            $(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();

        });
        // 下一张
        $(".next-frame").click(function () {
            if (n < imgLen - 1) {
                n = n + 1;

            } else {
                n = imgLen - 1;
                layer.msg("已经是最后一张了")
            }
            all.hide();
            $(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();

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
                    if (n < imgLen) {
                        n = n;
                    } else {
                        n = 0
                    }
                    all.hide();
                    $(".dishbox1 img:eq(" + n + "),.dishbox2 img:eq(" + n + "),.dishbox3 img:eq(" + n + "),.dishbox4 img:eq(" + n + "),.dishbox5 img:eq(" + n + "),.dishbox6 img:eq(" + n + "),.dishbox7 img:eq(" + n + "),.dishbox8 img:eq(" + n + "),.dishbox9 img:eq(" + n + "),.dishbox10 img:eq(" + n + "),.dishbox11 img:eq(" + n + "),.dishbox12 img:eq(" + n + ")").show();
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
		
		// 时间轴
		$('.time-page').on('click','i',function(){
				$(this).siblings('i').removeClass('active');
				$(this).addClass('active');
		})
		$('.time-list span').hover(function(){
				const that = this;
				const text = $(this).find("i").text();
				layer.tips(text, that,{tips: [1]}); 
		})
		$('.time-list').on('click','span',function(){
				$(this).siblings('span').removeClass('active');
				$(this).addClass('active');
		})
})
