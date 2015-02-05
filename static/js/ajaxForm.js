$(document).ready(function() {
	$("form.ajax").bind("submit", function() {
		
		$("input").attr('disabled', true);
		var target = $(this);
		var todo = target.attr("todo");

		var param = GetPostParameter(this);

		var url = target.attr("action");

		var options = {
			type : "post",
			url : url,
			contentType : "application/x-www-form-urlencoded; charset=utf-8",
			data : param,
			success : function(result) {
				if (todo == null || todo == "") {
					default_tip(result);
				} else {
					eval(todo + "(result,target)");
				}
				$("input").attr('disabled', false); 
			},
			cache : false,
			timeout : 5000,
			error : function() {
				$("#tip_box").html("链接超时！请重试");
				$("#tip_box").dialog({ modal: true });
				$("input").attr('disabled', false);
			}
		}
		$.ajax(options);
		return false;
	});
});