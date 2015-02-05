$(document).ready(function() {
	
	//处理本来带del class 的A链接标签
	$('a.del').each(function() {
		//如果同时存在 ajax class 则删除本来的del class所绑定的事件
		if(-1 !=  $(this).attr('class').indexOf('ajax')){
			$(this).unbind('click');
		}
	});


	bindingPagerAjax();

	//客服回复 用的....
	$(".msgbox.ajax").bind("submit", function() {

		var url = "/question/answer";

		var question_id = $('input[name="question_id"]').val();
		var answer = $('textarea[name="answer"]').val();

		var options = {
			type : "post",
			url : url,
			data : {
				"question_id" : question_id,
				"answer" : answer,
				"ajax" : true
			},
			success : function(result) {
				//更新回复内容
				$("#reply_" + question_id).html(result);
				//关闭弹出窗口
				$(".msgbox.ajax").hide();
			}
		};
		$.ajax(options);
		return false;
	});
});

function init_ALinkPager() {
	$("a.ajax").each(function() {
		var page_num = $(this).attr("page_num");

		if (page_num == null)//如果不是分页
			//each 中的continue
			return true;
		var url = $(this).attr("href");
		if (-1 == url.indexOf('ajax=true')) {
			if (-1 == url.indexOf('?'))
				url += '?';
			else
				url += '&';
			url += "ajax=true";
			$(this).attr("href", url)
		}
	});

	$(".prePage,.nextPage").each(function() {
		var url = $(this).attr("href");
		if (-1 == url.indexOf('ajax=true')) {
			if (-1 == url.indexOf('?'))
				url += '?';
			else
				url += '&';
			url += "ajax=true";
			$(this).attr("href", url)
		}
	});
}

function bindingPagerAjax() {

	init_ALinkPager();
	
	$("a").each(function() {
		if ($(this).html() == "删除") {
			$(this).css("color", "gray");
		}
	});

	//设置列表 行间隔颜色
	$(".list tr:even").addClass('even')
	
	//设置当前页样式
	setPageFocus();
	
	$("a.ajax").bind("click", function() {

		var url = $(this).attr("href");

		var page_num = $(this).attr("page_num");

		if (page_num != null) {//如果是分页

			//纪录‘已知’ 最大页数
			if (new Number(known_max_pageNum) < new Number(page_num)) {
				known_max_pageNum = page_num;
			}
 
			do_page(page_num, url);
			//调用分页
			return false;
			//退出并取消A标签跳转
		}

		//如果是普通A标签
		var todo = $(this).attr("todo");

		var json = {
			'ajax' : true
		};

		var tip = $(this).attr("tip");
		//提示框
		if (tip != null) {
			var result = confirm(tip);
			if (!result)
				return false;
		}

		ajax_Request(url, json, todo);
		return false;
		//取消A标签跳转
	});

	// 上一页
	$(".prePage,.nextPage").show();
	$(".prePage").bind("click", function() {
		up_down_page(-1);
		return false;
		//退出并取消A标签跳转
	});

	// 下一页
	$(".nextPage").bind("click", function() {
		up_down_page(1);
		return false;
		//退出并取消A标签跳转
	});
}

var pagesArray = new Array();
var current_pageNum = 1;
var known_max_pageNum = 0;
//‘已知’总页数
//在这里是换页 的 AJAX
function do_page(page_num, url) {
	current_pageNum = page_num;

	if (existsValue(pagesArray, current_pageNum)) {//已经被添加过
		changePageState();
		setPageFocus();
		$.scrollTo($("#list_" + current_pageNum), 500, {
			axis : "y"
		});
		return;
	}

	ajax_GetList(url);
}

function up_down_page(value) {
	current_pageNum = new Number(current_pageNum) + value;
	if ($("a[page_num=" + current_pageNum + "]").length <= 0) {
		current_pageNum = new Number(current_pageNum) - value;
	}
	$("a[page_num=" + current_pageNum + "]").click();
}

//设置页码 状态
function changePageState() {

	var pageElem_arry = new Array();
	$("a.ajax, span.ajax").each(function() {
		var tmp = $(this).attr("page_num");
		if (tmp != null && tmp != "") {

			var item = {};
			item["page_num"] = tmp;
			item["elem"] = $(this);
			pageElem_arry.push(item);
		}
	});

	sortPageElemArray(pageElem_arry);

	known_max_pageNum = new Number(known_max_pageNum)

	var sPageNum = new Number(current_pageNum) - 4;
	if (sPageNum < 1)
		sPageNum = 1;
	var ePageNum = new Number(current_pageNum) + 10;

	var last_ele_item = pageElem_arry[pageElem_arry.length - 1];

	var tmp = new Number(last_ele_item.page_num);
	if (known_max_pageNum < tmp)
		known_max_pageNum = tmp;

	if (ePageNum > known_max_pageNum)
		ePageNum = known_max_pageNum;

	var index = 0;

	$("#pager").children().each(function() {
		$(this).unbind("click");
		$(this).remove();
	});

	var last_ele = last_ele_item["elem"];
	var href = last_ele.attr("href");
	var pager_str = '<a href="' + href.replace('page_num=' + last_ele.attr('page_num'), 'page_num=1') + '" class="prePage"  >上一页</a>';

	for (var i = sPageNum; i <= ePageNum; i++) {
		href = last_ele.attr("href");
		href = href.replace('page_num=' + last_ele.attr('page_num'), 'page_num=' + i);
		pager_str += '<a href="' + href + '"  class="ajax"  page_num="' + i + '"   >' + i + '</a>';
	}
	href = last_ele.attr("href");
	pager_str += '<a href="' + href.replace('page_num=' + last_ele.attr('page_num'), 'page_num=' + ePageNum) + '"  class="nextPage"  >下一页</a>';

	$("#pager").html(pager_str);
	bindingPagerAjax();
}

//排序页码数组
function sortPageElemArray(pageElem_arry) {
	for (var i = 0; i < pageElem_arry.length; i++) {
		for (var k = 0; k < pageElem_arry.length; k++) {
			var iItem = pageElem_arry[i];
			var kItem = pageElem_arry[k];
			if (new Number(iItem["page_num"]) < new Number(kItem["page_num"])) {
				var nTemp = iItem;
				pageElem_arry[i] = kItem;
				pageElem_arry[k] = nTemp;
			}
		}
	}
}

//设置当前页状态
function setPageFocus() {
	$("a.ajax,  span.ajax").each(function() {
		var tmp = $(this).attr("page_num");
		if (tmp != null && tmp != "") {

			if (tmp == current_pageNum) {//如果是当前页
				$(this).css("background-color", "#fff");
			} else {
				$(this).css("background-color", "");
			}
		}
	});
}

//Ajax请求
function ajax_Request(url, json, todo) {
	$("input").attr('disabled', true);

	var json = GetJSON(this);

	var options = {
		type : "post",
		url : url,
		data : json,
		success : function(result) {
			if (todo == "" || todo == null) {//如果没有指定todo，则调用默认提示
				default_tip(result);
			} else {
				eval(todo + "(result)");
			}
			$("input").attr('disabled', false);
		},
		cache : false,
		timeout : 5000,
		error : function() {
			$("#tip_box").html("链接超时！请重试");
			$("#tip_box").dialog();
			$("input").attr('disabled', false);
		}
	}
	$.ajax(options);
}

function ajax_GetList(url) {
	var options = {
		type : "post",
		url : url,
		data : '',
		success : function(result) {
			if (existsValue(pagesArray, current_pageNum)) {//已经被添加过 则 直接滚动 （这里再判断多一次，原因是处理提交有延时，再被点击多次）
				$.scrollTo($("#list_" + current_pageNum), 500, {
					axis : "y"
				});
				return false;
			}

			//首先先移除旧pager和它下的click 事件 (在呈现新数据中会有pager的div)
			$("#pager").children().each(function() {
				$(this).unbind("click");
			});
			$("#pager").remove();
			//呈现数据
			reflashList(result);
			//加入已加载纪录
			pagesArray.push(current_pageNum);

			bindingPagerAjax();

		},
		error : function() {
			return false;
		}
	};
	$.ajax(options);
}

//呈现分页数据
function reflashList(result) {

	//获取上一页 页数
	var per_pageNum = 1;

	if (current_pageNum > 1) {
		per_pageNum = 1;
		sortPageArray(pagesArray);
		for (var i = 0; i < pagesArray.length; i++) {
			var v = pagesArray[i];
			if (v >= current_pageNum) {
				break;
			}
			per_pageNum = v;
		}
	}
	// 获取上一页 页数 END

	//加载数据
	if ($("#list_" + per_pageNum).length != 0){
		$("#list_" + per_pageNum).after(result);
	}else{
		$(".list").first().after(result);
	}

	//绑定被加载的页数A标签 点击事件 作为”滚动“
	var pageID = '#pager_' + current_pageNum;
	$(pageID).bind("click", {
		page : current_pageNum
	}, function(e) {
		$.scrollTo($("#list_" + e.data.page), 500, {
			axis : "y"
		})
		current_pageNum = e.data.page;
		return false;
	});

	// 滚动到被加载页数的位置
	$.scrollTo($("#list_" + current_pageNum), 500, {
		axis : "y"
	})

	return false;

}

///对数组升序排序
function sortPageArray(array) {

	for (var i = 0; i < array.length; i++) {
		for (var k = 0; k < array.length; k++) {
			var iNum = new Number(array[i]);
			var kNum = new Number(array[k]);
			if (iNum < kNum) {
				var nTemp = iNum;
				array[i] = kNum;
				array[k] = nTemp;
			}
		}
	}
}

///检测数据是否存在值
function existsValue(array, value) {
	for (var i = 0; i < array.length; i++) {
		if (array[i] == value) {
			return true;
			break;
		}
	}
	return false;
}
