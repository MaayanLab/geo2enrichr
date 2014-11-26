var GEO2Enrichr = GEO2Enrichr || {};

(function(app, $) {

	app.main = {};

	// Set this to `false` before deploying.
	app.debug = false;

	app.global = {};

	$(document).ready(function() {
		if (app.main.__set_mode()) {
			app.notifier.log('GEO2Enrichr');
			app.mode.init();
		}
	});

	app.main.__set_mode = function() {
		var relevant_path;
		if (window.location.pathname !== '/') {
			relevant_path = window.location.pathname.split('/')[1];
			if (relevant_path === 'sites') {
				app.mode = app.gds;
				return true;
			} else if (relevant_path === 'geo') {
				app.mode = app.gse;
				return true;
			}
		}
		return false;
	};

})(GEO2Enrichr, jQuery);