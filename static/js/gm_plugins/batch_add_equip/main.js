$(document).ready(function(){
	if (current_page != 'gm_post'){
	 	return;
	}
	$("input[name='player_id']").after('<textarea id="player_id_list" placeholder="角色ID:111,2222,333,444,555" ></textarea>');
	$("input[name='player_id']").remove();
	 
	var equip_list = $("input[name='equip_list']");
	equip_list.after([
	 	'<textarea id="equip_list" placeholder="装备ID" ></textarea><input type="button" id="cfg_equip" onclick="cfg_equip()" value="配置" />',
	 	'<input type="button" id="batch_post" value="发送" onclick="do_post()" /> ',
	 	'<div style="display:none" id="equip_cfg_container"  ></div>'
	 ].join('<br/>'));
	 
	equip_list.remove();
	 
	$(".bottom-buttons").hide();
	
});

var id_list = [];
var err_list = [];
var error_count = 0;

function do_post(){
	err_list = [];
	error_count = 0;
	id_list = $("#player_id_list").val();
	var server_list = $("input[flag='batch_server_id']:checked");
	if(server_list.length == 0){
		alert('没有选择服务器!');
		return;
	}
	var server_id = $(server_list[0]).val();
	try{
		id_list = eval('[' + id_list.replace('，', ',') + ']');
	}catch(ex){
		alert('角色ID 填写错误！');
		return;
	}
	
	var equip_list = $("#equip_list").val();
	
	post_data(id_list.pop(), server_id, equip_list);
}

var tip_div = $(".msg_tip_div");
var the_form = $("#gm_form");

function post_data(player_id, server_id, equip_list){
	if (!player_id){
		if (err_list.length != 0 && error_count <= 5){
			error_count ++;
			id_list = err_list;
			err_list = [];
			post_data(id_list.pop(), server_id);
			return;
		}
		if (err_list.length != 0){
			$("#player_id_list").val(err_list.join(','));
		}else{
			$("#player_id_list").val('');
		}
		alert('全部完成,文本框上如果还有值,那么是失败的角色ID.');
		return;
	}
	
	var url = the_form.attr('action');
	if (-1 == url.indexOf('?')){
		url += '?';
	}else{
		url += "&";
	}
	url += "ajax=1";
	var param = GetJSON("#gm_form");
	
	param['server_id'] = server_id;
	param['player_id'] = player_id;
	param['equip_list'] = equip_list;
	
	var options = {
		type : "post",
		url : url,
		contentType : "application/x-www-form-urlencoded; charset=utf-8",
		data : param,
		success : function(result) {
			if(result.indexOf('成功') != -1){
				tip_div.html(tip_div.html() + "<p>角色ID:" + player_id +",结果:" + result + "</p>");
			}else{
				err_list.push(player_id);
			}
			post_data(id_list.pop(), server_id, equip_list);
		},
		cache : false,
		timeout : 20000,
		error : function(msg) {
			var error_msg = "<p>链接超时！player_id:" + server_id  + "时出错！</p>";
			tip_div.html(tip_div.html() + error_msg);
			err_list.push(player_id);
			post_data(id_list.pop(), server_id, equip_list);
		}
	}
	$.ajax(options);
}


function cfg_equip(){
	var container = $("#equip_cfg_container");
	
	window.load_gm_template('batch_add_equip/add_equip').done(function(tpl){
		
		var add_equip_tpl = doT.template(tpl);
		var equip_list = [];
		
		try{
			var equip_list_array = eval($("#equip_list").val());
			for(var i = 0; i < equip_list_array.length; i ++){
				var item = equip_list_array[i];
				equip_list.push({equip_id:item[0], equip_level:item[1], equip_num:item[2]});
			}
		}catch(ex){
			equip_list = [];
		}
		var equip_container = $(add_equip_tpl());
		container.append(equip_container);
		
		var equip_list_container = equip_container.find('#equip_list_container');
		
		window.load_gm_template('batch_add_equip/equip_item').done(function(tpl){
			
			var equip_item_tpl = doT.template(tpl);
			
			for(var i=0;i <equip_list.length; i++){
				var item = equip_list[i];
				
				var item_html = equip_item_tpl({equip_id:item.equip_id, equip_level:item.equip_level, equip_num:item.equip_num});
				equip_list_container.append(item_html);
				
			}
			
			var save_btn = equip_container.find('.btn_save_equip');
			var add_btn = equip_container.find('.btn_add_equip');
			
			var dia = container.dialog({title:"装备设置",close:function(){equip_container.remove()}});
			
			save_btn.bind('click',function(){
				var equip_item_list = equip_list_container.find('div.item');
				
				var save_equip_list_str = '[';
				var is_first = true;
				for(var i=0; i < equip_item_list.length; i++){
					var item = $(equip_item_list[i]);
					try{
						var equip_id = item.find('input[name="equip_id"]').val();
						var equip_level = item.find('input[name="equip_level"]').val();
						var equip_num = item.find('input[name="equip_num"]').val();
						
						if(equip_id == '' || equip_level == '' || equip_num == ''){
							continue;
						}
						
						equip_id = parseInt(equip_id);
						equip_level = parseInt(equip_level);
						equip_num = parseInt(equip_num);
						var tmp_str = [equip_id, equip_level, equip_num];
						if (!is_first){
							tmp_str = ',[' + tmp_str.join(',') + ']';
						}else{
							tmp_str = '[' + tmp_str.join(',') + ']';
							is_first = false;
						}
						save_equip_list_str += tmp_str;
						
					}catch(ex){
						continue;
					}
					
				}
				save_equip_list_str += ']';
				var r = /\[(\[\d+,\d+,\d+\],?)+\]/gi;
				if (save_equip_list_str.match(r)){
					r = /\[\d+,\d+,\d+\]/gi;
					var equip_len =  save_equip_list_str.match(r).length;
					var equip_tip = $("#equip_tip");
					if(!equip_tip.length){
						equip_tip = $('<span id="equip_tip"></span>');
						$("#equip_list").after(equip_tip);
					}
					equip_tip.text('共'+equip_len+'种物品');
					$("#equip_list").val(save_equip_list_str);
				}else{
					alter('配置错误');
				}
			});
			
			add_btn.bind('click', function(){
				var item_html = equip_item_tpl({equip_id:"", equip_level:"", equip_num:""});
				equip_list_container.append(item_html);
				dia.resetPos();
			});
			
		});
		
		
	});
	
}
