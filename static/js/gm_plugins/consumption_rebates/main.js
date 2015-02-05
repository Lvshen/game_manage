$(document).ready(function(){
	if(current_page != "gm_form"){
		return;
	}
	
	var submit_btn = $('[type="submit"]');
	submit_btn.unbind('click');
	submit_btn.removeAttr('onclick');
	
	var begin_time = $('[field_key="aot"]').val();
	var end_time = $('[field_key="act"]').val();
	var acst = $('[field_key="acst"]').val(); 
	var now_time = new Date();
	
	var y = now_time.getFullYear();
	var m = now_time.getMonth() + 1;
	var d = now_time.getDate();
	var h = now_time.getHours();
	var i = now_time.getMinutes();
	var s = now_time.getSeconds();
	
	now_time = now_time_str;
	if (begin_time == '1970-01-01 08:00:00'){
		var target = $('[field_key="aot"]');
		target.val(now_time);
		target.attr('name', target.attr('field_key'));
	}
	
	if(end_time == '1970-01-01 08:00:00'){
		var target = $('[field_key="act"]');
		target.val(now_time);
		target.attr('name', target.attr('field_key'));
	}
	
	if(acst == '1970-01-01 08:00:00'){
		var target = $('[field_key="acst"]');
		target.val(now_time);
		target.attr('name', target.attr('field_key'));
	}
	
	submit_btn.bind('click', function(e){
		
		var msg = [];
		
		var begin_time = $('[field_key="aot"]').val();
		var end_time = $('[field_key="act"]').val();
		var acst = $('[field_key="acst"]').val(); 
		var air = $('[field_key="air"]').val();//每次可领奖励
		var ain = $('[field_key="ain"]').val();//可领次数
		var acn = $('[field_key="acn"]').val();//累计充值条件
		
		
		var now_time = now_time_str;
		
		var aet = new Date(Date.parse(field_key_dic['aet'].replace(/-/g,"/")));
		var is_new_cfg = false;
		
		if(aet.getFullYear() == 1970){
			is_new_cfg = true;
		}
		
		
		if(now_time > field_key_dic['act'] && !is_new_cfg){//如果活动已经过期则不能设置
			msg.push('该活动已结束，不可再更改');
		}else{
			/* 在新配置时候*/
			if(now_time > begin_time && is_new_cfg){
				msg.push("<开始时间>不可早于当前时间");
			}
			
			/*新配置END*/
			
			if(begin_time != field_key_dic['aot'] && !is_new_cfg){
				msg.push("活动已开始<开始时间>不能修改");
			}
			
			if(begin_time > end_time){
				msg.push('<活动开始时间>不能晚于<结束时间>');
			}
			
			if(now_time > end_time){
				msg.push("<活动结束时间>不能早于当前时间");
			}
			
			if(acst >= end_time){
				msg.push('<充值结束时间>不能晚于、等于<活动结束时间>');
			}
			
			air = parseInt(air);
			if(isNaN(air)){
				msg.push('<每次可领奖励>只能输入整数');
			}
			ain = parseInt(ain);
			if(isNaN(ain)){
				msg.push('<可领次数>只能输入整数');
			}else{
				var now_tmp = new Date(Date.parse(now_time.replace(/-/g,"/")));//当前
				
				try{
					if(DateDiff(end_time, acst) < ain){//充值结束 日期//活动结束
						msg.push('活动结束时间和充值结束时间的相差天数不能小于<可领取次数>');
					}
				}catch(ex){
					
				}
				
			}
			acn = parseInt(acn);
			if(isNaN(acn)){
				msg.push('<累计充值条件>只能整数');
			}
		}
		
		var target = $("#gm_form");
		var feedback = target.find(".feedback");
		if(feedback.length){
			feedback.html('');
		}
		if(msg.length != 0){
			var len = msg.length;
			if(!feedback.length){
				feedback = $("<div class='feedback'></div>");
			}
			while(len){
				len--;
				var str = '<p  ><h2 style="color:red;" >' + msg[len] + '</h2></p>';
				feedback.append(str);
			}
			target.append(feedback);
			e.preventDefault();
			return false;
		}
		success_msg = '<p style="color:red;" >保存成功，请勿在当前页面再次修改配置信息。</p><p>正确的做法是：退出当前页面，重新进入此项后台进行修改。</p>';
		return loopComit();
		
	});
	
});
