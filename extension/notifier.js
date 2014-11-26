var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.notifier = {};

	app.notifier.log = function(msg) {
		if (app.debug) {
			console.log(msg);
		}
	};

	app.notifier.prompt = function(msg, deflt) {
		return prompt(msg, deflt);
	};

	app.notifier.warn = function(msg) {
		alert(msg);
	};

})(GEO2Enrichr, jQuery);