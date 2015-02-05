/*
 * 链接的href和表单的action为请求地址
 * todo 完成后执行方法
 * goto 完成后跳转页面
 * 
 * 
 */

(function($) {
	var ajax_do = function(obj){
		var go_url = $(obj).attr("goto");
		var do_func = $(obj).attr("todo");
		var param = '';
		var post_url = ''
		
		if(obj[0].tagName=="FORM"){
			param = GetParameter(obj);
			post_url = obj.attr('action');
			action_method = "post";
		}else{
			post_url = obj.attr('href');
			param = obj.attr('params');
			var action_method = obj.attr('method');
			if (!action_method){
				action_method = "get";
			}
		}
		if (post_url.indexOf('?') != -1) {
			post_url += '&format=json';
		} else {
			post_url += '?format=json';
		}
		var options = {
			type : action_method,
			url : post_url,
			dataType : 'json',
			contentType : "application/x-www-form-urlencoded; charset=utf-8",
			data : param,
			success : function(result,textStatus) {
				offset = obj.offset();
				if(result.code==-10){
					login();
				}else if(result.code==0){
					if (result.msg.change){
						var change = result.msg.change;
						result.msg = result.msg.msg;
						var offset = null;
						if(obj[0].tagName=="FORM"){
							offset = obj.find('[type="submit"]').offset();
						}else{
							offset = obj.offset();
						}
						var timeOut = 0;
						if (change.score && change.score != 0) {
							timeOut += 500;
							setTimeout(function() {
								showTips('积分' + change.score,
										'fg-color-blue', offset);
							}, timeOut);
						}

						if (change.power && change.power != 0) {
							timeOut += 500;
							setTimeout(function() {
								showTips('体力' + change.power, 'fg-color-red',
										offset);
							}, timeOut);
						}

						if (change.amount && change.amount != 0) {
							timeOut += 500;
							setTimeout(function() {
								showTips('游爱星' + change.amount,
										'fg-color-green', offset);
							}, timeOut);
						}

						if (change.level && change.level != 0) {
							timeOut += 500;
							setTimeout(function() {
								showTips('级别' + change.level,
										'fg-color-orange', offset);
							}, timeOut);
						}
							
					}
					if(result.next_url){
						go_url = result.next_url;
					}
					if (result.msg.model_id){
						var last_action = obj.attr("action");
						if(last_action){
							last_action = last_action.replace(/&?id=/,'');
							if(last_action.indexOf("?")==-1)
								last_action += "?id=" + result.msg.model_id;
							else 
								last_action += "&id=" + result.msg.model_id;
							obj.attr("action",last_action);
						}
					}
					
					if (do_func && do_func != "") {
						eval(do_func + "(result,obj)");
					} else if(go_url && go_url!=""){
						if(go_url=='#back'){
							go_url = document.referrer;
							var the_url = document.location.href;
							if(go_url.indexOf(the_url.split('/')[2])==-1)
								go_url = '/';
						}
							
						setTimeout(function(){document.location = go_url;},1000);
					}
					
					if(typeof(result.msg)=='object' && result.msg.msg)
						result.msg = result.msg.msg;						

					if(typeof(result.msg)=='object' || (result.msg == '' && typeof(result.msg) == "string"))
						result.msg = '';
						//result.msg = result.msg
				}
				if(obj[0].tagName=="FORM")
					obj.find("input").attr('disabled', false); 
				if (result.msg != '') {
					if(obj[0].tagName=="FORM"){
						showFormTips(obj,result.msg, result.code);
					}else{
						showTips(result.msg,'fg-color-black',offset);
					}					
				}
				
			},
			cache : false,
			timeout : 5000,
			error : function(XMLHttpRequest,textStatus) {
				var msg = "未知错误!" + XMLHttpRequest.status;
				if(XMLHttpRequest.status==403){
					msg = '请先登录!';
					login();
				}
				
				if(obj[0].tagName=="FORM"){
					showFormTips(obj,msg,1);
					if(obj[0].tagName=="FORM")
						obj.find("input").attr('disabled', false); 
				}else{
					showTips(msg,'fg-color-black',obj.offset());
				}
			}
		}
		if(obj[0].tagName=="FORM"){
			obj.find("input").attr('disabled', true);
			showFormTips(obj,"提交中...");
		}

		$.ajax(options);
		return false;
	}
	
	var showTips = function(msg,color_style,pos){
		if(pos==null){
			pos = {left:400,top:($(window).scrollTop() + 300)};
		}else{
			if(pos.left<400)
				pos.left = 400;
			if(pos.top<($(window).scrollTop() + 300))
				pos.top = ($(window).scrollTop() + 300);
		}
		if(color_style==null){
			color_style = 'fg-color-white';
		}
		var msg_obj = '<p class="tips ' + color_style + '" style="background-color:rgba(100,100,100,0.5);top:'+(pos.top)+'px;padding:5px;font-size:14px;left:'+(pos.left)+'px;">'+msg+'</p>';
		$(msg_obj).appendTo('body').animate({top:(pos.top-100)},500,function(){
			$(this).fadeOut(3000,function(){$(this).remove()});
		});
	} 
	window.alert = showTips;
	
	var showFormTips = function(the_form,msg, error){
			var feedback = $(the_form).find('.alert');
			msg = '<button data-dismiss="alert" class="close" type="button"></button>' + msg;
			if(feedback.length==0){
				var msg = '<p class="alert" style="position:absolute;">'+msg+'</p>';
				$(the_form).find('[type="submit"]').after(msg);
			}else{
				feedback.html(msg);
			}
			if(error==0){
				feedback.removeClass('alert-error');
				feedback.addClass('alert-success');
			}else{
				feedback.removeClass('alert-success');
				feedback.addClass('alert-error');
			}
			feedback.fadeIn('slow',function(){
				setTimeout(function(){
				feedback.fadeOut();
				},2000);
			});
			
			
	}

	var removeLine = function(result,obj){
			$(obj).parent().parent().fadeOut(function(){
				$(this).remove();
			});
	}
	var reload = function(result,obj){
		document.location.reload();
	}
	
	var GetParameter = function (the_form) {
		var result = "";
		$(the_form).find("input,textarea,select").each(function() {
			if ($(this).attr('name') == undefined || $(this).attr('name') == ''){
				return;
			}
			//过滤不需要的input
			var type = $(this).attr('type');
			if (type == "button" || type == "submit")
				return;

			var chk_box = false;
			if (type == "checkbox" || type == "radio")
				chk_box = true;

			var chk = false;

			if (chk_box) {
				if (!$(this)[0].checked)
					return;
				// 等于 each中的continue;
			}

			result += $(this).attr('name') + "=" + encodeURIComponent($(this).val()) + "&";
			
		});
		return result;
	}
	var applyAjaxDoFunc = function(){
		$(document).on('submit','form.ajax',function(e) {
			e.preventDefault();
			var valid = $(this).attr('valid');
			var allow = true;
			if (valid) 
				allow =  eval(valid + "()");
			if (allow)
				ajax_do($(this));
		});
		$(document).on('click','a.ajax', function(e) {
			e.preventDefault();
			if($(this).attr("class").indexOf("confirm")==-1 ||($(this).attr("class").indexOf("confirm")!=-1 && confirm("确定要执行此操作吗？")))
				ajax_do($(this));
		});
	}
	window.applyAjaxDoFunc = applyAjaxDoFunc;
	$(document).ready(function() {
		$('select').each(function(){
			$(this).val($(this).attr('value'));
		});
		$(document).on("focus",".init textarea",function(){
			$(this).parent().parent().removeClass('init');
			$(this).parent().parent().find('input[type="submit"]').removeAttr("disabled");
		});
		applyAjaxDoFunc();
	})
})(window.jQuery);