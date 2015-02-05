var GMeditor = function() {

	var ctrl_index = 0;
	var content_json = {};

	var code_path = {
		type : "list",
		name : "状态码路径:",
		json_key : "code_path",
		default_value : ["code"]
	};

	var content_path = {
		type : "list",
		name : "内容路径:",
		json_key : "content_path",
		default_value : ["content", 0]
	};
	
	var reason_phrase_path = {
		type : "list",
		name : "结果路径(可空):",
		json_key : "reason_phrase_path",
		default_value : ["reason_phrase"]
	};
 
	var check_number = function(value) {
		return value.replace(/[\.\d]+/i, '') == '';
	} 

	this.set_result_define = function(txt_target, type_enum) {
		content_json = {};
		var control_box = [code_path, content_path, reason_phrase_path];
		var txt = $(txt_target).val();
		if ($.trim(txt) != '') {
			content_json = eval('(' + txt + ')');
		}
		$('#gm_editor').remove();
		$('body').append('<div id="gm_editor" ></div>');
		var div = $('#gm_editor');
		div.css({"width":"800px", "height":"500px", "overflow":"auto"});
		if (type_enum == GMTypeEnum.form) { 
			control_box.push({type:"value", name:"保存请求路径:", json_key:"form_action"});
			control_box.push({type:"value", name:"发送类型(json):", json_key:"form_type"});
			control_box.push({type:"value", name:"发送参数:", json_key:"form_key"});
			control_box.push({type:"form_field", name:"表单内容", json_key:"form_items"});
			control_box.push({type:"server_list_chkbox", name:"服务器复选框", json_key:"server_list_chkbox"});
		} else if (type_enum == GMTypeEnum.list) {
			control_box.push({type:"list_times", name:"列表字段", json_key:"list_items"});
			control_box.push({type:"list_action", name:"行的操作", json_key:"action"});
		} else if (type_enum == GMTypeEnum.msg) { 
			control_box.push({type:"key_value", name:"返回消息:", json_key:"msg_values"});
			control_box.push({type:"key_value", name:"备注:(例数据库中的log_user保存player_id)", json_key:"desc_field_map"});
		}
		
		for (index in control_box){ 
			var tmp = control_box[index];
			add_ctrl(div, tmp);
		}
		
		div.dialog({title:"配置接收参数",
			close:function(){
				var code_path = new Array(); 
				$('#code_path input').each(function(){
					var tmp = $(this).val();
					if ($.trim(tmp) == '')
						return;
					if(check_number(tmp))
						tmp = parseInt(tmp);
					code_path.push(tmp);
				});
				content_json['code_path'] = code_path;
				
				var content_path = new Array();
				$('#content_path input').each(function(){
					var tmp = $(this).val();
					if ($.trim(tmp) == '')
						return;
					if(check_number(tmp))
						tmp = parseInt(tmp);
					content_path.push(tmp);
				});
				content_json['content_path'] = content_path;
				
				var reason_phrase_path = new Array();
				$('#reason_phrase_path input').each(function(){
					var tmp = $(this).val();
					if ($.trim(tmp) == '')
						return;
					if(check_number(tmp))
						tmp = parseInt(tmp);
					reason_phrase_path.push(tmp);
				});
				content_json['reason_phrase_path'] = reason_phrase_path;
				
				if (type_enum == GMTypeEnum.form){
					save_form(txt_target);
				}else if(type_enum == GMTypeEnum.msg){
					save_msg(txt_target);
				}else if(type_enum == GMTypeEnum.list){
					save_list(txt_target);
				}
			}
		});
	}
	
	var save_msg = function(txt_target){
		var msg_values = {};
		var desc_field_map = {};
		
		$("#msg_values div").each(function(){
			var key = '';
			var value = '';
			$(this).children("input").each(function(){
				var tmp = $(this).attr('name');
				var v = $(this).val();
				if (tmp == 'key'){
					key = v;
				}else if(tmp == 'value'){
					value = v;
				}
				
			});
			if ($.trim(key) == '')
				return;
			msg_values[key] = value;
		});
		
		$("#desc_field_map div").each(function(){
			var key = '';
			var value = '';
			$(this).children("input").each(function(){
				var tmp = $(this).attr('name');
				var v = $(this).val();
				if (tmp == 'key'){
					key = v;
				}else if(tmp == 'value'){
					value = v;
				}
				
			});
			if ($.trim(key) == '')
				return;
			desc_field_map[key] = value;
		});
		
		content_json['msg_values'] = msg_values;
		content_json['desc_field_map'] = desc_field_map;
		
		$(txt_target).val(JSON.stringify(content_json));
	}
	
	var save_list = function(txt_target){
		var action_array = new Array();
		$("#action div").each(function(){
			var title = '';
			var form_action = '';
			
			var param_list = new Array();
			$(this).children("input").each(function(){
				var tmp = $(this).attr('name');
				var value = $(this).val();
				if (tmp == 'title')
					title = value;
				
				if (tmp == 'form_action'){
					form_action = value;
				}
				
				
			});
			
			$(this).find("div").each(
				function(){
					var param_name = '';
					var value_source = '';
					$(this).children("input").each(function(){
						var tmp = $(this).attr('name');
						var value = $(this).val();
						
						if (tmp == 'param_name')
							param_name = value;
						
						if (tmp == 'value_source'){ 
							value_source = value;
						}
						
					});
					param_list.push({param_name:param_name, value_source:value_source});
				}
			);
			
			if ($.trim(title) == '')
				return;
				
			action_array.push({title:title, form_action:form_action,  param_list:param_list});
		});
		content_json['action'] = action_array;
		
		var list_items = {};
		$("#list_items div").each(function(){
			
			var key = '';
			var value = '';
			var type = '';
			var order = 0;
			
			$(this).children("input").each(function(){
				var tmp = $(this).attr('name');
				var v = $(this).val();
				if (tmp == 'key'){
					key = v;
				}else if(tmp == 'value'){
					value = v;
				}
				
				if (tmp == 'type'){
					if ('' == v)
						v = 'text';
					type = v;
				}
				
				if (tmp == 'order'){
					if(''== v)
						v = '0';
					try{
						order = parseInt(v);
					}catch(e){
						order = 0;
					}
				}
				
			});
			if ($.trim(key) == '')
				return;
			list_items[key] = {value:value, type:type, order:order };
		});
		 
		content_json['list_items'] = list_items;
		$(txt_target).val(JSON.stringify(content_json));
	}
	
	var save_form = function(txt_target){
		
		content_json['form_action'] = $('#form_action').val();
		var form_type = $('#form_type').val();
		var form_key =  $('#form_key').val();
		
		if(form_type == '' || !form_type){
			form_type = 'json';
		}
		
		if(form_key == '' || !form_key){
			form_key = 'content';
		}
		
		content_json['form_type'] = form_type;
		content_json['form_key'] = form_key;
		
		
		
		var form_items = {};
		$("#form_items div").each(function(){
			var key = '';
			var name = '';
			var is_modify = 0;
			var allow_empty = 0;
			var type = 'text';
			var order = 0;
			$(this).children("input,select").each(function(){
				var tmp = $(this).attr('name');
				var v = $(this).val();
				if (tmp == 'key'){
					key = v;
				}else if(tmp == 'name'){
					name = v;
				}else if(tmp == 'is_modify'){
					if($(this).attr('checked')){
						is_modify = 1;
					}
				}else if(tmp == 'type'){
					type = v;
				}else if(tmp == 'order'){
					try{
						order = parseInt(v);
					}
					catch(e){
						order = 0;
					}
				}else if(tmp == 'allow_empty'){
					if($(this).attr('checked')){
						allow_empty = 1;
					}
				}
			});
			if ($.trim(key) == '')
				return;
			form_items[key] = {'name':name, 'is_modify':is_modify, 'type': type, 'order':order, 'allow_empty':allow_empty};
		});
		content_json['form_items'] = form_items;
		content_json['server_list_chkbox'] = $('#server_list_chkbox').attr('checked');
		$(txt_target).val(JSON.stringify(content_json));
	}
	
	var add_ctrl = function(context, ctrl_param) {
		ctrl_index++;
		var ctrl_class = "ctrl_" + ctrl_index;
		context.append('<div class="' + ctrl_class + '"></div>');
		var content = $('.' + ctrl_class);
		if (ctrl_param.type == 'list') {
			add_list_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'key_value'){
			add_key_value_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'value'){
			add_value_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'form_field'){
			add_form_field_ctrl(context,ctrl_param);
		}else if(ctrl_param.type == 'list_action'){
			add_list_row_action_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'list_times'){
			add_list_items_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'gm_params'){
			add_gm_params_ctrl(context, ctrl_param);
		}else if(ctrl_param.type == 'server_list_chkbox'){
			add_server_list_chkbox(context, ctrl_param);
		}
	}
	
	var add_list_items_ctrl = function(context, ctrl_param){
		var list_items_container = $("<div id=" + ctrl_param.json_key + "  ></div>");
		var btn_add = $('<input type="button" value="添加" />');
		 
		context.append(list_items_container); 
		list_items_container.append(ctrl_param.name);
		list_items_container.append(btn_add);
		btn_add.bind('click', function(){
			add_list_items(list_items_container);
		});
		
		var key_value = content_json[ctrl_param.json_key];
		
		if (key_value != undefined) {
			for (key in key_value) {
				var item = key_value[key];
				var value = item.value;
				var type = item.type;
				var order = item.order;
				if (typeof(item) == 'string'){
					console.log('hellow');
					value = item;
					type = 'text';
					order = 0;	
				}
				add_list_items(list_items_container, key, value, type, order);
			}
		}
	}
	
	var add_list_items = function(list_items_container, key, value, type, order){
		if(key == undefined)
			key = '';
		if(value == undefined)
			value = '';
		if(type == undefined)
			type = 'text';
		if(type == undefined)
			order = 0;
		
		div = $('<div></div>');
		//div.css({"float":"left"});
		list_items_container.append(div);
		var txt_key = $('<input type="text" name="key" class="input_key" />');
		var txt_value = $('<input type="text" name="value" class="input_value" />');
		var sel_type = $("<select name='type'  ><option value='text' >字符串</option><option value='textarea' >文本域</option><option value='int' >整数</option><option value='number' >数字</option><option value='array' >数组</option><option value='json' >json</option><option value='timestamp' >时间戳</option><option value='boolean' >布尔</option></select>");
		var txt_order = $("<input type='order' name='order' class='input_value' />");
		
		div.append("键:");
		div.append(txt_key);
		div.append("值");
		div.append(txt_value);
		div.append("类型");
		div.append(sel_type);
		div.append("排序");
		div.append(txt_order);
		
		txt_key.val(key);
		txt_value.val(value);
		
		sel_type.val(type);
		txt_order.val(order);
		
	}
	
	var add_list_row_action_ctrl = function(context, ctrl_param){
		var list_row_action_container = $("<div id=" + ctrl_param.json_key + "  ></div>");
		var btn_add = $('<input type="button" value="添加" />'); 
		context.append(list_row_action_container);
		list_row_action_container.append(ctrl_param.name);
		list_row_action_container.append(btn_add);
		btn_add.bind('click', function(){
			add_list_row_action(list_row_action_container);
		}); 
		var key_value = content_json[ctrl_param.json_key];
		if (key_value != undefined) {
			for (key in key_value) {
				var item = key_value[key];
				add_list_row_action(list_row_action_container, item.title, item.form_action, item.param_list);
			}
		}
	}
	
	
	var add_list_row_action = function(list_row_action_container, title, form_action, param_list){
		if (title == undefined)
			title = '';
		if (form_action == undefined)
			form_action = '';
		if (param_list == undefined)
			param_list = [];
		
		var div = $('<div></div>');
		var txt_title = $('<input type="text" name="title" class="input_value" />');
		var txt_form_action = $('<input type="text" name="form_action"  />');
		  
		list_row_action_container.append(div);
		
		div.append("标题:");
		div.append(txt_title);
		div.append("url:");
		div.append(txt_form_action);
		
		var param_list_len = param_list.length;
		for(var i = 0; i < 5;i++){
			var param_div = $('<div></div>');
			var txt_param_name = $('<input type="text" name="param_name"  class="input_value" />');
			var txt_value_source = $('<input type="txt" name="value_source" class="input_value"  />');
			div.append(param_div);
			param_div.append("参数名:");
			param_div.append(txt_param_name);
			param_div.append("值来源key:");
			param_div.append(txt_value_source);
			
			if (param_list_len > i){
				txt_param_name.val(param_list[i].param_name);
				txt_value_source.val(param_list[i].value_source);
			}
			
		}
		
		txt_title.val(title);
		txt_form_action.val(form_action);
		
	}
	
	var add_form_field_ctrl = function(context, ctrl_param){
		var form_field_container = $("<div id=" + ctrl_param.json_key + " class='form_field_container_" + ctrl_index + "' ></div>");
		var btn_add = $('<input type="button" value="添加" />');
		context.append(ctrl_param.name);
		context.append(btn_add);
		context.append(form_field_container);
		
		btn_add.bind('click',function(){
			add_form_field(context, form_field_container);
		});
		
		var key_value = content_json[ctrl_param.json_key];
		if (key_value != undefined) {
			for (key in key_value) {
				var item = key_value[key];
				add_form_field(context, form_field_container, key, item);
			}
		}
	}
	
	var add_form_field = function(context, form_field_container, key, item){
		if (key == undefined)
			key = '';
		if (item == undefined)
			item = {};
		
		var div = $("<div></div>");
		var txt_key = $("<input type='text' name='key' class='input_key' />");
		var txt_name = $("<input type='text' name='name' class='input_value' />");
		var chk_modify = $("<input name='is_modify'  type='checkbox'  />");
		var sel_type = $("<select name='type'  ><option value='auto_timestamp'>自动生成时间戳</option><option value='text' >字符串</option><option value='textarea' >文本域</option><option value='int' >整数</option><option value='number' >数字</option><option value='array' >数组</option><option value='json' >json</option><option value='timestamp' >时间戳</option><option value='boolean' >布尔</option></select>");
		var order = $("<input type='order' name='order' class='input_value' />");
		var chk_allow_empty = $("<input name='allow_empty' type='checkbox' />"); 
		
		form_field_container.append(div);
		div.append('键:');
		div.append(txt_key);
		div.append('名称:');
		div.append(txt_name);
		div.append('可修改');
		div.append(chk_modify);
		div.append('类型');
		div.append(sel_type);
		div.append('排序');
		div.append(order);
		div.append('允许空值显示');
		div.append(chk_allow_empty);
		
		txt_key.val(key);
		txt_name.val(item.name);
		
		if (item.is_modify == 1){
			chk_modify.attr('checked', true);
		}
		
		if (item.allow_empty == 1){
			chk_allow_empty.attr('checked', true);
		}
		
		order.val(item.order);
		sel_type.val(item.type);
	}
	
	/*表单 是否保存到各个服务器上*/
	var add_server_list_chkbox = function(context, ctrl_param){
		var chk_server = $("<input type='checkbox' name='server_list' id='server_list_chkbox' />");
		var value = content_json[ctrl_param.json_key];
		
		context.append('服务器复选框：');
		context.append(chk_server);
		chk_server.attr('checked', value);
	}
	
	var add_value_ctrl = function(context, ctrl_param){
		var key_value_container = $("<div  class='value_container_" + ctrl_index + "' ></div>");
		
		var value = content_json[ctrl_param.json_key];
		
		var txt_value = $("<input id='"+ ctrl_param.json_key +"' type='text' />");
		if (value != undefined) {
			txt_value.val(value);
		}
		
		context.append(key_value_container);
		context.append(ctrl_param.name);
		context.append(txt_value);
	}
	
	var add_key_value_ctrl = function(context, ctrl_param){
		var txt_key = $("<input type='text' class='input_key' />");
		var txt_value = $("<input type='text' class='input_value' />"); 
		var btn_add = $("<input type='button' value='添加' /> ");
		var key_value_container = $("<div id=" + ctrl_param.json_key + " class='key_value_container_" + ctrl_index + "' ></div>");
		context.append(ctrl_param.name);
		context.append('键:');
		context.append(txt_key);
		context.append('值:');
		context.append(txt_value);
		context.append(btn_add);
		context.append(key_value_container);
		
		btn_add.bind('click', function(){
			add_key_value(key_value_container, txt_key.val(), txt_value.val());
		});
		
		var key_value = content_json[ctrl_param.json_key];
		if (key_value != undefined) {
			for (key in key_value) {
				var value = key_value[key];
				add_key_value(key_value_container, key, value);
			}
		}
	}
	
	var add_key_value = function(key_value_container, key, value){
		if (key == undefined)
			key = ''
		if (value == undefined)
			value = ''
		var div = $("<div></div>");
		key_value_container.append(div);
		
		var txt_key = $("<input type='text' name='key'   class='input_key' />");
		var txt_value = $("<input type='text' name='value'  class='input_value' />");
		div.append('键:');
		div.append(txt_key);
		div.append('值:');
		div.append(txt_value);
		txt_key.val(key);
		txt_value.val(value);
	}
	
	var add_list_ctrl = function(context, ctrl_param){
		var txt_01 = $("<input type='text' class='input_int' />");
		var btn_01 = $("<input type='button' value='添加' />");
		var list_container = $("<div id=" + ctrl_param.json_key  + " class='list_container_" + ctrl_index + "' ></div>");
		context.append(ctrl_param.name);
		context.append(txt_01);
		context.append(btn_01);
		context.append(list_container); 
		btn_01.bind('click', {list_container:list_container, text_box:txt_01}, list_ctrl_add_button_handler);
		
		var value_list = content_json[ctrl_param.json_key];
		
		if (value_list != undefined) {
			for (index in value_list) {
				var value = value_list[index];
				add_list_ctrl_value(list_container, value);
			}
		}else{
			if(ctrl_param.default_value){
				for(index in ctrl_param.default_value){
					var item = ctrl_param.default_value[index];
					add_list_ctrl_value(list_container, item);
				}
			}
		}
	}
	
	var list_ctrl_add_button_handler = function(e){
		add_list_ctrl_value(e.data.list_container, $(e.data.text_box).val());
	}
	
	var add_list_ctrl_value = function(list_container, value) {
		var list_item = $("<input type='text' class='input_int' />");
		list_item.val(value);
		$(list_container).append(list_item);
	}
	
	
	/* 以下是配置  发送参数  */
	var param_json = {}
	this.set_params = function(txt_target, type_enum){
		param_json = {};
		var control_box = [];
		var txt = $(txt_target).val();
		if ($.trim(txt) != '') {
			param_json = eval('(' + txt + ')');
		}
		$('#gm_params_editor').remove();
		$('body').append('<div id="gm_params_editor" ></div>');
		var div = $('#gm_params_editor');
		div.css({"width":"820px", "height":"500px", "overflow":"auto"});
		
		control_box.push({type:"gm_params", name:"发送参数:", json_key:"gm_params_content"});
		
		for (index in control_box){ 
			var tmp = control_box[index];
			add_ctrl(div, tmp);
		}
		
		div.dialog({title:"配置协议参数", close:function(){
			param_json = {};
			$("#gm_params_content div").each(function(){
				var key = '';
				var name = '';
				var value_map = {};
				var type = '';
				var method = '';
				var value = '';
				var json_name = '';
				var postback = 0;
				var required = 0;
				$(this).children("input, select").each(function(){
					var tmp = $(this).attr('name');
					var v = $(this).val();
					if (tmp == 'key'){
						key = v;
					}else if(tmp == 'name'){
						name = v;
					}else if(tmp == 'value_map'){
						value_map = v;
					}else if(tmp == 'type'){
						type = v;
					}else if(tmp == 'method'){
						method = v;
					}else if(tmp == 'value'){
						value = v;
					}else if(tmp == 'json_name'){
						json_name = v;
					}else if(tmp == 'postback'){
						if($(this).attr('checked')){
							postback = 1;
						}
					}else if(tmp == 'required'){
						if($(this).attr('checked')){
							required = 1;
						}
					}
					
				});
				if ($.trim(key) == '')
					return;
				param_json[key] = {"name":name, "type":type, "value_map": value_map,"method":method, "value":value, "json_name": json_name,"postback":postback, "required": required};
			});
			
			$(txt_target).val(JSON.stringify(param_json));
		}});		
	}
	
	var add_gm_params_ctrl = function(context, ctrl_param){
		var container  = $("<div id=" + ctrl_param.json_key + " ></div>");
		var btn_add = $("<input type='button' value='添加' />");
		context.append(container);
		container.append(ctrl_param.name);
		container.append(btn_add);
		
		btn_add.bind('click', function(){
			add_gm_params(container);
		});
		
		
		for (key in param_json) {
			var item = param_json[key];
			add_gm_params(container, key, item.name, item.value_map, item.type, item.method, item.value, item.json_name,item.postback, item.required);
		}
		 
	}
	
	var add_gm_params = function(gm_params_ctrl_container, key, name, value_map,type, method, value, json_name, postback, required){
		if (key == undefined)
			key = '';
		if (name == undefined)
			name = '';
		if (value_map == undefined)
			name = '';
		if (type == undefined)
			type = 'string';
		if (name == undefined)
			name = '';
		if (method == undefined)
			method = 'get';
		if (value == undefined)
			value = '';
		if (postback == undefined)
			postback = 0;
			
		if (required == undefined)
			required = 0;
		
		var div = $("<div style='background-color:#D4D9E4; margin-bottom:10px;' ></div>");
		var txt_key = $("<input type='text' name='key' class='input_value' />");
		var txt_name = $("<input type='text' name='name' class='input_value' />");
		var txt_value = $("<input type='text' name='value' class='input_value' />");
		var dbl_type = $("<select name='type' ><option value='int' >int</option><option value='string' >string</option><option value='text' >text</option><option value='boolean' >boolean</option></select>");
		var dbl_method = $("<select name='method' ><option value='get' >get</option><option value='post' >json</select>");
		var txt_json_name = $("<input type='text' name='json_name' class='input_value' />");
		var txt_value = $("<input type='text' name='value' class='input_value' />");
		var chk_postback = $("<input type='checkbox' name='postback' />");
		var txt_value_map = $("<input type='text' name='value_map' class='input_value' /> "); 
		var chk_required = $("<input type='checkbox' name='required' />");
		
		gm_params_ctrl_container.append(div);
		
		
		div.append("参数名:");
		div.append(txt_key);
		div.append("值:");
		div.append(txt_value);
		div.append("显示标题:");
		div.append(txt_name);
		div.append("类型:");
		div.append(dbl_type);
		div.append("对应值(JSON格式)");
		div.append(txt_value_map);
		
		div.append("发送类型:");
		div.append(dbl_method);
		div.append("json参数名:");
		div.append(txt_json_name); 
		div.append("重用参数:");
		div.append(chk_postback);
		
		div.append("必须参数:");
		div.append(chk_required);
		
		// var tmp_controls = [];
		// tmp_controls.push({"name":"参数名", "control":txt_key});
		// tmp_controls.push({"name":"值", "control":txt_value});
		// tmp_controls.push({"name":"显示标题", "control":txt_name});
		// tmp_controls.push({"name":"发送类型", "control":dbl_method});
		// tmp_controls.push({"name":"json参数名", "control":txt_json_name});
		// tmp_controls.push({"name":"回传", "control":chk_postback});
// 		
		// div.append(add_to_table(tmp_controls, 4));
		txt_key.val(key);
		txt_name.val(name);
		txt_value_map.val(value_map);
		dbl_type.attr("value",type);
		dbl_method.attr("value", method);
		txt_json_name.val(json_name)
		txt_value.val(value);
		if(postback == 1)
			chk_postback.attr("checked", true);
		
		if(required == 1)
			chk_required.attr("checked", true);
	}
	
	var add_to_table = function(controls, cols){
		var content = $('<table style="border:0px;" ></table>');
		var row = $("<tr></tr>");
		content.append(row);
		var cur = row;
		for (index in controls){
			var row_index = parseInt(index) + 1;
			var item = controls[index];
			if (0 == row_index % cols){
				row = $("<tr></tr>");
				content.append(row);
				cur = row;
			}
			
			cur.append($("<td style='text-align:right;' >" + item.name + "</td>"));
			cur.append($("<td></td>").append(item.control));
		}
		return content;
	}
}

var GMTypeEnum = {
	form : 0,
	list : 1,
	msg : 2
}