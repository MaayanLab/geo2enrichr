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
			targetApp = TargetApp(),
			templater = Templater(EXTENSION_ID, targetApp),
			baseScraper = BaseScraper(DEBUG, events),
			scraper,
			ui,
			comm;

		if (isGds()) {
			modeScraper = GdsScraper(events);
			scraper = $.extend(modeScraper, baseScraper);
		} else {
			modeScraper = GseScraper(events, templater);
			scraper = $.extend(modeScraper, baseScraper);
		}
		comm = Comm(events, notifier, targetApp, SERVER);
		ui = $.extend(GdsUi(templater, events), BaseUi(comm, events, notifier, scraper, targetApp, templater));

		// This executes in the background, collecting information about the page before the user even inputs.
		if (scraper.getAccessionFromUrl) {
			comm.fetchMetadata(scraper.getAccessionFromUrl());
		}

		ui.init();
		notifier.log('g2e loaded.');
	};

	init();
};
