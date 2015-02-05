var submit_timer = null;
$(document).ready(function(){
	$(".editor input[type='text']").each(function()
	{
		$(this).focus(function(){
			$(this).addClass("focus");
			$(this).select();
		});
		
		$(this).blur(function(){
			$(this).removeClass("foucs");
		});
		$(this).keyup(function(){
			var key = $(this).attr("name").split("|")[1];
			$("#status_" +key).html("输入中...");
			clearTimeout(submit_timer);
			submit_timer = setTimeout("quick_submit('"+key+"')",800);
		});
	});
//	var submit = $(".form input[type='submit']");
//	var new_submit = '<input type="button" value="'+submit.attr("value")+'" onclick="submit(this.form)" class="submit" />';
//	submit.replaceWith(new_submit);
});

function quick_submit(id)
{
	$("#status_" +id).html("保存中...");
	submit($(".editor").parent(),id);
}

function submit(the_form,key)
{
	var datas = new Array();
	
	the_form = $(the_form)
	the_form.find("input,select,textarea").each(function(){
		var item = $(this);
		if(item.attr("name")!=null && item.attr("name")!="")
		{
			var name = item.attr("name");
			if(key==null || name.indexOf("|" + key)!=-1)
				datas[datas.length]=name.replace("|" + key,"")+"="+item.val();
		}
	});

	var url = the_form.attr("action");
	if(key!=null)
		url += "/" + key;
	$.ajax({
		url:url,
		type:the_form.attr("method"),
		cache:false,
		data:datas.join("&"),
		success:function(data){alert(data);
			if(key!=null)
				$("#status_"+key).html("完成");
		},
		error:function(){}
	})
}