$(document).ready(function() {
	if (top.location == self.location) {
		fixWin();
		doLanguageTypeChange();
		$("#menuList").html("<dl>" + showMenuList("0") + "</dl>");
	} else {
		$(".list tr:even").addClass('even');
		
		
		
		$("#err_msg").click(function() {
			$("#err_msg").hide();
		})
		//parent.document.title = parent.document.title.replace(/- \S+/,"- " + document.title);

		$('.Wdate').focus(function() {
			WdatePicker({
				dateFmt : 'yyyy-MM-dd HH:mm:ss'
			})
		});
		$('.Wdate1').focus(function() {
			WdatePicker({
				dateFmt : 'yyyy-MM-dd'
			})
		});
		$('.dialog').click(function() { 
 			$.dialog({type:'iframe', value:$(this).attr('href') });
			return false;
		});

		if (parent.$('#tabList a.active').length != 0) {
			var href = window.location.href;
			href = href.replace('http://', '');
			var tmp = href.indexOf('/');
			href = href.substr(tmp, href.length - tmp);
			var tmp2 = href.indexOf('?');
			if (-1 != tmp2) {//带参数移除参数
				href = href.substr(0, tmp2);
			}
			
			if (href[href.length-1] == '/'){
				href = href.substr(0, href.lastIndexOf('/'));
			}
			
			var url_id = href.replace(/[:\/\._]/g, "-");
			
			var tmpID = parent.$('#tabList a.active').attr('id');
			
			parent.$('#tabList a.active').attr('id', url_id + "_tab");
			parent.$('#' + tmpID.replace('_tab', '')).attr('id', url_id);
			var iframe_height = $(document).height();
			if(iframe_height<($(parent.window).height())){
				iframe_height=$(parent.window).height();
			}
			parent.$('#' + url_id.replace('_tab', '')).css('height', iframe_height+'px');
			parent.$('#tabList a.active').text($('title').html());
			parent.$('#tabList a.active').attr('href', href);
			parent.last_url_id = url_id;
			$(parent.document).scrollTop(0);
			
			//fixAmound();
		}

	}

	alterForLink();
	
	$(window).resize(function() {
		if (top.location == self.location) {
			fixWin();
		}
	});
	
	$(window).scroll(function() {
		if($(window).scrollTop()>100){
			$('#tabList').css('position','fixed');
		}else{
			$('#tabList').css('position','static');
		}
	});
	
	
	$('[data-action="chk-all"]').bind('click', function(){
		var child_name = $(this).attr('data-chk-child');
		if(!child_name)
			return;
		$('input[name=' + child_name + ']').attr('checked', $(this).attr('checked'));
	});
	
});

function fixAmound() {
	var gold_item_index = -1;
	var amount_item_index = -1;
	$(document).ready(function(){
		var index = 0;
		var href = document.location.href;
		$(".list th").each(function(){
			if (-1 != href.indexOf('pay/list')){
				return;
			}
			
			if($(this).text().indexOf("充值金额")!=-1 || $(this).text().indexOf("实充金额")!=-1){
				amount_item_index = index;
			}else if($(this).text().indexOf("金币")!=-1){
				gold_item_index = index;
			}
			index += 1;
		});
		if(gold_item_index>-1 && amount_item_index>-1){
			var gold_value = 0;
			var amoun_value = 0;
			
			$(".list tr").each(function(){
				if($(this).find("td").length>0){
					gold_value = $(this).find("td")[gold_item_index].innerHTML * 1;
					amoun_value = $(this).find("td")[amount_item_index].innerHTML * 1;
					if(amoun_value>0){
						$(this).find("td")[amount_item_index].innerHTML = gold_value / 10;
					}
				}
			});
		}
	});
}

function fixWin() {
	//$("#body").css("height", ($(window).height() - $("#header").outerHeight()) + "px");
	$("#main").css("width", ($(window).width() - $("#menuList").outerWidth()) + "px");
}

var is_frist_menu = true;
function showMenuList(parent_id) {
	if ( typeof (menu_list) == 'undefined')
		return;
	var str = "";

	for (var i = 0; i < menu_list.length - 1; i++) {
		var item = menu_list[i];

		if (item.name == null || item.parent_id != parent_id)
			continue;

		if (parent_id == "0")
			str += '<dt onclick="switchMenuItem(this)">';

		var item_name = item.name
		if (item.icon != "")
			item_name = '<img src="' + item.icon + '" />' + item_name;
		if (item.css != "")
			item_name = '<span style="' + item.css + '">' + item_name + '</span>';
		if (item.url != "")
			item_name = '<a href="' + item.url + '" onclick="showTab(this);return false;" title="' + item.name + '">' + item_name + '</a>';
		else {
			var css_name = '';
			if (item.parent_id != 0)
				css_name = ' class="gray"';
			item_name = '<a href="javascript:void(0)"' + css_name + '>' + item_name + '</a>';
		}
		str += item_name;

		if (parent_id == "0")
			str += "</dt>";

		var childStr = showMenuList(item.id);
		if (childStr != "") {
			if (is_frist_menu && false) {
				str += "<dd>" + childStr + "</dd>";
				is_frist_menu = false;
			} else
				str += "<dd class='hide'>" + childStr + "</dd>";
		}

	}
	return str;
}

var last_url_id = "";
function showTab(link) {
	link = $(link);
	href = link.attr("href");
	if (typeof (href) == "undefined")
	{
		return;
	}
	if (-1 != href.indexOf('http://')) {
		href = href.replace('http://', '');
		var tmp = href.indexOf('/');

		if (-1 != tmp)
			href = href.substr(tmp, href.length - tmp);
	}
	
	if (href[href.length-1] == '/'){
		href = href.substr(0, href.lastIndexOf('/'));
	}
	
	var tmp = href.indexOf('?');
	if (-1 != tmp) {//带参数移除参数
		href = href.substr(0, tmp);
	}
	
	var url_id = href.replace(/[:\/\._]/g, "-");
	
	
	var is_reload = true;

	if ($("#" + url_id).length == 0) {
		is_reload = false;
		$("#main").append("<iframe frameborder='0' src='" + link.attr("href") + "' id='" + url_id + "' name='" + url_id + "'></iframe>");
		$("#tabList").prepend("<a linkIframeId=\"" + url_id + "\" href=\"" + link.attr("href") + "\" title=\"双击关闭\" ondblclick=\"closeTab(this);return false;\" onclick=\"showTab(this);return false;\" id=\"" + url_id + "_tab\" class=\"active\">" + link.html().replace(/<[^>]+?>/g, "") + "</a>");
		$(document).scrollTop(0);
	}
	if (last_url_id != url_id) {//切换标签
		var timer = 500;
		$("#tabList a").removeClass("active");
		$("#" + url_id + "_tab").addClass("active");
		var mainWidth = $("#main").width();
		if(last_url_id!=url_id){
			if(last_url_id!='')
				$('#'+last_url_id).hide();
			$('#'+url_id).show();
		} 
		
//		$("#" + url_id).css({
//			"left" : (mainWidth * -1) + "px",
//			"display" : ""
//		});
//		if (last_url_id != "")//移除上一次打开的frame
//			$("#" + last_url_id).animate({
//				left : mainWidth + "px"
//			}, timer, function() {
//				$(this).hide();
//				//双击关闭
//			});
//		$("#" + url_id).animate({
//			left : "0px"
//		}, timer, function() {
//			/* 返回之前打开的标签重复加载，暂时注释 */
//			/*if (is_reload)
//			 $('#' + url_id).attr('src', link.attr("href"));
//			 */
//		});

		last_url_id = url_id;
	} /*else {
	 window.frames[url_id].document.location = link.attr("href");
	 }*/
}

var closeTab_timer;
function closeTab(link) {
	clearTimeout(closeTab_timer);
	closeTab_timer = setTimeout(function() {
		link = $(link);
		var url_id = link.attr("href").replace(/[:\/\._]/g, "-");
		if ($("#" + url_id).length > 0) {
			$("#" + url_id).remove();
			$("#" + url_id + "_tab").remove();
		}
		showTab($("#tabList a:first-child"));
	}, 500);
}

function switchMenuItem(menu) {
	menu = $(menu);
	//var v = menu.next().prop("tagName")
	//if (typeof(v) == "undefined")
	//	menu.next().slideToggle('fast');
	if (menu.next().prop("tagName") == "DD")
		menu.next().slideToggle('fast');
}

function switchMenuList() {
	var menuList = $("#menuList");
	if (menuList.css("margin-left").replace("px", "") * 1 == 0) {
		$("#menuList").animate({
			marginLeft : "-200px"
		}, 100);
		$("#main").animate({
			marginLeft : "0"
		}, 100, function() {
			$("#main").css("width", $(window).width() + "px");
			$("#" + last_url_id).width("100%");
		})
	} else {
		$("#menuList").animate({
			marginLeft : "0"
		}, 100);
		$("#main").animate({
			marginLeft : "200px"
		}, 100, function() {
			$("#main").css("width", ($(window).width() - $("#menuList").outerWidth() - 5) + "px");
			$("#" + last_url_id).width("100%");
		})
	}
}

//给下面pager 方法调用
function change_page(ele, pageUrl){
	var value = ele.value;
	if (0>= value){
		return;
	}
	
	if (pageUrl.substr(pageUrl.length - 1, 1) == "&"){
		pageUrl = pageUrl.substr(0, pageUrl.length - 1);
	}
		
	var url =  pageUrl + "&page_num=" + value;
	
	document.location.href = url;
}

function pager(pageNum, pageSize, totalRecord) {
	var totalPage = parseInt(totalRecord / pageSize);
	//总页数
	if (totalRecord % pageSize != 0)
		totalPage++;

	var pageUrl = document.location.href;
	pageUrl = pageUrl.replace(/page_num=\d+/, '')
	if (pageUrl.indexOf("?") == -1)
		pageUrl += "?"

	if (pageUrl.substr(pageUrl.length - 1, 1) != "&" && pageUrl.substr(pageUrl.length - 1, 1) != "?")
		pageUrl += "&";

	var pagerHtml = "";

	var display_str = "display: none; ";
	if (pageNum > 1)
		display_str = "";

	pagerHtml += '<a href="' + pageUrl + 'page_num=' + (pageNum - 1) + '" class="prePage"  style="' + display_str + '" >上一页</a>';

	var sPageNum = pageNum - 4;
	if (sPageNum < 1)
		sPageNum = 1;
	var ePageNum = sPageNum + 10;
	if (ePageNum > totalPage)
		ePageNum = totalPage;

	for (var i = sPageNum; i <= ePageNum; i++) {
		if (i == pageNum)
			pagerHtml += '<a href="' + pageUrl + "page_num=" + i + '"  class="ajax active"    page_num="' + i + '"   >' + i + '</a>';
		else
			pagerHtml += '<a id="pager_' + i + '" href="' + pageUrl + "page_num=" + i + '" class="ajax"  page_num="' + i + '"  >' + i + '</a>';
	}

	if (pageNum < totalPage)
		pagerHtml += '<a href="' + pageUrl + 'page_num=' + (pageNum + 1) + '"  class="nextPage"  >下一页</a>';
	
	pagerHtml += '<input type="text" style="width:20px; margin:0px; padding:0px;" onblur="change_page(this, \''+ pageUrl +'\'  )" > ';
	
	$("#pager").html(pagerHtml);
}


function pager_post(pageNum, pageSize, totalRecord) {
	var totalPage = parseInt(totalRecord / pageSize);
	if (totalRecord % pageSize != 0)
		totalPage++;

	var pageUrl = document.location.href;
	pageUrl = pageUrl.replace(/page_num=\d+/, '')
	if (pageUrl.indexOf("?") == -1)
		pageUrl += "?"

	if (pageUrl.substr(pageUrl.length - 1, 1) != "&" && pageUrl.substr(pageUrl.length - 1, 1) != "?")
		pageUrl += "&";

	var pagerHtml = "";
	if (pageNum > 1)
		pagerHtml += "<a href='javascript:goPage(" + (pageNum - 1) + ");'>上一页</a>";

	var sPageNum = pageNum - 4;
	if (sPageNum < 1)
		sPageNum = 1;
	var ePageNum = sPageNum + 10;
	if (ePageNum > totalPage)
		ePageNum = totalPage;

	for (var i = sPageNum; i <= ePageNum; i++) {
		if (i == pageNum)
			pagerHtml += '<span>' + i + '</span>';
		else
			pagerHtml += "<a href='javascript:goPage(" + i + ");'>" + i + "</a>";
	}

	if (pageNum < totalPage)
		pagerHtml += "<a href='javascript:goPage(" + (pageNum + 1) + ");'>下一页</a>";

	$("#pager").html(pagerHtml);
}

function goPage(pageNum) {
	var pageUrl = document.location.href;

	pageUrl = pageUrl.replace(/page_num=\d+/, '')

	if (pageUrl.indexOf("?") == -1)
		pageUrl += "?"

	if (pageUrl.substr(pageUrl.length - 1, 1) != "&" && pageUrl.substr(pageUrl.length - 1, 1) != "?")
		pageUrl += "&";

	actionUrl = $("form[method='post']").attr('action');
	if (actionUrl == '') {
		actionUrl = pageUrl;
	}

	if (actionUrl.indexOf("?") == -1)
		actionUrl += "?"

	if (actionUrl.substr(actionUrl.length - 1, 1) != "&" && actionUrl.substr(actionUrl.length - 1, 1) != "?")
		actionUrl += "&";

	actionUrl += 'page_num=' + pageNum

	$("form[method='post']").attr('action', actionUrl);
	$("form[method='post']").submit();
}

function inputText(inputName, inputValue) {
	$("input[name='" + inputName + "']").val(inputValue);
}

function replyQuestion(questionId) {
	$("input[name='question_id']").val(questionId);
	$("textarea[name='answer']").val($("#reply_" + questionId).text()); 
	$(".msgbox").css({top : parent.document.documentElement.scrollTop+"px"});
	$(".msgbox").show();
}

function replyQuestionDo(the_form) {
	var post_data = 'question_id=' + the_form.question_id.value + '&' + 'answer=' + the_form.answer.value
	$.ajax({
		url : the_form.action,
		type : the_form.method,
		cache : false,
		data : post_data,
		success : function(data) {
			if (data.length == 0) {
				$("#reply_" + the_form.question_id.value).html(the_form.answer.value);
				return;
			}
			alert(data);
		},
		error : function() {
			alert('发生错误啦!')
		}
	});
	$(".msgbox").hide();
	return false;
}

function alterForLink() {
	$(".del").click(function() {
		return confirm("确认删除吗?");
	});
	$(".ask").click(function() {
		return confirm("确认进行此操作吗 ?");
	});
}

function selectAll(oId) {
	var checked = $('#' + oId).attr('checked');
	var select_area = oId + '_area'
	$("#" + select_area + " input[type='checkbox']").each(function() {
		$(this).attr('checked', checked);
	});
}
 
//$(function() {
// run the currently selected effect
function runEffect(msg) {
	alert("aaa");

	$("#show_effect_msg").html(msg);

	// get effect type from
	var selectedEffect = "blind";
	//$( "#effectTypes" ).val();

	// most effect types need no options passed by default
	var options = {};
	// some effects have required parameters
	if (selectedEffect === "scale") {
		options = {
			percent : 100
		};
	} else if (selectedEffect === "size") {
		options = {
			to : {
				width : 280,
				height : 185
			}
		};
	}

	// run the effect
	$("#effect").show(selectedEffect, options, 500, callback);
};

//callback function to bring a hidden box back
function callback() {
	setTimeout(function() {
		$("#effect:visible").removeAttr("style").fadeOut();
	}, 1000);
};

// set effect from select menu value
//		$( "#button" ).click(function() {
//			runEffect("角色名错误!");
//			return false;
//		});

//		$( "#effect" ).hide();
//	});

 

function showDialog(url, the_title) {
	showDialog_param(url, {
		title : the_title,
		maxHeight : 900,
		maxWidth : 700,
		minHeight : 300,
		minWidth : 400
	});
}

// 获取 某 元素中所有空间需要提交的参数字符串（用户Ajax提交中的data）
function GetPostParameter(elementStr) {
	var result = "";
	$(elementStr).find("input,textarea,select").each(function() {

		//过滤不需要的input
		var type = $(this).attr('type');
		if (type == "button" || type == "submit")
			return;

		var chk_box = false;
		if (type == "checkbox" || type == "radio")
			chk_box = true;

		var chk = false;

		if (chk_box) {
			if (!$(this).attr('checked'))
				return;
			// 等于 each中的continue;
		}
		if ($(this).attr('name') == undefined || $(this).attr('name') == ''){
			return;
		}
		result += $(this).attr('name') + "=" + encodeURIComponent($(this).val()) + "&";
		
	});
	return result;
}

/// 获取 某 元素中的 json 元素
function GetJSON(elementStr) {
	var json = {};
	$(elementStr).find("input,textarea,select").each(function() {
		var name = $(this).attr('name');
		if (!name || '' == name){
			return;
		}
		
		//过滤不需要的input
		var type = $(this).attr('type');
		if (type == "button" || type == "submit")
			return;
		
		if ($(this).attr('type') != "checkbox") {
			json[name] = $(this).val();
		} else {
			if ($(this).attr('checked')) {
				if (json[name] == null)
					json[name] = new Array();
				json[name].push($(this).val());
			}
		}
	});
	return json;
}

function valueReplace(v) {
	v = v.toString().replace(new RegExp('(["\"])', 'g'), "\\\"");
	return v;
}

///默认没有todo 标签则调用这个提示
function default_tip(msg) {
	$("#tip_box").html('操作完成');
	$("#tip_box").dialog();
}


//搜索下拉框
function search_dbl_list(dbl_class_name, input_box_class_name){
	var input_value = $("." + input_box_class_name).val();
	$("."+dbl_class_name + " option").each(function(){
		if(-1 != $(this).text().indexOf(input_value))
			$(this).attr('selected', true);
	});
}

