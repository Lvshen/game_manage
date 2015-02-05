/*
 * 加载服务器数据并显示
 * data-role = 'ajax.html'
 * data-params-url #数据页地址
 * data-params-target #目标显示标签
 * data-params-template #模板地址
 */


(function($) {
	var get_attr = function(obj, param_name){
		var result = obj.attr('data-'+param_name);
		if(!result)
			result = obj.attr(param_name);
		return result;
	}
	
	var load_html = function(obj) {
		var data_url = '';
		var data_tpl_url = get_attr(obj, 'params-template');
		var do_func = get_attr(obj, 'params-todo');
		if (obj[0].tagName == "A") {
			
			data_url = obj.attr('href');
			obj = get_attr(obj, 'params-target');
			//obj.show();
		} else {
			data_url = get_attr(obj, 'params-url');
		}
		if(data_url=='')return;
		if (data_url.indexOf('?') != -1) {
			data_url += '&format=json';
		} else {
			data_url += '?format=json';
		}
		obj.html('加载中...');
		dataType = '';
		if(data_tpl_url && data_tpl_url!=""){
			dataType = 'json';
		}
		var data_result = '';
		var options = {
			type : "get",
			url : data_url,
			dataType : dataType,
			contentType : "application/x-www-form-urlencoded; charset=utf-8",
			success : function(result) {
				data_result = result;
				if(data_tpl_url && data_tpl_url!=""){
					//加载模板
					load_template(data_tpl_url).done(function(tpl) {
						var doTpl = doT.template(tpl);
						result = doTpl(data_result);
						obj.html(result);
						if(do_func){
							eval(do_func + "(data_result,obj)");
						}
					});
				}
				else{
					obj.html(result);
					if(do_func){
						eval(do_func + "(data_result,obj)");
					}
				}
				
			},
			cache : false,
			timeout : 5000,
			error : function() {
				alert('json format has error');
			}
		}
		$.ajax(options);
	}

	var load_template = function(tpl_url) {
		var tmpl = null;//localStorage.getItem(tpl_url);
		if (!tmpl) { //如果模板不存在，获取
			tmpl = $.get('/static/template/' + tpl_url + '.html',{cache : false}).done(function(data) {
				localStorage.setItem(tpl_url, data);
			});
		} else {
			var dtd = $.Deferred();
			tmpl = dtd.resolve(tmpl);
		}
		return tmpl;
	}
	
	var applyAjaxHtmlFunc = function(){
		/*
		$('[data-role="ajax-html"]').each(function() {
			if ($(this)[0].tagName == "A") {
				$(this).on('click', function(e) {
					e.preventDefault();
					load_html($(this));
				})
			}
		})*/
	}
	window.applyAjaxHtmlFunc = applyAjaxHtmlFunc;
	$(document).ready(function() {
		initAjaxLoadHtml();
	});
	function initAjaxLoadHtml(){
		
		$('[data-role="ajax-html"]').each(function() {
			if ($(this)[0].tagName == "A") {
				$(this).on('click', function(e) {
					e.preventDefault();
					load_html($(this));
				})
			} else {
				var data_params_url = $(this).attr('data-params-url');
				if (data_params_url && '' != data_params_url)
					load_html($(this));
			}
		});
		
		$(document).on('click', 'a[data-role="ajax-html"]',function(e){
			var target = e.target || e.srcElement;
		 
			if(typeof e.preventDefault == 'function'){
				e.preventDefault();
				e.stopPropagation();
			}else{
				e.returnValue = false;
				e.cancelBubble = true;
			}
			load_html($(this));
		});
	}
	window.init_ajax_load_html = initAjaxLoadHtml;
	window.ajax_load_html = load_html;
})(window.jQuery);