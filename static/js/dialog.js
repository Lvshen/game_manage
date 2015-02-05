/**
 * Dialog
 *
 * @author    caixw <http://www.caixw.com>
 * @copyright Copyright (C) 2010, http://www.caixw.com
 * @license   FreeBSD license
 */

/**
 * jQuery的Dialog插件。
 * @param object options 。
 * @return
 */
function Dialog(options) {
	this.options = {};
	this.overlayId;
	this.timeId = null;
	this.isShow = false;
	this.isIe = $.browser.msie;
	this.isIe6 = $.browser.msie && ('6.0' == $.browser.version);
	this.dialog = null;
	 
	this.reset = function(options){ 
		var defaults = {// 默认值。
			title : '提示框', // 标题文本，若不想显示title请通过CSS设置其display为none
			showTitle : true, // 是否显示标题栏。
			closeText : '[关闭]', // 关闭按钮文字，若不想显示关闭按钮请通过CSS设置其display为none
			draggable : true, // 是否移动
			modal : true, // 是否是模态对话框
			center : true, // 是否居中。
			fixed : true, // 是否跟随页面滚动。
			time : 0, // 自动关闭时间，为0表示不会自动关闭。
			close : function(){},
			id : false // 对话框的id，若为false，则由系统自动产生一个唯一id。
		};
		if ('object' != typeof(options)){
			defaults = $.extend(defaults, {type:'text', value:options});
		}
		this.options = $.extend(defaults, options);
		
		//this.options.id = this.options.id ? this.options.id : 'dialog-' + Dialog.__count;
		
		this.options.id = 'dialog-1';
		if (0 != $('#' + this.options.id).length){
			if (null != this.content_parent){
				var dialog_content = $('#' + this.options.id + " .content").children();
				this.content_parent.append(dialog_content);
				dialog_content.hide();
			}
			return;
		}
		
		
		// 唯一ID
		this.overlayId = this.options.id + '-overlay';
		// 遮罩层ID
		this.timeId = null;
		// 自动关闭计时器
		this.isShow = false;
	
		/* 对话框的布局及标题内容。*/
		var barHtml = !this.options.showTitle ? '' : '<div class="bar"><span>' + this.options.title + '</span><a class="close">' + this.options.closeText + '</a></div>';
		this.dialog = $('<div id="' + this.options.id + '" class="mydialog">' + barHtml + '<div class="content"></div></div>').hide();
		$('body').append(this.dialog);
	}

	/**
	 * 重置对话框的位置。
	 *
	 * 主要是在需要居中的时候，每次加载完内容，都要重新定位
	 *
	 * @return void
	 */
	this.resetPos = function() {
		/* 是否需要居中定位，必需在已经知道了dialog元素大小的情况下，才能正确居中，也就是要先设置dialog的内容。 */
		if (this.options.center) {
			var left = ($(window).width() - this.dialog.width()) / 2;
			var top = ($(window).height() - this.dialog.height()) / 2;
			if (top.location != self.location) {
				top = ($(parent.window).height() - this.dialog.height()) / 2;
			}
			if (!this.isIe6 && this.options.fixed) {
				this.dialog.css({
					top : top,
					left : left
				});
			} else {
				this.dialog.css({
					top : top + $(document).scrollTop(),
					left : left + $(document).scrollLeft()
				});
			}
		}
	}
	/**
	 * 初始化位置及一些事件函数。
	 *
	 * 其中的this表示Dialog对象而不是init函数。
	 */
	this.init = function() {
		if (0 < $('#' + this.overlayId).length){
			return;
		}
		
		/* 是否需要初始化背景遮罩层 */
		if (this.options.modal) {
			$('body').append('<div id="' + this.overlayId + '" class="mydialog-overlay"></div>');
			$('#' + this.overlayId).css({
				'left' : 0,
				'top' : 0,
				/*'width':$(document).width(),*/
				'width' : '100%',
				/*'height':'100%',*/
				'height' : $(document).height(),
				'z-index' : ++Dialog.__zindex,
				'position' : 'absolute'
			}).hide();
		}

		this.dialog.css({
			'z-index' : ++Dialog.__zindex,
			'position' : this.options.fixed ? 'fixed' : 'absolute'
		});

		/*  IE6 兼容fixed代码 */
		if (this.isIe6 && this.options.fixed) {
			this.dialog.css('position', 'absolute');
			//this.resetPos();
			var top = parseInt(this.dialog.css('top')) - $(document).scrollTop();
			var left = parseInt(this.dialog.css('left')) - $(document).scrollLeft();
			$(window).scroll(function() {
				this.dialog.css({
					'top' : $(document).scrollTop() + top,
					'left' : $(document).scrollLeft() + left
				});
			});
		}

		/* 以下代码处理框体是否可以移动 */
		var mouse = {
			x : 0,
			y : 0
		};
		function moveDialog(event) {
			var e = window.event || event;
			var the_dialog = event.data;
			var dlg_div = the_dialog.dialog;
			var top = parseInt(dlg_div.css('top')) + (e.clientY - mouse.y);
			var left = parseInt(dlg_div.css('left')) + (e.clientX - mouse.x);
			dlg_div.css({
				top : top,
				left : left
			});
			mouse.x = e.clientX;
			mouse.y = e.clientY;
		};
		this.dialog.find('.bar').bind('mousedown', this, 
			function (event){
				var the_dialog = event.data; 
				if (!the_dialog.options.draggable) {
					return;
				}
				var e = window.event || event;
				mouse.x = e.clientX;
				mouse.y = e.clientY;
				$(document).bind('mousemove', the_dialog, moveDialog);
			}
		);
		
		this.dialog.bind('mousedown', this,
			function(event) {
				var the_dialog = event.data;
				var dlg_div = the_dialog.dialog;
				
				var top = parseInt(dlg_div.css('top'));
				var left = parseInt(dlg_div.css('left'));
				var right = parseInt(dlg_div.css('right'));
				
				if(top <= 0 || left <= 0 || right <= 0){ 
					the_dialog.resetPos();
				}
			}
		);
		
		$(document).mouseup(function(event) {
			$(document).unbind('mousemove', moveDialog);
		});

		/* 绑定一些相关事件。 */
		this.dialog.find('.close').bind('click', this ,this.hide);

		// 自动关闭
		if (0 != this.options.time) {
			timeId = setTimeout(this.close, this.options.time);
		}
	}
	
	this.content_parent = null;
	
	/**
	 * 设置对话框的内容。
	 *
	 * @param string c 可以是HTML文本。
	 * @return void
	 */
	this.setContent = function(c) {
		this.content_parent = null;
		var div = this.dialog.find('.content');
		var current_obj = this;
		if ('object' == typeof (c)) {
			switch(c.type.toLowerCase()) {
				case 'id':
					this.content_parent = $('#' + c.value).parent();
					$('#' + c.value).show();
					div.append($('#' + c.value));
					//div.html($('#' + c.value).html());
					//$('#' + c.value).before(this.dialog);
					break;
				case 'img':
					div.html('加载中...');
					$('<img alt="" />').load(function() {
						div.empty().append($(this));
						//this.resetPos();
					}).attr('src', c.value);
					break;
				case 'url':
					div.html('加载中...');
					$.ajax({
						url : c.value,
						success : function(html) {
							div.html("<div style='max-height:450px; overflow: auto;'>" + html + "</div>");
							current_obj.resetPos();
						},
						error : function(xml, textStatus, error) {
							div.html('出错啦');
						}
					});
					break;
				case 'iframe':
					div.html('');
					var frame_attr = ' frameborder="0" '
					var frame_ele = $('<iframe '+ frame_attr +' src="' + c.value + '" style="width:850px; height:600px;" />');
					var full_screen = $('<input type="button" value="全屏"  />'); 
					full_screen.hide();
					frame_ele.bind('load', function(){ full_screen.show(); });
					div.append(frame_ele);
					full_screen.bind('click', {frame:frame_ele, dialog:this}, this.SetIfrme);
					
					div.append(full_screen);
					break;
				case 'text':
				default:
					div.html(c.value);
					break;
			}
		} else {
			div.html(c);
		}
	}
	
	this.SetIfrme = function(e){
		var frame = e.data.frame;
		var dia = e.data.dialog;
		var doc = frame[0];
		frame.css({width:1200});
		frame.css({height:600});
		dia.resetPos();
	}
	
	/**
	 * 显示对话框
	 */
	this.show = function() {
		this.init();
		
		this.setContent(this.options);	
		 
		if (undefined != this.options.beforeShow && !this.options.beforeShow()) {
			return;
		}

		/**
		 * 获得某一元素的透明度。IE从滤境中获得。
		 *
		 * @return float
		 */
		var getOpacity = function(id) {
			if (!isIe) {
				return $('#' + id).css('opacity');
			}

			var el = document.getElementById(id);
			return (undefined != el && undefined != el.filters && undefined != el.filters.alpha && undefined != el.filters.alpha.opacity) ? el.filters.alpha.opacity / 100 : 1;
		}
		/* 是否显示背景遮罩层 */
		if (this.options.modal) {
			//$('#' + overlayId).fadeTo('slow', getOpacity(overlayId));
			$('#' + this.overlayId).show();
		}
		/*dialog.fadeTo('slow', getOpacity(options.id), function() {
			if (undefined != options.afterShow) {
				options.afterShow();
			}
			isShow = true;
		});*/
		this.dialog.show();
		this.isShow = true;
		
		// 自动关闭
		if (0 != this.options.time) {
			this.timeId = setTimeout(this.close, this.options.time);
		}

		this.resetPos();
	}
	/**
	 * 隐藏对话框。但并不取消窗口内容。
	 */
	this.hide = function(param) {
		var this_dialog = null;
		if(param == undefined){
			this_dialog = this;
		}else{
			this_dialog = param.data;
		}
		
		if (!this_dialog.isShow) {
			return;
		}

		if (undefined != this_dialog.options.beforeHide && !this_dialog.options.beforeHide()) {
			return;
		}

		this_dialog.dialog.fadeOut('slow', function() {
			if (undefined != this_dialog.options.afterHide) {
				this_dialog.options.afterHide();
			}
		});
		if (this_dialog.options.modal) {
			$('#' + this_dialog.overlayId).fadeOut('slow');
		}
		
		this_dialog.options.close();
		
		this_dialog.isShow = false;
		this_dialog.dialog.css({"display": "none"});
	}
	/**
	 * 关闭对话框
	 *
	 * @return void
	 */
	this.close = function() {
		if (undefined != this.options.beforeClose && !this.options.beforeClose()) {
			return;
		}

		this.dialog.fadeOut('slow', function() {
			$(this).remove();
			this.isShow = false;
			if (undefined != this.options.afterClose) {
				this.options.afterClose();
			}
		});
		if (this.options.modal) {
			$('#' + this.overlayId).fadeOut('slow', function() {
				$(this).remove();
			});
		}
		clearTimeout(timeId);
	}
	
	this.reset(options);
	
	//init.call(this);
	//this.setContent(content);

	Dialog.__count++;
	Dialog.__zindex++;
}

Dialog.__zindex = 500;
Dialog.__count = 1;
Dialog.version = '1.0 beta';

$(document).ready(function() {
	jQuery.mydialog = {
		create : function(options) {
			if (undefined == window.mydialog){
				window.mydialog = new Dialog(options);
			}else{
				window.mydialog.reset(options);
			}
			return window.mydialog;
		}
	};

	// dialog adapter
	(function($) {
		$.fn.dialog = function(options) {
			if ('close' == options) {
				$(this).hide();
				return;
			}
			var defaults = {
				modal : true,
				type : 'id',
				value : $(this).attr("id")
			};
			var opts = $.extend(defaults, options);
			var dia = $.mydialog.create(opts);
			dia.show();
			return dia;
		}
	})(jQuery);

	jQuery.dialog = function(options) {
		var dia = null;
		if (top.location != self.location) {
			dia = parent.$.mydialog.create(options);
		}else{
			dia = $.mydialog.create(options);
		}
		dia.show();
		return dia;
	};
});


