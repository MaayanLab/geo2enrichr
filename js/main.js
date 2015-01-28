var main = function() {

	var isGds = function() {
		var path;
		if (window.location.pathname !== '/') {
			path = window.location.pathname.split('/')[1];
			if (path === 'sites') {
				return true;
			} else if (path === 'geo') {
				return false;
			}
		}
	};

	var init = function() {
		// EXTENSION_ID, DEBUG, and SERVER are set in config.js via deploy.sh.
	    var events = Events(),
			notifier = Notifier(DEBUG),
			targetApps = TargetApps(events),
			templater = Templater(EXTENSION_ID, targetApps),
			baseScraper = BaseScraper(DEBUG),
			scraper,
			bootstrapper,
			ui,
			comm;

		// TODO: Make GdsUi and GseUi both part of a single Bootstrapper module?.
		if (isGds()) {
			modeScraper = GdsScraper(events);
			bootstrapper = GdsUi(events, templater);
		} else {
			modeScraper = GseScraper(events, templater);
			bootstrapper = GseUi(events, templater);
		}

		scraper = $.extend(modeScraper, baseScraper);
		comm = Comm(events, notifier, targetApps, SERVER);
		ui = BaseUi(comm, events, notifier, scraper, targetApps, templater);
		
		bootstrapper.init();

		notifier.log('g2e loaded.');
	};

	init();
};
