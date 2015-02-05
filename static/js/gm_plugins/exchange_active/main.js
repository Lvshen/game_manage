var exchange_editor = function() {
	
	this.old_gold_dict = {};/* 原始数据 */
	this.new_gold_dict = {};
	
	var add_item = function (data_item){
		if (!data_item){
			data_item = {gold:'', goods_type:1, id:''};
		}
		
		window.load_gm_template('exchange_active/exchange_active_item').done(function(tpl){
			var doTpl = doT.template(tpl);
			var html = doTpl({gold:data_item.gold, goods_type:data_item.goods_type, id:data_item.id});
			$(".exchange_active_list").append(html);
		});	
	}
	
	var check_update = function(that){
		var modify = false;
		var len = 0;
		for(var item in that.old_gold_dict){
			len ++;
			var new_gift_list = that.new_gold_dict[item];
			if(!new_gift_list){
				modify = true;
				break;
			}
			var old_gift_list = that.old_gold_dict[item];
			var new_gift_list_len = new_gift_list.length;
			
			if(old_gift_list.length != new_gift_list_len){
				modify = true;
				break;
			}
			
			while(new_gift_list_len){
				new_gift_list_len --;
				var new_goods_item = new_gift_list[new_gift_list_len];
				var old_goods_item = old_gift_list[new_gift_list_len];
				if (new_goods_item[0] != old_goods_item[0]){
					modify = true;
					break;
				}
				if(new_goods_item[1] != old_goods_item[1]){
					modify = true;
					break;
				}
			}
		}
		if (0 == len)
			modify = true;
		return modify;
	}
	
	var save = function(that){
		var item_element_list = $(".exchange_active_list div.item");
		var len = item_element_list.length;
		
		var gold_dict = {};//key积分：value得到礼包[]
		for(var i= 0 ; i < len;i++){
			var item_element = $(item_element_list[i]);
			var gold = item_element.find('input[name="gold"]').val();
			gold = gold.trim();
			var gift_array = gold_dict[gold];
			if (!gift_array)
				gift_array = [];
			
			var goods_type = item_element.find('select[name="goods_type"]').val().trim();
			var id = item_element.find("input[name='id']").val().trim();
			 
			goods_type = parseInt(goods_type);
		 	gold = parseInt(gold);
		 	id = parseInt(id);
		 	
			if (gold < 0 || goods_type < 0 || id < 0){
				continue;
			}
			
			gift_array.push({goods_type:goods_type, id:id});
			gold_dict[gold] = gift_array;
		}
		that.new_gold_dict = gold_dict;
		
		/* 拆分为要保存的 2组数组 ....*/
		/*
			lock like...
			这是礼包列表[ [[1,10022],[2,10033],[1,20033]]], [[1,200]], [2,100]],  [[1,200]] ]
			礼包里又有一个个礼品数组
			
			触发获得礼品的金币数组[600,1000,1200]
			
			分别3个金币额度触发 3种礼品包
		*/
		
		var gold_list = [];
		var gift_list = [];
		for (var key in gold_dict){
			/* 礼包 里的礼品数组  */
			var gift_item_array = gold_dict[key];
			
			var goods_list = [];
			for(var tmp in gift_item_array){
				var item = gift_item_array[tmp];
				goods_list.push([item.goods_type, item.id]);
			}
			gold_list.push(parseInt(key));
			gift_list.push(goods_list);
		}
		
		
		
		$("#gm_form textarea[field_key='arl']").val(JSON.stringify(gift_list));
		$("#gm_form textarea[field_key='apl']").val(JSON.stringify(gold_list));
		
		//if(check_update(that)){
		$("#gm_form textarea[field_key='arl']").attr('name', 'arl');
		$("#gm_form textarea[field_key='apl']").attr('name', 'apl');
		alert('保存成功');
			//return;
		//}
		//alert('没修改');
	}
	
	this.show = function(container){
		var that = this;
		if(!container)
		{
			window.load_gm_template("exchange_active/exchange_active").done(function(tpl){
				var doTpl = doT.template(tpl);
				container = doTpl();
				$("body").append(container);
				/*$(container).dialog({title:"充值活动参数配置",
				close:function(){}});*/
				container = $("#exchange_active_container");
			 	that.show(container);
			});
			return;
		}
		
		container.hide();
		
		var gift_list = $("#gm_form textarea[field_key='arl']").val();
		var gold_list = $("#gm_form textarea[field_key='apl']").val(); 
		
		try{ 
			gift_list = eval('(' + gift_list + ')');
			gold_list = eval('(' + gold_list + ')');
		}catch(e){
			gift_list = [];
			gold_list = [];
		}
		
		var gold_dict = {};
		var gold_list_len = gold_list.length;
		for (var i = 0 ; i < gold_list_len; i ++){
			var gold = gold_list[i];
			var gift_array = gold_dict[gold];
			if (!gift_array)
				gift_array = [];
			var goods_list = gift_list[i];
			
			var goods_list_len = goods_list.length;
			for(var k = 0 ; k < goods_list_len; k ++){
				var goods_item = goods_list[k];
				gift_array.push({goods_type:goods_item[0], id:goods_item[1]});
				
				add_item({gold:gold, goods_type:goods_item[0], id:goods_item[1]});
			}
			gold_dict[gold] = gift_array;
		}
		
		that.old_gold_dict = gold_dict;
		
		container.find("#btn_append").bind('click', function(){add_item();});
		
		container.find('#btn_save').bind('click', function(){save(that)});
		
		container.dialog({title:"充值活动设置",close:function(){$("#exchange_active_container").remove();}});
	}
	
}

$(document).ready(function(){
	var editor = new exchange_editor();
	var btn = $('<input id="btn_exchange_active_config" type="button" value="配置" />');
	var target = $("#gm_form textarea[field_key='apl']");
	if(target.length <= 0)
		return;
		
	target.after(btn);
	$("#btn_exchange_active_config").live('click', function(){
		//alert('sfsdf');
		$("#exchange_active_container").remove();
		editor.show();
	});
});
