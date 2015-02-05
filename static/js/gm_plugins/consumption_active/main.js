var consumption_editor = function() {
	 
	var active_item_tpl = null;
	var goods_item_tpl = null;
	var task_list = [];
	var do_add_item = function (data_item){
		var that = this;
		if (!data_item){
			data_item = {title:'',pid:'',amount:'',gold:'', goods:[]};
		}
		
		var html = active_item_tpl({title:data_item.title, pid:data_item.pid, amount: data_item.amount, gold:data_item.gold});
		html = $(html);
		$(".consumption_active_list").append(html);
		
		var goods_len = data_item.goods.length;
		var goods_list = data_item.goods;
		for(var i = 0; i < goods_len; i ++){
			var goods_item = goods_list[i];
			add_goods(html, goods_item);
		}
		
		var btn_add_goods = html.find('.btn_add_goods');
		btn_add_goods.bind('click', function(){
			add_goods(html);
		});
	}
	
	var add_item = function(data_item){
		//if (active_item_tpl == null){
			window.load_gm_template('consumption_active/consumption_active_item').done(function(tpl){
				active_item_tpl = doT.template(tpl);
				//if(goods_item_tpl == null){
					window.load_gm_template('consumption_active/goods_item').done(function(tpl){
						goods_item_tpl = doT.template(tpl);
						do_add_item(data_item);
						
					});
				//}
			}); 
		//}
		//if (null == goods_item_tpl)
			//return;
		//do_add_item(data_item);
	}
	
	var add_goods = function(container, data_item){
		if(!data_item){
			data_item = {goods_type:1, id:''};
		}
		var goods_list_container = container.find('#goods_list_container');
		var goods_item_html = goods_item_tpl({goods_type:data_item.goods_type, id:data_item.id});
		goods_list_container.append(goods_item_html);
	}
	
	
	
	var save = function(that){
		
		var data_list = [];
		
		var item_list = container = $("#consumption_active_container").find('div.item');
		var len = item_list.length;
		for(var i = 0; i < len; i ++){
			var ele = $(item_list[i]);
			var title = ele.find('input[name="title"]').val();
			var pid = ele.find('input[name="pid"]').val();
			var amount = ele.find('input[name="amount"]').val();
			var gold = ele.find('input[name="gold"]').val();
			var goods = [];
			var goods_ele_list = ele.find('#goods_list_container .goods_item');
			var g_len = goods_ele_list.length;
		 
			gold = parseInt(gold);
			amount = parseInt(amount);
			pid = parseInt(pid);
			
			if (gold<0 || amount<0 || pid<0||  amount == ''){
				continue;
			}
			
			for(var k = 0 ; k < g_len; k ++){
				var g_item = $(goods_ele_list[k]);
				var goods_type = g_item.find("select[name='goods_type']").val();
				var id = g_item.find('input[name="id"]').val();
				
				goods_type = parseInt(goods_type);
				id = parseInt(id);
				if (id == '' )
					continue;
				
				goods.push({goods_type:goods_type,id:id});
				
			}
			if ('' == gold){
				continue;
			}
			
			data_list.push({gold:gold, amount:amount, pid:pid, title: title, goods:goods});
		}
		
		 
		var pid_list = [];
		var an_list = [];
		var arl_list = [];
		var gn_list = [];
		var apl_list = [];
		
		for(var index in data_list){
			var item = data_list[index];
			pid_list.push(item.pid);
			an_list.push(item.amount);
			var goods = item.goods;
			var len = goods.length;
			
			var goods_array = [];
			for (var i = 0 ; i < len; i++){
				var goods_item = goods[i];
				goods_array.push([goods_item.goods_type, goods_item.id]);	
			}
			gn_list.push(item.title);
			apl_list.push(item.gold);
			arl_list.push(goods_array);
		}
		
		var pid_ele = $("#gm_form textarea[field_key='pid']");
		var an_ele = $("#gm_form textarea[field_key='an']");
		var arl_ele = $("#gm_form textarea[field_key='arl']");
		var gn_ele = $("#gm_form textarea[field_key='gn']");
		var apl_ele = $("#gm_form textarea[field_key='apl']");
		
		pid_ele.val(JSON.stringify(pid_list));
		an_ele.val(JSON.stringify(an_list));
		arl_ele.val(JSON.stringify(arl_list));
		gn_ele.val(JSON.stringify(gn_list));
		apl_ele.val(JSON.stringify(apl_list));
		
		pid_ele.attr('name', 'pid');
		an_ele.attr('name', 'an');
		arl_ele.attr('name', 'arl');
		gn_ele.attr('name', 'gn');
		apl_ele.attr('name', 'apl');
		
	}
	
	this.show = function(container){
		var that = this; 
		if(!container)
		{
			window.load_gm_template("consumption_active/consumption_active").done(function(tpl){
				var doTpl = doT.template(tpl);
				container = doTpl();
				$("body").append(container);
				container = $("#consumption_active_container");
			 	that.show(container);
			});
			return;
		}
		
		container.hide();
		
		container.find("#btn_append").bind('click', function(){
			add_item();
		});
		
		
		var pid_list = $("#gm_form textarea[field_key='pid']").val();
		var an_list = $("#gm_form textarea[field_key='an']").val();
		var arl_list = $("#gm_form textarea[field_key='arl']").val();
		var gn_list =  $("#gm_form textarea[field_key='gn']").val();
		var apl_list = $("#gm_form textarea[field_key='apl']").val();
		
		if('' != pid_list){
			pid_list = eval('(' +pid_list + ')' );
		}
		if('' != an_list){
			an_list = eval('(' +an_list + ')' );
		}
		if('' != arl_list){
			arl_list = eval('(' +arl_list + ')' );
		}
		if('' != gn_list){
			gn_list = eval('(' +gn_list + ')' );
		}
		if('' != apl_list){
			apl_list = eval('(' +apl_list + ')' );
		}
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
			add_item(data_item);
		}
		
		container.find('#btn_save').bind('click', function(){save(that)});
		
		container.dialog({title:"消费活动设置",close:function(){$("#consumption_active_container").remove();}});
	}
	
}

$(document).ready(function(){
	var editor = new consumption_editor();
	var btn = $('<input id="btn_consumption_active_config" type="button" value="配置" />');
	var target = $("#gm_form textarea[field_key='pid']");
	if(target.length <= 0)
		return;
		
	target.after(btn);
	$("#btn_consumption_active_config").live('click', function(){
		//alert('sfsdf');
		$("#consumption_active_container").remove();
		editor.show();
	});
});
