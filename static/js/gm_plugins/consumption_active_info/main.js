var _activity_dict = {};
$(document).ready(function(){
	if(!field_key_dic['asc']){
		return;
	}
	
	var asc = field_key_dic['asc'];
	asc = eval('(' + asc + ')');
	
	var rsl = field_key_dic['rsl']; //正在运行活动中的服务器ID
	rsl = eval('('+rsl+')');
	var rsl_len = rsl.length;
	var ssl = field_key_dic['ssl']; //还没开始活动的服务器ID
	ssl = eval('('+ssl+')');
	var ssl_len = ssl.length;
	var nesl = field_key_dic['nesl']; //获取活动状态网络错误的服务器ID
	nesl = eval('('+nesl+')');
	var nesl_len = nesl.length;
	
	/* 一个活动配置    对应  服务器列表           1对多的一个映射      */
	var rsl_dict = {};
	var ssl_dict = {};
	//var nesl_dict = {};
	var nomal_dict = {};//未知状态的dict
	
	
	for(var key in asc){
		var activity = asc[key];
		_activity_dict[activity.activity_id] = activity;
		var task_list = [
			{"server_list":rsl, "dict":rsl_dict},
			{"server_list":ssl, "dict":ssl_dict},
			//{"server_list":nesl, "dict":nesl_dict}
		];
		f(task_list, key, asc, nomal_dict);
	}
	
	show_activity_list(rsl_dict, ssl_dict, nomal_dict);
});

function show_activity_list(rsl_dict, ssl_dict,  nomal_dict){
	
	var activity_list = [];
	activity_list.push({"activity_dict":rsl_dict, "status":"正在执行中"});
	activity_list.push({"activity_dict":ssl_dict, "status":"等待执行"});
	//activity_list.push({"activity_dict":nesl_dict, "status":"检测状态网络错误"});
	activity_list.push({"activity_dict":nomal_dict, "status":"未知状态"});
	
	var target = $('[data-target="asc"]');
	window.load_gm_template("consumption_active_info/activity_list").done(function(tpl){
		var doTpl = doT.template(tpl);
		var list = doTpl({"activity_list":activity_list});
		target.html(list);
	});
}

function f(status_list, key, asc, nomal_dict){
	if(status_list.length == 0){
		var activity = asc[key];
			
		var new_item = nomal_dict[activity.activity_id];
		if(!new_item){
			new_item = {"activity":activity, "server_list":[]};
		}
		new_item.server_list.push(key);
		nomal_dict[activity.activity_id] = new_item;
		return;
	}
	
	var target = status_list.pop();
	var server_list = target.server_list;
	var dict = target.dict;
	var len = server_list.length;
	while(len){
		len--;
		var server_id = server_list[len];
		key = parseInt(key);
		if (server_id == key){
			
			
			var activity = asc[key];
			
			var new_item = dict[activity.activity_id];
			if(!new_item){
				new_item = {"activity":activity, "server_list":[]};
			}
			new_item.server_list.push(key);
			dict[activity.activity_id] = new_item;
			return;
		}
	}
	f(status_list, key, asc, nomal_dict);
}


function show_info(activity_id){
	var activity = _activity_dict[activity_id];
	
	var display_list = [];
	
	var pid_list = activity.pid;
	var an_list = activity.an;
	var arl_list = activity.arl;
	var gn_list =  activity.gn;
	var apl_list = activity.apl;
	
	var len = apl_list.length;
	for(var i =0; i <len;i++ ){
		goods_list = arl_list[i];
		goods = [];
		var g_len = goods_list.length;
		for(var k = 0; k <g_len; k++ ){
			var goods_item = goods_list[k]
			goods.push({goods_type:goods_item[0], id:goods_item[1]});
		}
		var gold = apl_list[i];
		data_item = {title:gn_list[i], pid:pid_list[i], amount:an_list[i], gold:gold, goods:goods};
		display_list.push(data_item);
	}
	 
	
	window.load_gm_template("consumption_active_info/info").done(function(tpl){
		
		var doTpl = doT.template(tpl);
		var container = doTpl({"list":display_list});
		$("body").append(container);
		
		container = $("#consumption_active_list_container");
		
		container.dialog({title:"消费活动详细",close:function(){$("#exchange_active_list_container").remove();}});
		
	});
}

function timestamp_to_time_str(timestamp){
	var unixTimestamp = new Date(timestamp*1000) ;
	var commonTime = unixTimestamp.toLocaleString();
	return commonTime;
}
