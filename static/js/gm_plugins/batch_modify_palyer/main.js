var the_form = $("#gm_form");
$(document).ready(function(){
	 if (current_page != 'gm_post'){
	 	return;
	 }
	
	 var ctrl_list = [
	 	'<textarea id="player_id_list" ></textarea>',
	 	'<input type="button" id="batch_post" value="发送" onclick="do_post()" /> '
	 ];
	  
	  player_controls = [
		'金币：<input data-name="gl" value="0" /> ',
		'银币：<input data-name="sl" value="0" /> ',
		'军工：<input data-name="jg" value="0" /> ',
		'军令：<input data-name="jl" value="0" /> '
		]
	  
	  var ctr_player_info =  $("input[name='edited_player_info']");
	  ctr_player_info.after(player_controls.join('<br/>'));
	  ctr_player_info.remove();
	  
	  var ctr_player_id = $("input[name='player_id']");
	  ctr_player_id.after(ctrl_list.join('<br/>'));
	  ctr_player_id.remove();
	  $(".bottom-buttons").hide();
	  // $("#batch_post").bind('click', function(){
// 			
	  // });
	  
});
var id_list = [];
var err_list = [];
var error_count = 0;

var tip_div = $(".msg_tip_div");

function do_post(){
	err_list = [];
	tip_div.html('');
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
	
	var post_param = GetJSON("#gm_form");
	
	post_param['server_id'] = server_id;
	var player_info = {};
	var gl = parseInt($('input[data-name="gl"]').val());
	var sl = parseInt($('input[data-name="sl"]').val());
	var jg = parseInt($('input[data-name="jg"]').val());
	var jl = parseInt($('input[data-name="jl"]').val());
	 
	if (!isNaN(gl)) player_info['gl'] = gl; else {alert('金币格式错误');return;};
	if (!isNaN(sl)) player_info['sl'] = sl; else {alert('银币格式错误');return;};
	if (!isNaN(jg)) player_info['jg'] = jg; else {alert('军工格式错误');return;};
	if (!isNaN(jl)) player_info['jl'] = jl; else {alert('军令格式错误');return;};
	
	post_param['edited_player_info'] = JSON.stringify(player_info);
	
	post_data(id_list.pop(), post_param);
}


function post_data(player_id, post_param){
	if (!player_id){
		if (err_list.length != 0 && error_count <= 5){
			error_count ++;
			id_list = err_list;
			err_list = [];
			post_data(id_list.pop(), post_param);
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
	param = $.extend(post_param, {'player_id':player_id});
	
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
			post_data(id_list.pop(), post_param);
		},
		cache : false,
		timeout : 20000,
		error : function(msg) {
			var error_msg = "<p>链接超时！player_id:" + server_id  + "时出错！</p>";
			tip_div.html(tip_div.html() + error_msg);
			err_list.push(player_id);
			post_data(id_list.pop(), post_param);
		}
	}
	$.ajax(options);
}
