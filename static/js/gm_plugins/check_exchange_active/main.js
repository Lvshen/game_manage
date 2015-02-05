$(document).ready(function(){
	if(!current_page)
		return;
	
	if(current_page != 'gm_post')
		return;
	
	var btn = $("#btn_submit");
	btn.removeAttr("onclick");
	btn.unbind('click');
	btn.bind('click', function(){
		post_on_click();
		return false;
	});
});



//需要提交的数量
var server_count = 0;
var post_count = 0;
var post_server_list = [];//要去请求的服务器列表
var finish_server_list = [];//正确返回参数的服务器列表 
var err_server_list = [];//异常返回参数的服务器列表

var tip_div = $(".msg_tip_div");//信息框
var the_form = $("#gm_form");//提交的form


/*关于活动的一些变量*/
var status_activity_data = {};

function post_on_click(){
	initPostState();
	$("input[flag='batch_server_id']:checked").each(function(){
		var server_id = $(this).val();
		post_server_list.push(server_id);
	});
	var post_len = post_server_list.length;
	server_count = finish_server_list.length;
	while(post_len){
		post_len--;
		var p_id = post_server_list[post_len];
		var finish_len = finish_server_list.length;
		var find = false;
		while(finish_len){
			finish_len--;
			var f_id = finish_server_list[finish_len];
			if(f_id == p_id){
				find = true;
				break;
			}
		}
		if(!find)
			server_count++;
	}
	
	doPost();
	return false;
}

function initPostState() {
	post_server_list = [];
	err_server_list = [];
	post_count = 0;
	tip_div.html('');
}

function doPost() {
	$("#btn_submit").attr('disabled', 'disabled');
	postData(post_server_list.pop());
}

function postData(server_id, err_count){
	if(!server_id){
		$("#btn_submit").removeAttr('disabled');
		tip_div.html("<p>全部完成</p>");
		display(status_activity_data);
		return;
	}
	
	for(var i=0; i < finish_server_list.length; i++){
		if(server_id == finish_server_list[i]){
			post_count++;
			postData(post_server_list.pop());
			return;
		}
	}
	
	tip_div.html(tip_div.html() + "<p>正在获取状态:" +server_id+ "...</p>");
	var url = the_form.attr('action');
	if (-1 == url.indexOf('?')){
		url += '?';
	}else{
		url += "&";
	}
	url += "ajax=1";
	var param = GetJSON("#gm_form");
	param['server_id'] = server_id;
	var options = {
		type : "post",
		url : url,
		contentType : "application/x-www-form-urlencoded; charset=utf-8",
		data : param,
		success : function(result) {
			try{
				result = eval('(' + result + ')');
				var chk_result = get_data_callback(result, server_id);
				if(!chk_result){
					if(!err_count){
						err_count = 1;
					}
					if (err_count >= 10){
						post_count++;
						err_server_list.push(server_id);
						tip_div.html(tip_div.html() + "<p style='color:red;' >放弃获取:" +server_id+ "</p>");
						postData(post_server_list.pop());
						return;
					}
					err_count ++;
					tip_div.html(tip_div.html() + "<p>重新获取状态:" + server_id  + "</p>");
					postData(server_id, err_count);
					return;
				}
				post_count ++;
				tip_div.html(tip_div.html() + "<p style='color:green;' >获取状态成功:" + server_id  + "</p>");
				finish_server_list.push(server_id);
				postData(post_server_list.pop());
			}catch(ex){
				post_count++;
				tip_div.html(tip_div.html() + "<p>重新获取状态:" + server_id  + "</p>");
				console.log('eval result error:::::::::::::::::::');
				postData(post_server_list.pop());
			}
		},
		cache : false,
		timeout : 20000,
		error : function(msg) { 
			if(!err_count){
				err_count = 1;
			}
			if (err_count >= 10){
				post_count++;
				err_server_list.push(server_id);
				tip_div.html(tip_div.html() + "<p style='color:red;' >网络异常,放弃获取:" +server_id+ "</p>");
				postData(post_server_list.pop());
				return;
			}
			tip_div.html(tip_div.html() + "<p>重新获取状态:" + server_id  + "</p>");
			err_count ++;
			postData(server_id, err_count);
		}
	}
	$.ajax(options);
}


function get_data_callback(result,server_id){
	if(result.err_msg)
		return false;
	
	/*{"activity_id": 0, 
	 * "aet": 1432093676, 
	 * "act": 1432525560, 
	 * "aot": 1432093680, 
	 * "apl": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 100, 300, 500, 1000, 3000, 5000, 10000, 20000, 30000, 40000, 45000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 200000], 
	 * "ada": "www.baidu.com", 
	 * "arl": [[[9, 3]], [[9, 3]], [[9, 4]], [[9, 5]], [[9, 6]], [[9, 7]], [[2, 3020]], [[2, 5022]], [[2, 2032]], [[2, 3020]], [[9, 8]], [[2, 5022]], [[2, 2032]], [[2, 3020]], [[2, 5022]], [[2, 2032]], [[2, 5022]], [[9, 9]], [[2, 2032]], [[9, 10]], [[9, 3]], [[9, 3]], [[9, 4]], [[9, 5]], [[9, 6]], [[9, 7]], [[2, 3020]], [[2, 5022]], [[2, 2032]], [[2, 3020]]], 
	 * "iar": false}], 
	 * "code": 0*/
	
	/*判断状态
	 * 有活动： iar (bool)
	 * 已重置：aot 为 0
	 * 没开始活动: aot > now
	 * 设错：act > aot
	 */
	//var status_list = ["有活动", "已重置", "没开始", "设错"];
	
	/*数据格式为
	 * {"runing": { "name":"有活动", "activity_dict":{"1123123":{"activity":{}, "server_list":[]}} }}
	 */
	
	var timestamp = Date.parse(new Date()) / 1000;
	var status_name = "";
	var status_key = "";
	/**/
	var iar = result.iar;
	var aot = result.aot;
	var act = result.act;
	/**/
	if (aot <= timestamp && act > timestamp){
		status_key = "runing";
		status_name = "有活动";
	}else if(aot == '0' || aot == 0){
		status_key = "reset";
		status_name="已重置";
	}else if(aot >= timestamp){
		status_key = "ready";
		status_name = "待开始";
	}else if(act < timestamp){
		status_key = "over";
		status_name = "已过期";
	}else{
		status_key = "except";
		status_name="异常";
	}
	
	
	var entity = status_activity_data[status_key];
	var activity_id = result.activity_id;
 	
	if(!entity){
		var activity_dict = {};
		activity_dict[activity_id] = result;
		entity = {"name":status_name, "activity_dict": activity_dict};
		result["server_list"] = [];
		status_activity_data[status_key] = entity;
	}
	
	if(!entity.activity_dict[activity_id]){
		entity.activity_dict[activity_id] = result;
		result["server_list"] = [];
	}
	
	var server_list = entity.activity_dict[activity_id].server_list;
	
	/*server_id 转 名称 */
	var server_name = server_id;
	var is_find = false;
	for(var group_item in group_server_list){
		group_item = group_server_list[group_item];
		for(var server_item in group_item.server_list){
			server_item = group_item.server_list[server_item];
			if(server_id == server_item.id){
				server_name = server_item.name;
				is_find = true;
				break;
			}
		}
		if(is_find)
			break;
	}
	server_list.push(server_name);
	
	display(status_activity_data);
	return true;
}

function get_status_server_count(status_key){
	var entity = status_activity_data[status_key];
	var count = 0;
	if(entity){
		if(entity.activity_dict){
			for(var activity_key in entity.activity_dict){
				var server_list = server_list = entity.activity_dict[activity_key].server_list;
				if(server_list){
					count += server_list.length;
				}
			}
		}
	}
	return count;
}

function display(status_activity_data){
	
	var runing_count = get_status_server_count('runing');
	var ready_count = get_status_server_count('ready');
	var reset_count = get_status_server_count('reset');
	var except_count = get_status_server_count('except');
	var over_count = get_status_server_count('over');
	var err_list = [];
	for(var server_id in err_server_list){
		server_id = err_server_list[server_id];
		var is_find= false;
		for(var group_item in group_server_list){
			group_item = group_server_list[group_item];
			for(var server_item in group_item.server_list){
				server_item = group_item.server_list[server_item];
				if(server_id == server_item.id){
					err_list.push(server_item.name);
					is_find = true;
					break;
				}
			}
			if(is_find)
				break;
		}
	}
	
	 
	var pass_count = server_count - (runing_count + ready_count + reset_count + except_count + over_count);
	window.load_gm_template("check_exchange_active/index").done(function(tpl){
		$(".data_list_content").remove();
		var doTpl = doT.template(tpl);
		var container = doTpl({
				server_count:server_count,
				runing_count:runing_count,
				ready_count:ready_count,
				reset_count:reset_count,
				over_count:over_count,
				except_count:except_count,
				pass_count:pass_count,
				err_list:err_list,
				data_dict:status_activity_data
			});
		$(".form").after(container);
	});
}
