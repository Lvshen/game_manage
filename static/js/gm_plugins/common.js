(function(w) {
	w.load_gm_template = function(tpl_url) {
		var tmpl = null;
		//localStorage.getItem(tpl_url);
		if (!tmpl) {//如果模板不存在，获取
			tmpl = $.get('/static/js/gm_plugins/template/' + tpl_url + '.html', {
				cache : false
			}).done(function(data) {
				localStorage.setItem(tpl_url, data);
			});
		} else {
			var dtd = $.Deferred();
			tmpl = dtd.resolve(tmpl);
		}
		return tmpl;
	}
})(window);

function timestamp_to_time_str(timestamp) {
	var unixTimestamp = new Date(timestamp * 1000);
	var commonTime = unixTimestamp.toLocaleString();
	return commonTime;
}

//var s = "2006-12-13 09:41:30";
//var s2 = '2006-12-15 09:42:00';
function DateDiff(s, s2) {//sDate1和sDate2是2002-12-18格式
	var aDate, oDate1, oDate2, iDays;
	oDate1 = new Date(Date.parse(s.replace(/-/g,"/")));
	oDate2 = new Date(Date.parse(s2.replace(/-/g,"/")));
	iDays = parseInt(Math.abs(oDate1 - oDate2) / 1000 / 60 / 60 / 24);
	if ((oDate1 - oDate2) < 0) {
		return -iDays;
	}
	return iDays;
}